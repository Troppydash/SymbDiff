from typing import Any

from symbols import binary, literal, function, operator, unary
from symbols.node import Node, Expression
from symbols.binary import Add, Sub, Mul, Div, Pow
from symbols.unary import Negate


class OverloadException(RuntimeError):
    pass


def __overload_add(instance, other):
    if not isinstance(other, Node):
        raise OverloadException()

    return Add(instance, other)


def __overload_sub(instance, other):
    if not isinstance(other, Node):
        raise OverloadException()

    return Sub(instance, other)


def __overload_mul(instance, other):
    if not isinstance(other, Node):
        raise OverloadException()

    return Mul(instance, other)


def __overload_div(instance, other):
    if not isinstance(other, Node):
        raise OverloadException()

    return Div(instance, other)


def __overload_pow(instance, other):
    if not isinstance(other, Node):
        raise OverloadException()

    return Pow(instance, other)


def __overload_neg(instance):
    return Negate(instance)


def overload():
    setattr(Node, '__add__', __overload_add)
    setattr(Node, '__sub__', __overload_sub)
    setattr(Node, '__mul__', __overload_mul)
    setattr(Node, '__truediv__', __overload_div)
    setattr(Node, '__pow__', __overload_pow)
    setattr(Node, '__neg__', __overload_neg)


# experimental ast overload

import ast


class AstTransformerError(RuntimeError):
    pass


class AstTransformer:
    """
    Recursive tree transformer, a class as configuration might be needed
    """

    def transform(self, pyast: Any) -> Node:
        match pyast:
            case ast.Module():
                # only parses the first body expression value
                if len(pyast.body) != 1:
                    raise AstTransformerError(
                        f"unable to parse a module with multiple body expressions, len(body) = {len(pyast.body)}"
                    )

                if not isinstance(expression := pyast.body[0], ast.Expr):
                    raise AstTransformerError(
                        f"unable to parse a module with a non-expression body"
                    )

                return self.transform(expression.value)

            case ast.BinOp():
                # parse as binary operator, first parse left and right
                left = self.transform(pyast.left)
                right = self.transform(pyast.right)

                match pyast.op:
                    case ast.Add():
                        return binary.Add(left, right)
                    case ast.Sub():
                        return binary.Sub(left, right)
                    case ast.Mult():
                        return binary.Mul(left, right)
                    case ast.Div():
                        return binary.Div(left, right)
                    case ast.Pow():
                        return binary.Pow(left, right)
                    case _:
                        raise AstTransformerError(
                            f"unknown binary operator, type(op) = {type(pyast.op)}"
                        )

            case ast.Name():
                # parse as variable
                name = pyast.id
                return literal.Variable(name)

            case ast.Constant():
                # parse as real or int
                value = pyast.value
                if isinstance(value, int):
                    return literal.Int(value)
                elif isinstance(value, float):
                    return literal.Real(value)
                else:
                    raise AstTransformerError(
                        f"unknown constant value, type(constant) = {type(pyast.value)}"
                    )

            case ast.UnaryOp():
                value = self.transform(pyast.operand)
                return unary.Negate(value)

            case ast.Call():
                # parse functions

                # reject with multiple args
                if len(pyast.args) != 1:
                    raise AstTransformerError(
                        f"function cannot have multiple arguments, len(args) = {len(pyast.args)}"
                    )

                expression = self.transform(pyast.args[0])

                # identify name
                name = str(pyast.func.id)
                if name.startswith('d') and len(name) == 2:
                    return operator.Diff(
                        expression,
                        name[1]
                    )

                match name.lower():
                    case 'sin':
                        return function.Sin(expression)
                    case 'cos':
                        return function.Cos(expression)
                    case 'exp':
                        return function.Exp(expression)
                    case 'log':
                        return function.Log(expression)
                    case _:
                        raise AstTransformerError(
                            f"unknown function name: '{name}'"
                        )


            case _:
                raise AstTransformerError(
                    f"unknown node type, type(node) = {type(pyast)}"
                )



def as_expression(expression: str) -> Expression:
    parsed = ast.parse(expression, 'as_expression__inner')
    transformer = AstTransformer()
    return transformer.transform(parsed)
