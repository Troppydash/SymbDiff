from typing import Callable, Any

from symbols import Node

Visitor = Callable[[Node, list[Any]], Any]


class ExpressionVisitor:
    """
    A generic visitor for all nodes in the tree
    """

    # a visit closure with a (node, visit(node.children)) as parameter, returns a value to the parent
    visitor: Visitor


    def __init__(self, visitor: Visitor) -> None:
        self.visitor = visitor

    def visit(self, node: Node):
        # visit the children
        results = [self.visit(child) for child in node.children]
        return self.visitor(node, results)
