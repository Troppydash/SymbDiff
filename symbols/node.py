from enum import IntEnum


class NodePrecedence(IntEnum):
    LOWEST = 0
    EQUAL = 1
    ADDSUB = 3
    MULDIV = 4
    POW = 5
    UNARY = 6
    FUNCTION = 7
    LITERAL = 8
    HIGHEST = 100


class Node:
    children: list['Node']  # the child nodes
    symbol: str  # a format-able string of printable items
    precedence: NodePrecedence = NodePrecedence.LOWEST  # the higher, the more grouped it is

    def __init__(self, children: list['Node'], symbol: str) -> None:
        self.children = children
        self.symbol = symbol

    def as_symbol(self) -> str:
        replaced = self.symbol

        # start the replacing step
        for index, value in enumerate(self.children):
            replaced = replaced.replace(
                f'%{index}',
                f"( {value.as_symbol()} )"
            )

        return replaced

    def copy(self) -> 'Node':
        return Node(
            [child.copy() for child in self.children],
            self.symbol
        )

    def as_display(self, parent_precedence: NodePrecedence = NodePrecedence.LOWEST) -> str:
        replaced = self.symbol

        # start the replacing step
        for index, child in enumerate(self.children):
            child_symbol = child.as_display(self.precedence)
            replaced = replaced.replace(
                f'%{index}',
                child_symbol
            )

        if self.precedence < parent_precedence:
            replaced = f"({replaced})"

        return replaced

    # equals
    def weak_equals(self, other: 'Node') -> bool:
        """
        Weak equals compares the display out of the expressions to be the same,
        does not regard the AST structure
        :param other: The other expression
        :return: Whether they are equal
        """
        return self.as_display() == other.as_display()


Expression = Node
