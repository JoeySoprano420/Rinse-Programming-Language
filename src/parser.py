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
