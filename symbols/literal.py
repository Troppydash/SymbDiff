from symbols.node import Node, NodePrecedence


class Literal(Node):
    pass

class Variable(Literal):
    precedence = NodePrecedence.LITERAL

    def __init__(self, symbol: str = 'x'):
        super().__init__([], symbol)
        self.what = 12

    def as_symbol(self):
        return self.symbol

    def as_display(self, parent_precedence: NodePrecedence = NodePrecedence.LOWEST) -> str:
        return self.symbol


class Real(Literal):
    number: float
    precedence = NodePrecedence.LITERAL

    def __init__(self, number: float):
        super().__init__([], 'R')
        self.number = number

    def as_symbol(self):
        return f"{self.number}"

    def as_display(self, parent_precedence: NodePrecedence = NodePrecedence.LOWEST) -> str:
        return f"{self.number}"

    def copy(self) -> 'Node':
        return Real(self.number)


class Int(Literal):
    number: int
    precedence = NodePrecedence.LITERAL

    def __init__(self, number: int):
        super().__init__(number)
        self.symbol = 'I'


Literal = Variable | Real
