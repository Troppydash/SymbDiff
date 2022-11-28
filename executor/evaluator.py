import math

from executor.visitor import ExpressionVisitor
from symbols.node import Expression, Node
from symbols import literal, binary, unary, function
from typing import Callable, Any



def _interpret_visitor(node: Node, results: list[float]) -> float:
    match node:
        case literal.Real():
            return node.number

        case binary.Add():
            return results[0] + results[1]

        case binary.Sub():
            return results[0] - results[1]

        case binary.Mul():
            return results[0] * results[1]

        case binary.Div():
            return results[0] / results[1]

        case binary.Pow():
            return results[0] ** results[1]

        case unary.Negate():
            return -results[0]

        case function.Sin():
            return math.sin(results[0])

        case function.Cos():
            return math.cos(results[0])

        case function.Exp():
            return math.exp(results[0])

        case function.Log():
            return math.log(results[0])

        case _:
            raise TypeError(f"unsupported node type, {type(node)}")


def interpret_expression(expression: Expression) -> float:
    visitor = ExpressionVisitor(_interpret_visitor)
    return visitor.visit(expression)
