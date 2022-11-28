from symbols.node import Node
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
