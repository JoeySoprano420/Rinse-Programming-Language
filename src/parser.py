# parser.py — Rinse v0.1.0
# Simple parser → Dodecagram AST

from lexer import tokenize
from ast_dgm import ASTNode, DGM_MAP

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, kind=None):
        tok = self.peek()
        if kind and tok[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {tok}")
        self.pos += 1
        return tok

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        self.eat("INIT")
        _, name = self.eat("ID")
        block = self.parse_block()
        return ASTNode(DGM_MAP["PROGRAM"], name, [block])

    def parse_block(self):
        self.eat("SYMBOL")  # {
        stmts = []
        while self.peek()[1] != "}":
            stmts.append(self.parse_stmt())
        self.eat("SYMBOL")  # }
        return ASTNode(DGM_MAP["BLOCK"], None, stmts)

    def parse_stmt(self):
        kind, val = self.peek()
        if kind == "LET":
            return self.parse_let()
        elif kind == "PRINT":
            return self.parse_print()
        else:
            raise SyntaxError(f"Unknown stmt {kind}")

    def parse_let(self):
        self.eat("LET")
        _, name = self.eat("ID")
        self.eat("SYMBOL")  # :
        _, typ = self.eat("ID")
        self.eat("OP")  # =
        _, value = self.eat("NUMBER")
        return ASTNode(DGM_MAP["VAR"], (name, typ), [
            ASTNode(DGM_MAP["VALUE"], value)
        ])

    def parse_print(self):
        self.eat("PRINT")
        self.eat("SYMBOL")  # (
        _, name = self.eat("ID")
        self.eat("SYMBOL")  # )
        return ASTNode(DGM_MAP["FLOW"], "print", [
            ASTNode(DGM_MAP["VAR"], name)
        ])

if __name__ == "__main__":
    code = 'init main { let x: int = 12 print(x) }'
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

# parser.py (extended to handle expressions)

def parse_expr(self):
    # supports VAR + VAR and VAR + NUMBER for now
    _, left = self.eat("ID")
    if self.peek()[0] == "OP":  # e.g. +
        op = self.eat("OP")[1]
        kind, right = self.peek()
        if kind == "ID":
            _, right = self.eat("ID")
        elif kind == "NUMBER":
            _, right = self.eat("NUMBER")
        else:
            raise SyntaxError("Expected ID or NUMBER after operator")
        return ASTNode(DGM_MAP["EXPR"], op, [
            ASTNode(DGM_MAP["VAR"], left),
            ASTNode(DGM_MAP["VAR"], right) if isinstance(right, str) else ASTNode(DGM_MAP["VALUE"], right)
        ])
    return ASTNode(DGM_MAP["VAR"], left)

def parse_print(self):
    self.eat("PRINT")
    self.eat("SYMBOL")  # (
    expr = self.parse_expr()
    self.eat("SYMBOL")  # )
    return ASTNode(DGM_MAP["FLOW"], "print", [expr])

# parser.py (extended to handle expressions)

def parse_expr(self):
    # supports VAR + VAR and VAR + NUMBER for now
    _, left = self.eat("ID")
    if self.peek()[0] == "OP":  # e.g. +
        op = self.eat("OP")[1]
        kind, right = self.peek()
        if kind == "ID":
            _, right = self.eat("ID")
        elif kind == "NUMBER":
            _, right = self.eat("NUMBER")
        else:
            raise SyntaxError("Expected ID or NUMBER after operator")
        return ASTNode(DGM_MAP["EXPR"], op, [
            ASTNode(DGM_MAP["VAR"], left),
            ASTNode(DGM_MAP["VAR"], right) if isinstance(right, str) else ASTNode(DGM_MAP["VALUE"], right)
        ])
    return ASTNode(DGM_MAP["VAR"], left)

def parse_print(self):
    self.eat("PRINT")
    self.eat("SYMBOL")  # (
    expr = self.parse_expr()
    self.eat("SYMBOL")  # )
    return ASTNode(DGM_MAP["FLOW"], "print", [expr])

# parser.py — extended arithmetic

def parse_expr(self):
    # Pratt/recursive descent (simple for now: left-assoc, same precedence)
    node = self.parse_term()
    while self.peek()[0] == "OP" and self.peek()[1] in ["+", "-"]:
        op = self.eat("OP")[1]
        right = self.parse_term()
        node = ASTNode(DGM_MAP["EXPR"], op, [node, right])
    return node

def parse_term(self):
    node = self.parse_factor()
    while self.peek()[0] == "OP" and self.peek()[1] in ["*", "/"]:
        op = self.eat("OP")[1]
        right = self.parse_factor()
        node = ASTNode(DGM_MAP["EXPR"], op, [node, right])
    return node

def parse_factor(self):
    kind, val = self.peek()
    if kind == "ID":
        _, name = self.eat("ID")
        return ASTNode(DGM_MAP["VAR"], name)
    elif kind == "NUMBER":
        _, num = self.eat("NUMBER")
        return ASTNode(DGM_MAP["VALUE"], num)
    else:
        raise SyntaxError(f"Unexpected token {self.peek()}")

