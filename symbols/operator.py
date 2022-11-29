from symbols import Node
from symbols.node import NodePrecedence


class Diff(Node):
    regard: str
    precedence = NodePrecedence.FUNCTION

    def __init__(self, expression: Node, symbol: str = 'x'):
        super().__init__([expression], f'd/d{symbol} %0')
        self.regard = symbol

    @property
    def expression(self):
        return self.children[0]

    @expression.setter
    def expression(self, value):
        self.children[0] = value