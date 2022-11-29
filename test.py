import unittest

import symbols.literal as lit
import symbols.binary as bi
import symbols.function as fn
from executor.simplify import simplify_expression
from symbols import operator, function, make
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


class TestAsExpression(unittest.TestCase):
    def setUp(self) -> None:
        overload()

    def test_basic(self):
        expression = '(z + 2) * 3.1 - 0.1 / x ** 2'
        expected = (lit.Variable('z') + lit.Int(2)) * lit.Real(3.1) - lit.Real(0.1) / lit.Variable('x') ** lit.Int(2)
        self.assertEqual(
            as_expression(expression).as_display(),
            expected.as_display()
        )

    def test_functions(self):
        expression = 'sin(x) + cos(2 * x) + exp(exp(x)) / log(1.0) * dx(dz(x * z))'
        x, z = make.variables('x z')
        expected = function.Sin(x) + function.Cos(lit.Int(2) * x) + function.Exp(function.Exp(x)) / function.Log(lit.Real(1.0)) * \
            operator.Diff(operator.Diff(x * z, 'z'), 'x')
        self.assertEqual(
            as_expression(expression).as_display(),
            expected.as_display()
        )


if __name__ == '__main__':
    unittest.main()
