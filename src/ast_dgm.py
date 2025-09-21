# ast_dgm.py — Rinse v0.1.0
# Dodecagram AST (base-12)

DGM_MAP = {
    "PROGRAM": 0,
    "BLOCK": 1,
    "STMT": 2,
    "EXPR": 3,
    "TYPE": 4,
    "FUNC": 5,
    "VAR": 6,
    "VALUE": 7,
    "OP": 8,
    "FLOW": 9,
    "ITEM": "a",
    "MACRO": "b",
}

class ASTNode:
    def __init__(self, tag, value=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.tag}, {self.value}, {self.children})"
