"""
Dodecagram AST (0-9, a, b)
"""
class Node:
    def __init__(self, tag, children=None, value=None):
        self.tag = tag      # dodecagram digit
        self.children = children or []
        self.value = value

    def __repr__(self):
        return f"Node({self.tag}, {self.value}, {self.children})"

# Example tags
DODECAGRAM = {
    "PROGRAM": "0",
    "BLOCK": "1",
    "STATEMENT": "2",
    "EXPR": "3",
    "TYPE": "4",
    "FUNC": "5",
    "VAR": "6",
    "VALUE": "7",
    "OP": "8",
    "FLOW": "9",
    "ITEM": "a",
    "MACRO": "b",
}
