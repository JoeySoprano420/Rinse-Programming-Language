# lexer.py — Rinse v0.1.0
# Tokenizer for .rn source

import re

KEYWORDS = {
    "init", "process", "item", "flow",
    "let", "print", "parallel", "is", "return"
}

TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),
    ("STRING",   r"\".*?\""),
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP",       r"[+\-*/=]"),
    ("SYMBOL",   r"[{}():,]"),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_pat = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKEN_SPEC))

def tokenize(code):
    tokens = []
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "ID" and value in KEYWORDS:
            kind = value.upper()
        elif kind == "NUMBER":
            value = int(value)
        elif kind == "STRING":
            value = value.strip('"')
        elif kind == "SKIP" or kind == "NEWLINE":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected char {value}")
        tokens.append((kind, value))
    return tokens

if __name__ == "__main__":
    code = 'init main { let x: int = 12 print(x) }'
    print(tokenize(code))
