import symbols.literal as lit
import symbols.binary as binary
import symbols.function as fn
from executor.simplify import simplify_expression
from symbols import operator, function
from symbols.overload import overload, as_expression


def main():
    overload()


    # x = lit.Variable('x')
    # z = lit.Variable('z')
    # expression = function.Cos(x * lit.Real(2.0)) * lit.Real(2) * z ** lit.Real(2.0)
    # expression = as_expression('x ** x')
    # dydx = operator.Diff(expression, 'x')
    # dydz = operator.Diff(expression, 'z')
    # print(dydx.as_display())
    # print(simplify_expression(simplify_expression(dydx)).as_display())
    # print('')
    # print(dydz.as_display())
    # print(simplify_expression(dydz).as_display())

    expression = 'dx(2**x * sin(x) / cos(2*x))'
    print(simplify_expression(as_expression(expression)).as_display())


main()

