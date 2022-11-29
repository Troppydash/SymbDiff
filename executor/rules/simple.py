from executor.evaluator import interpret_expression
from executor.rule import Rule
from executor.visitor import ExpressionVisitor
from symbols import Expression, literal, unary, binary
from symbols.operator import Diff
from symbols.literal import Variable


def contains_variable(expression: Expression, symbol: str | None = None) -> bool:
    visitor = ExpressionVisitor(
        lambda node, results:
        True
        if any(results)
        else isinstance(node, Variable) and (symbol is None or node.symbol == symbol)
    )
    return visitor.visit(expression)


def contains_unevallable(expression: Expression) -> bool:
    blacklist = (Variable, Diff,)
    visitor = ExpressionVisitor(
        lambda node, results:
        True
        if any(results)
        else isinstance(node, blacklist)
    )
    return visitor.visit(expression)


# evaluate any evaluable expression
class EvaluateRule(Rule):
    weight = 10.0

    def match(self, expression: Expression) -> bool:
        match expression:
            case literal.Real():
                return False
            case _:
                return not contains_unevallable(expression)

    def apply(self, expression: Expression) -> Expression:
        value = interpret_expression(expression)
        return literal.Real(value)


# remove identities
class IdentityRule(Rule):
    weight = 10.0

    POW_SIMP = 1
    MUL_SIMP = 2
    ADD_SIMP_L = 3
    ADD_SIMP_R = 4
    SUB_SIMP_R = 5

    def match(self, expression: Expression) -> bool:
        match expression:
            case binary.Pow() if isinstance(exp := expression.right, literal.Real) and (
                    exp.number == 1.0 or exp.number == 0.0):
                self.setitem(self.POW_SIMP)
                return True
            case binary.Mul() if isinstance(left := expression.left, literal.Real) and (
                    left.number == 1.0 or left.number == 0.0):
                self.setitem(self.MUL_SIMP)
                return True

            case binary.Add() if isinstance(left := expression.left, literal.Real) and left.number == 0.0:
                self.setitem(self.ADD_SIMP_L)
                return True
            case binary.Add() if isinstance(right := expression.right, literal.Real) and right.number == 0.0:
                self.setitem(self.ADD_SIMP_R)
                return True

            case binary.Sub() if isinstance(right := expression.right, literal.Real) and right.number == 0.0:
                self.setitem(self.SUB_SIMP_R)
                return True

            case _:
                self.setitem(0)
                return False

    def apply(self, expression: Expression) -> Expression:
        match self.item:
            case self.POW_SIMP:
                exponent = expression.right
                if exponent.number == 1.0:
                    return expression.left
                if exponent.number == 0.0:
                    return literal.Real(1)
            case self.MUL_SIMP:
                left = expression.left
                if left.number == 1.0:
                    return expression.right
                if left.number == 0.0:
                    return literal.Real(0)

            case self.ADD_SIMP_L:
                return expression.right

            case self.ADD_SIMP_R:
                return expression.left

            case self.SUB_SIMP_R:
                return expression.left


# puts the multiplication constant on the left
# class LeftConstant(Rule):
#     weight = 10.0
#
#     def match(self, expression: Expression) -> bool:
#         match expression:
#             case binary.Mul() if isinstance(expression.right, literal.Real) and contains_variable(expression.left):
#                 return True
#             case _:
#                 return False
#
#     def apply(self, expression: Expression) -> Expression:
#         return binary.Mul(
#             expression.right,
#             expression.left
#         )


# Rule to combine the communicative operators
class CombineRule(Rule):
    weight = 5.0

    COM_RULE_L = 1
    COM_RULE_R = 2

    def match(self, expression: Expression) -> bool:
        match expression:
            case binary.Add() | binary.Sub() | binary.Mul() | binary.Div():
                """
                [[P + R] + R] => [P + [R + R]]          
                """
                if isinstance(expression.right, literal.Real) \
                        and type(left := expression.left) == type(expression) \
                        and isinstance(left.right, literal.Real):
                    self.setitem(self.COM_RULE_L)
                    return True

                # although this rule is covered by the left align rule, so maybe deprecated
                """
                [R + [R + P]] => [[R + R] + P]
                """
                if isinstance(expression.left, literal.Real) \
                        and type(right := expression.right) == type(expression) \
                        and isinstance(right.left, literal.Real):
                    self.setitem(self.COM_RULE_R)
                    return True
                return False

            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        match self.item:
            case self.COM_RULE_L:
                cls = expression.__class__
                return cls(
                    expression.left.left,
                    cls(expression.left.right, expression.right),
                )
            case self.COM_RULE_R:
                cls = expression.__class__
                return cls(
                    cls(expression.left, expression.right.left),
                    expression.right.right
                )


# rule to move the literals to the left
# with reals the most left, followed by variables
class ReorderRule(Rule):
    weight = 6.0

    def match(self, expression: Expression) -> bool:
        match expression:
            case binary.Add() | binary.Sub() | binary.Mul() | binary.Div():
                """
                [P + R] => [R + P]
                """
                if isinstance(expression.right, literal.Real) and not isinstance(expression.left, literal.Real):
                    return True

                """
                [P + x] => [x + P]
                """
                if isinstance(expression.right, literal.Variable) and not isinstance(expression.left,
                                                                                     (literal.Real, literal.Variable)):
                    return True
            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        return expression.__class__(
            expression.right,
            expression.left
        )


# improve the tree structure to be left aligned
class LeftAlignRule(Rule):
    weight = 7.0

    BB_RULE = 1
    LB_RULE = 2

    def match(self, expression: Expression) -> bool:
        match expression:
            case binary.Add() | binary.Sub() | binary.Mul() | binary.Div():
                """
                [[A + B] + [C + D]] => [[[A + B] + C] + D]
                """
                if type(expression.left) == type(expression) and type(expression.right) == type(expression):
                    self.setitem(self.BB_RULE)
                    return True

                """
                [A + [B + C]] => [[A + B] + C]
                """
                if type(expression.right) == type(expression):
                    self.setitem(self.LB_RULE)
                    return True

            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        match self.item:
            case self.BB_RULE:
                return expression.right.__class__(
                    expression.__class__(
                        expression.left, expression.right.left
                    ),
                    expression.right.right
                )

            case self.LB_RULE:
                return expression.right.__class__(
                    expression.__class__(
                        expression.left,
                        expression.right.left
                    ),
                    expression.right.right
                )

# TODO, POWER RULES (DIVISION too)
# also correct the precedence ignoring on reordering

simplerules = [EvaluateRule(), IdentityRule(), CombineRule(), ReorderRule(), LeftAlignRule()]
