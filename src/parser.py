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

def parse_let(self):
    self.eat("LET")
    _, name = self.eat("ID")
    self.eat("SYMBOL")  # :
    _, typ = self.eat("ID")
    self.eat("OP")  # =
    expr = self.parse_expr()   # <-- instead of just NUMBER
    return ASTNode(DGM_MAP["VAR"], (name, typ), [expr])

def parse_if(self):
    self.eat("IF")
    cond = self.parse_expr()
    block = self.parse_block()
    else_block = None
    if self.peek()[0] == "ELSE":
        self.eat("ELSE")
        else_block = self.parse_block()
    return ASTNode(DGM_MAP["IF"], None, [cond, block, else_block])

def parse_stmt(self):
    kind, _ = self.peek()
    if kind == "LET":
        return self.parse_let()
    elif kind == "PRINT":
        return self.parse_print()
    elif kind == "IF":
        return self.parse_if()
    elif kind == "STRUCT":
        return self.parse_struct()
    elif kind == "TUPLE":
        return self.parse_tuple()
    elif kind == "LIST":
        return self.parse_list()
    elif kind == "ARRAY":
        return self.parse_array()
    elif kind == "PROOF":
        return self.parse_proof()
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_if(self):
    self.eat("IF")
    cond = self.parse_expr()
    block = self.parse_block()
    else_block = None
    if self.peek()[0] == "ELSE":
        self.eat("ELSE")
        else_block = self.parse_block()
    return ASTNode(DGM_MAP["IF"], None, [cond, block, else_block])

def parse_struct(self):
    self.eat("STRUCT")
    _, name = self.eat("ID")
    block = self.parse_block()
    return ASTNode(DGM_MAP["STRUCT"], name, [block])

def parse_tuple(self):
    self.eat("TUPLE")
    self.eat("SYMBOL")  # (
    values = []
    while self.peek()[1] != ")":
        expr = self.parse_expr()
        values.append(expr)
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
    self.eat("SYMBOL")  # )
    return ASTNode(DGM_MAP["TUPLE"], None, values)

def parse_list(self):
    self.eat("LIST")
    self.eat("SYMBOL")
    values = []
    while self.peek()[1] != ")":
        expr = self.parse_expr()
        values.append(expr)
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["LIST"], None, values)

def parse_array(self):
    self.eat("ARRAY")
    self.eat("SYMBOL")
    values = []
    while self.peek()[1] != ")":
        expr = self.parse_expr()
        values.append(expr)
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["ARRAY"], None, values)

def parse_proof(self):
    self.eat("PROOF")
    cond = self.parse_expr()
    block = self.parse_block()
    return ASTNode(DGM_MAP["PROOF"], None, [cond, block])

def parse_stmt(self):
    kind, _ = self.peek()
    if kind == "LET":
        return self.parse_let()
    elif kind == "PRINT":
        return self.parse_print()
    elif kind == "IF":
        return self.parse_if()
    elif kind == "FOR":
        return self.parse_for()
    elif kind == "WHILE":
        return self.parse_while()
    elif kind == "NEST":
        return self.parse_nest()
    elif kind == "STRUCT":
        return self.parse_struct()
    elif kind == "TUPLE":
        return self.parse_tuple()
    elif kind == "LIST":
        return self.parse_list()
    elif kind == "ARRAY":
        return self.parse_array()
    elif kind == "PROOF":
        return self.parse_proof()
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_for(self):
    self.eat("FOR")
    _, var = self.eat("ID")
    self.eat("IN")
    start = self.parse_expr()
    self.eat("OP")  # ..
    end = self.parse_expr()
    block = self.parse_block()
    return ASTNode(DGM_MAP["FOR"], var, [start, end, block])

def parse_while(self):
    self.eat("WHILE")
    cond = self.parse_expr()
    block = self.parse_block()
    return ASTNode(DGM_MAP["WHILE"], None, [cond, block])

def parse_nest(self):
    self.eat("NEST")
    block = self.parse_block()
    return ASTNode(DGM_MAP["NEST"], None, [block])

def parse_stmt(self):
    kind, _ = self.peek()
    if kind == "LET":
        return self.parse_let()
    elif kind == "PRINT":
        return self.parse_print()
    elif kind == "IF":
        return self.parse_if()
    elif kind == "FOR":
        return self.parse_for()
    elif kind == "WHILE":
        return self.parse_while()
    elif kind == "NEST":
        return self.parse_nest()
    elif kind == "FLOW":
        return self.parse_func_def()
    elif kind == "ID" and self.tokens[self.pos+1][0] == "SYMBOL" and self.tokens[self.pos+1][1] == "(":
        return self.parse_func_call()
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_func_def(self):
    self.eat("FLOW")
    _, name = self.eat("ID")
    self.eat("SYMBOL")  # (
    params = []
    while self.peek()[1] != ")":
        _, pname = self.eat("ID")
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
        params.append(pname)
    self.eat("SYMBOL")  # )
    block = self.parse_block()
    return ASTNode(DGM_MAP["FUNC_DEF"], name, [ASTNode("params", params), block])

def parse_func_call(self):
    _, name = self.eat("ID")
    self.eat("SYMBOL")  # (
    args = []
    while self.peek()[1] != ")":
        args.append(self.parse_expr())
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["FUNC_CALL"], name, args)

def parse_factor(self):
    kind, val = self.peek()
    if kind == "ID":
        _, name = self.eat("ID")
        # field access like p.x
        if self.peek()[1] == ".":
            self.eat("SYMBOL")
            _, field = self.eat("ID")
            return ASTNode(DGM_MAP["FIELD"], (name, field))
        return ASTNode(DGM_MAP["VAR"], name)
    elif kind == "NUMBER":
        _, num = self.eat("NUMBER")
        return ASTNode(DGM_MAP["VALUE"], num)
    else:
        raise SyntaxError(f"Unexpected token {self.peek()}")

def parse_stmt(self):
    kind, _ = self.peek()
    if kind == "LET":
        return self.parse_let()
    elif kind == "PRINT":
        return self.parse_print()
    elif kind == "IF":
        return self.parse_if()
    elif kind == "FOR":
        return self.parse_for()
    elif kind == "WHILE":
        return self.parse_while()
    elif kind == "NEST":
        return self.parse_nest()
    elif kind == "FLOW":
        return self.parse_func_def()
    elif kind == "RETURN":
        return self.parse_return()
    elif kind == "ID" and self.tokens[self.pos+1][0] == "SYMBOL" and self.tokens[self.pos+1][1] == "(":
        return self.parse_func_call()
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_return(self):
    self.eat("RETURN")
    expr = self.parse_expr()
    return ASTNode(DGM_MAP["RETURN"], None, [expr])

def parse_expr(self):
    node = self.parse_term()
    while self.peek()[0] == "OP" or self.peek()[0] in ["AND", "OR"]:
        if self.peek()[0] == "OP" and self.peek()[1] in ["+", "-", "<", ">", "<=", ">=", "==", "!="]:
            op = self.eat("OP")[1]
            right = self.parse_term()
            node = ASTNode(DGM_MAP["EXPR"], op, [node, right])
        elif self.peek()[0] == "AND":
            self.eat("AND")
            right = self.parse_term()
            node = ASTNode(DGM_MAP["EXPR"], "and", [node, right])
        elif self.peek()[0] == "OR":
            self.eat("OR")
            right = self.parse_term()
            node = ASTNode(DGM_MAP["EXPR"], "or", [node, right])
    return node

def parse_factor(self):
    kind, val = self.peek()
    if kind == "ID":
        _, name = self.eat("ID")
        if self.peek()[1] == ".":
            self.eat("SYMBOL")
            _, field = self.eat("ID")
            return ASTNode(DGM_MAP["FIELD"], (name, field))
        return ASTNode(DGM_MAP["VAR"], name)
    elif kind == "NUMBER":
        _, num = self.eat("NUMBER")
        return ASTNode(DGM_MAP["VALUE"], num)
    elif kind == "TRUE":
        self.eat("TRUE")
        return ASTNode(DGM_MAP["BOOL"], True)
    elif kind == "FALSE":
        self.eat("FALSE")
        return ASTNode(DGM_MAP["BOOL"], False)
    elif kind == "NOT":
        self.eat("NOT")
        expr = self.parse_factor()
        return ASTNode(DGM_MAP["EXPR"], "not", [expr])
    else:
        raise SyntaxError(f"Unexpected token {self.peek()}")

