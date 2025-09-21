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
    "IF": "c1",
    "ELSE": "c2",
    "BOOL": "c3",
    "STRUCT": "c4",
    "TUPLE": "c5",
    "LIST": "c6",
    "ARRAY": "c7",
    "NEST": "c8",
    "DERIVE": "c9",
    "POLY": "ca",
    "PROOF": "cb",
    "FOR": "cc",
    "WHILE": "cd",
    "NEST": "ce",
    "FUNC_DEF": "cf",
    "FUNC_CALL": "cg",
    "FIELD": "ch",
    "RETURN": "ci",
    "INDEX": "cj",
    "ASSIGN": "ck",
    "BREAK": "cl",
    "CONTINUE": "cm",
    "SWITCH": "cn",
    "CASE": "co",
    "DEFAULT": "cp",
    "FIELD_ASSIGN": "cq",
    "MATCH": "cr",
    "PATTERN": "cs",
    "METHOD_DEF": "ct",
    "METHOD_CALL": "cu",
    "TRAIT_DEF": "cv",
    "TRAIT_IMPL": "cw",
    "DESTRUCT": "cx",
    "TRAIT_EXTENDS": "cy",
    "GENERIC_TRAIT": "cz",
    "GENERIC_IMPL": "caa",
    "ENUM_DEF": "cba",
    "VARIANT": "cbb",
    "GENERIC_HIGHER": "cbc",
    "DO_BLOCK": "cbd",
    "FOR_BLOCK": "cbe",
    "MONAD_BIND": "cbf",
    "MONAD_YIELD": "cbg"
}

class ASTNode:
    def __init__(self, tag, value=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"ASTNode({self.tag}, {self.value}, {self.children})"

