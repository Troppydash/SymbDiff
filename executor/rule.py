import abc
import queue

from symbols import Expression


class Rule(abc.ABC):
    weight: float = 0.0  # the higher the weighting, the more quickly it applies
    id: int = 0  # custom id to order

    item: int = 0  # the subnumber of the rule that matched, optionally used to keep state

    def setitem(self, item: int):
        self.item = item

    @abc.abstractmethod
    def match(self, expression: Expression) -> bool:
        """
        Returns whether the expression matches the rule
        :param expression: The expression
        :return: Whether the expression matches the rule
        """
        pass

    @abc.abstractmethod
    def apply(self, expression: Expression) -> Expression:
        """
        Returns the modified expression by the rule
        :param expression: The expression
        :return: The modified expression
        """
        pass


# a generic rule applier class
class RuleApplier:
    rules: list[Rule]

    # checking for loops
    depth: str  # the depth id for the operation
    logs: list[str]  # the list of depth/rules

    MAX_LOOP_SIZE = 20

    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.prepare()

    def order_rules(self):
        rules = sorted(self.rules, key=lambda r: r.weight, reverse=True)
        for i, r in enumerate(rules):
            r.id = i
        self.rules = rules

    def prepare(self):
        self.order_rules()
        self.depth = ''
        # self.logs = ['7', '9', '4', '7', '9']
        self.logs = []

    def __addlog(self, depth: str, rule: int):
        if len(self.logs) >= self.MAX_LOOP_SIZE:
            self.logs.pop(0)

        self.logs.append(f"{depth}_{rule}")

    def __poplog(self):
        self.logs.pop()

    def __isrepeated(self):
        # check for repeats, only accepts loop of size >= 2
        # O(n^2) lmao
        size = len(self.logs)
        for loopsize in range(2, size // 2 + 1):
            for i in range(size - 2 * loopsize + 1):
                s1 = self.logs[i:i + loopsize]
                s2 = self.logs[i + loopsize: i + 2 * loopsize]

                # check for slice equality
                for i in range(len(s1)):
                    if s1[i] != s2[i]:
                        break
                else:
                    return True
        return False

    def __logloop(self, verbose: bool = True):
        print(f"Warning: found loop {self.logs}")
        # print extra
        if verbose:
            names = []
            for log in self.logs:
                depth, rule_i = log.split('_')
                rule = self.rules[int(rule_i)]
                names.append(f"({type(rule).__name__}) {depth}")

            print(f"Verbose: [ {', '.join(names)} ]")

    def apply(self, expression: Expression) -> tuple[bool, Expression]:
        current = expression  # the modified expression
        changed = False  # whether the expression has changed

        # keep applying rules on the expression
        while True:
            # whether any change is made
            matched = False

            # apply rules on children
            result = []
            for index, child in enumerate(current.children):
                # add depth
                self.depth = f"{self.depth}{index}"
                result.append(self.apply(child))
                # remove depth
                self.depth = self.depth[:-1]

            # apply changes, and check for changes
            for index, res in enumerate(result):
                modified, new_child = res
                if modified:
                    matched = True
                    current.children[index] = new_child

            # try to apply the rules on the node
            for rule in self.rules:
                if rule.match(current):

                    # check for loops
                    self.__addlog(self.depth, rule.id)
                    if self.__isrepeated():  # skip the rule if found a loop
                        self.__logloop()
                        self.__poplog()
                        break

                    matched = True
                    current = rule.apply(current)
                    # also break the entire loop, for the children must be rescanned
                    break

            # any changes means changed is true, no changes means exit
            if matched:
                changed = True
            else:
                break

        return changed, current
