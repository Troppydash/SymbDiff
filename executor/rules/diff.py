from executor.rule import Rule
from executor.rules.simple import contains_variable
from symbols import Expression, literal, operator, binary, unary, function


### differential rules ###

# differentiate constants
class ConstantRule(Rule):
    weight = 10.0

    def match(self, expression: Expression) -> bool:
        match expression:
            case operator.Diff():
                return not contains_variable(expression.expression, expression.regard)
            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        return literal.Real(0)


# differentiates arithmetic operations
class ArithmeticRule(Rule):
    weight = 9.0

    def match(self, expression: Expression) -> bool:
        match expression:
            case operator.Diff():
                # check for arithmetic rules
                # addition, subtraction rule
                # multiplication and division rule
                # negate rule
                match expression.expression:
                    case binary.Add() | binary.Sub() | binary.Mul() | binary.Div() | unary.Negate():
                        return True
                    case _:
                        return False

            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        inner = expression.expression
        match inner:
            case unary.Negate():
                return unary.Negate(
                    operator.Diff(inner.children[0], expression.regard)
                )
            case binary.Add():
                return binary.Add(
                    operator.Diff(inner.left, expression.regard),
                    operator.Diff(inner.right, expression.regard)
                )
            case binary.Sub():
                return binary.Sub(
                    operator.Diff(inner.left, expression.regard),
                    operator.Diff(inner.right, expression.regard)
                )
            case binary.Mul():
                return binary.Add(
                    binary.Mul(
                        inner.left,
                        operator.Diff(inner.right, expression.regard)
                    ),
                    binary.Mul(
                        inner.right,
                        operator.Diff(inner.left, expression.regard)
                    )
                )
            case binary.Div():
                return binary.Div(
                    binary.Sub(
                        binary.Mul(
                            inner.right,
                            operator.Diff(inner.left, expression.regard)
                        ),
                        binary.Mul(
                            inner.left,
                            operator.Diff(inner.right, expression.regard)
                        )
                    ),
                    binary.Pow(
                        inner.right,
                        literal.Real(2)
                    )
                )

            case _:
                raise Exception("not matched, this should never happen")


# differentiate powers and exponentials
class PowerRule(Rule):
    weight = 9.0

    POW_RULE = 2
    CONSTANT_RULE = 1

    def match(self, expression: Expression) -> bool:
        match expression:
            case operator.Diff():
                match expression.expression:
                    case binary.Pow():
                        self.setitem(self.POW_RULE)
                        return True
                    case literal.Variable():
                        self.setitem(self.CONSTANT_RULE)
                        return True
            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        inner = expression.expression

        if self.item == self.CONSTANT_RULE:
            return literal.Real(1.0)

        # else check for power_rule
        # only when the exponent is a constant
        if not contains_variable(inner.right, expression.regard):
            return binary.Mul(
                binary.Mul(
                    inner.right,
                    binary.Pow(inner.left, binary.Sub(inner.right, literal.Real(1))),
                ),
                operator.Diff(inner.left, expression.regard)
            )

        # returns the ln version
        return operator.Diff(
            function.Exp(
                binary.Mul(
                    inner.left,
                    function.Log(inner.right)
                )
            ),
            expression.regard
        )


class ExpLogRule(Rule):
    weight = 9.0

    EXP_RULE = 1
    LOG_RULE = 2

    def match(self, expression: Expression) -> bool:
        match expression:
            case operator.Diff():
                match expression.expression:
                    case function.Exp():
                        self.setitem(self.EXP_RULE)
                        return True
                    case function.Log():
                        self.setitem(self.LOG_RULE)
                        return True
                    case _:
                        return False
            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        inner = expression.expression
        if self.item == self.EXP_RULE:
            return binary.Mul(
                inner,
                operator.Diff(inner.expression, expression.regard)
            )

        if self.item == self.LOG_RULE:
            return binary.Mul(
                binary.Div(
                    literal.Real(1.0),
                    inner.expression
                ),
                operator.Diff(inner.expression, expression.regard)
            )


class TrigRule(Rule):
    weight = 9.0

    SIN_RULE = 1
    COSINE_RULE = 2

    def match(self, expression: Expression) -> bool:
        match expression:
            case operator.Diff():
                match expression.expression:
                    case function.Sin():
                        self.setitem(self.SIN_RULE)
                        return True

                    case function.Cos():
                        self.setitem(self.COSINE_RULE)
                        return True
                    case _:
                        return False
            case _:
                return False

    def apply(self, expression: Expression) -> Expression:
        inner = expression.expression
        match self.item:
            case self.SIN_RULE:
                return binary.Mul(
                    function.Cos(inner.expression),
                    operator.Diff(inner.expression, expression.regard)
                )
            case self.COSINE_RULE:
                return binary.Mul(
                    unary.Negate(function.Sin(inner.expression)),
                    operator.Diff(inner.expression, expression.regard)
                )


diffrules = [ConstantRule(), ArithmeticRule(), PowerRule(), ExpLogRule(), TrigRule()]
