from symbols.node import Node, NodePrecedence


class Negate(Node):
    precedence = NodePrecedence.UNARY

    def __init__(self, node: Node) -> None:
        super().__init__([node], '-%0')

