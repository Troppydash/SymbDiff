from symbols.node import Node, NodePrecedence


class Binary(Node):
    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    @left.setter
    def left(self, value):
        self.children[0] = value

    @right.setter
    def right(self, value):
        self.children[1] = value


class Add(Binary):
    precedence = NodePrecedence.ADDSUB

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right], '%0 + %1')


class Sub(Binary):
    precedence = NodePrecedence.ADDSUB

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right], '%0 - %1')


class Mul(Binary):
    precedence = NodePrecedence.MULDIV

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right], '%0 * %1')


class Div(Binary):
    precedence = NodePrecedence.MULDIV

    def __init__(self, left: Node, right: Node):
        super().__init__([left, right], '%0 / %1')


class Pow(Binary):
    precedence = NodePrecedence.POW

    def __init__(self, base: Node, exp: Node):
        super().__init__([base, exp], '%0 ^ %1')
