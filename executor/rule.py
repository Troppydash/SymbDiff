import abc

from symbols import Expression


class Rule(abc.ABC):
    weight: float = 0.0  # the higher the weighting, the more quickly it applies
    id: int = 0          # custom id to order

    item: int = 0        # the subnumber of the rule that matched, optionally used to keep state

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

    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.order_rules()

    def order_rules(self):
        rules = sorted(self.rules, key=lambda r: r.weight, reverse=True)
        for i, r in enumerate(rules):
            r.id = i
        self.rules = rules

    def apply(self, expression: Expression) -> tuple[bool, Expression]:
        current = expression  # the modified expression
        changed = False       # whether the expression has changed

        # keep applying rules on the expression
        while True:
            # whether any change is made
            matched = False

            # apply rules on children
            result = [self.apply(child) for child in current.children]

            # apply changes, and check for changes
            for index, res in enumerate(result):
                modified, new_child = res
                if modified:
                    matched = True
                    current.children[index] = new_child

            # try to apply the rules on the node
            for rule in self.rules:
                if rule.match(current):
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
