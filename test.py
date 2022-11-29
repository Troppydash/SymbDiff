import unittest

import symbols.literal as lit
import symbols.binary as bi
import symbols.function as fn
from executor.simplify import simplify_expression
from symbols import operator, function, make, unary
from symbols.overload import overload, as_expression


class TestSimplification(unittest.TestCase):
    def setUp(self) -> None:
        overload()

    def test_eval_rule(self):
        expression = lit.Variable() + (lit.Real(2.0) * lit.Real(2.0)) + lit.Real(1.0)
        expected = lit.Real(5.0) + lit.Variable()
        self.assertEqual(
            simplify_expression(expression).as_display(),
            expected.as_display()
        )

    def test_reorder_rule(self):
        expression = '2 * x * 2 + (2 + 4) + 3 * 3 + a + b + c'
        expected = '15 + 4 * x + a + b + c'
        self.assertEqual(
            simplify_expression(as_expression(expression)).as_display(),
            as_expression(expected).as_display()
        )

    def test_hoist_division(self):
        expression = 'a / b * c'
        expected = 'a * c / b'
        self.assertEqual(
            simplify_expression(as_expression(expression)).as_display(),
            as_expression(expected).as_display()
        )

    def test_reorder_and_cancel(self):
        expression = '(x * (2.0 / x) + log(x))'
        expected = '2.0 + log(x)'
        self.__assertSimpExpression(expression, expected)

    def test_identities(self):
        expression = 'a ** 0 + b ** 1 + (c * 0.0) + (c * 1.0) + 0.0 + (0.0 + d) - 0.0 + (e - e) + x / x'
        expected = '2.0 + b + c + d'
        self.__assertSimpExpression(expression, expected)

    def test_leftorder(self):
        expression = "(a + (b - c)) + (d * (e / f))"
        expected = 'a + b - c + d * e / f'
        self.__assertSimpExpression(expression, expected)


    def __assertSimpExpression(self, expression: str, expected: str):
        self.assertEqual(
            as_expression(expected).as_display(),
            simplify_expression(as_expression(expression)).as_display()
        )


class TestAsExpression(unittest.TestCase):
    def setUp(self) -> None:
        overload()

    def test_basic(self):
        expression = '(z + 2) * 3.1 - 0.1 / x ** 2 + -c'
        expected = (lit.Variable('z') + lit.Int(2)) * lit.Real(3.1) - lit.Real(0.1) / lit.Variable('x') ** lit.Int(2) + unary.Negate(lit.Variable('c'))
        self.assertEqual(
            as_expression(expression).as_display(),
            expected.as_display()
        )

    def test_functions(self):
        expression = 'sin(x) + cos(2 * x) + exp(exp(x)) / log(1.0) * dx(dz(x * z))'
        x, z = make.variables('x z')
        expected = function.Sin(x) + function.Cos(lit.Int(2) * x) + function.Exp(function.Exp(x)) / function.Log(
            lit.Real(1.0)) * \
                   operator.Diff(operator.Diff(x * z, 'z'), 'x')
        self.assertEqual(
            as_expression(expression).as_display(),
            expected.as_display()
        )

class TestDifferentiation(unittest.TestCase):
    def setUp(self) -> None:
        overload()

    def test_basic(self):
        expression = 'dx(x + x + 1 + k + 2 * z)'
        expected = '2.0'
        self.__assertDiffExpression(expression, expected)

    def test_arithmetic(self):
        expression = 'dx(x ** 2 + x ** 3 + z * x + x / x)'
        expected = '2 * x + 3 * x ** 2 + z'
        self.__assertDiffExpression(expression, expected)

    def __assertDiffExpression(self, expression: str, expected: str):
        self.assertEqual(
            as_expression(expected).as_display(),
            simplify_expression(as_expression(expression)).as_display()
        )


if __name__ == '__main__':
    unittest.main()
