"""
Rinse Lexer
Turns .rns code into tokens
"""

import re

KEYWORDS = {"init", "item", "flow", "let", "print"}

TOKEN_SPEC = [
    ("NUMBER",  r"\d+"),
    ("ID",      r"[A-Za-z_][A-Za-z0-9_]*"),
    ("LBRACE",  r"\{"),
    ("RBRACE",  r"\}"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("COLON",   r":"),
    ("SEMICOL", r";"),
    ("OP",      r"[=+\-*/]"),
    ("NEWLINE", r"\n"),
    ("SKIP",    r"[ \t]+"),
    ("MISMATCH",r"."),
]

tok_regex = "|".join("(?P<%s>%s)" % pair for pair in TOKEN_SPEC)

def tokenize(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = int(value)
        elif kind == "ID" and value in KEYWORDS:
            kind = value.upper()
        elif kind == "SKIP" or kind == "NEWLINE":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character: {value}")
        tokens.append((kind, value))
    return tokens
