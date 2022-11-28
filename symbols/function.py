from symbols.node import Node, NodePrecedence


class Function(Node):
    precedence = NodePrecedence.FUNCTION

    @property
    def expression(self):
        return self.children[0]

    @expression.setter
    def expression(self, value):
        self.children[0] = value


class Sin(Function):
    def __init__(self, node: Node):
        super().__init__([node], 'sin %0')


class Cos(Function):
    def __init__(self, node: Node):
        super().__init__([node], 'cos %0')


class Exp(Function):
    def __init__(self, node: Node):
        super().__init__([node], 'exp %0')


class Log(Function):
    def __init__(self, node: Node):
        super().__init__([node], 'log %0')
