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
    elif kind == "ID":
        # peek ahead for assignment
        if self.tokens[self.pos+1][0] == "SYMBOL" and self.tokens[self.pos+1][1] == "[":
            # arr[index] = expr
            name = self.eat("ID")[1]
            self.eat("SYMBOL")  # [
            index_expr = self.parse_expr()
            self.eat("SYMBOL")  # ]
            self.eat("OP")      # =
            value_expr = self.parse_expr()
            return ASTNode(DGM_MAP["ASSIGN"], name, [index_expr, value_expr])
        elif self.tokens[self.pos+1][0] == "OP" and self.tokens[self.pos+1][1] == "=":
            # x = expr
            name = self.eat("ID")[1]
            self.eat("OP")
            value_expr = self.parse_expr()
            return ASTNode(DGM_MAP["ASSIGN"], name, [value_expr])
        elif self.tokens[self.pos+1][0] == "SYMBOL" and self.tokens[self.pos+1][1] == "(":
            return self.parse_func_call()
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_factor(self):
    kind, val = self.peek()
    if kind == "ID":
        _, name = self.eat("ID")
        if self.peek()[1] == ".":
            self.eat("SYMBOL")
            _, field = self.eat("ID")
            return ASTNode(DGM_MAP["FIELD"], (name, field))
        elif self.peek()[1] == "[":
            self.eat("SYMBOL")  # [
            index_expr = self.parse_expr()
            self.eat("SYMBOL")  # ]
            return ASTNode(DGM_MAP["INDEX"], name, [index_expr])
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

def parse_factor(self):
    kind, val = self.peek()
    if kind == "ID":
        _, name = self.eat("ID")
        node = ASTNode(DGM_MAP["VAR"], name)
        # handle chained indexing
        while self.peek()[1] == "[":
            self.eat("SYMBOL")  # [
            index_expr = self.parse_expr()
            self.eat("SYMBOL")  # ]
            node = ASTNode(DGM_MAP["INDEX"], None, [node, index_expr])
        return node
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
    elif kind == "BREAK":
        self.eat("BREAK")
        return ASTNode(DGM_MAP["BREAK"], None)
    elif kind == "CONTINUE":
        self.eat("CONTINUE")
        return ASTNode(DGM_MAP["CONTINUE"], None)
    elif kind == "ID":
        if self.tokens[self.pos+1][0] == "SYMBOL" and self.tokens[self.pos+1][1] == "(":
            return self.parse_func_call()
        # ... assignment already handled above
    else:
        raise SyntaxError(f"Unknown stmt {kind}")

def parse_stmt(self):
    kind, _ = self.peek()
    if kind == "SWITCH":
        return self.parse_switch()
    elif kind == "CASE":
        return self.parse_case()
    elif kind == "DEFAULT":
        return self.parse_default()
    elif kind == "ID":
        # check for field mutation like p.x = expr
        if self.tokens[self.pos+1][1] == ".":
            base = self.eat("ID")[1]
            self.eat("SYMBOL")  # .
            field = self.eat("ID")[1]
            self.eat("OP")      # =
            value_expr = self.parse_expr()
            return ASTNode(DGM_MAP["FIELD_ASSIGN"], (base, field), [value_expr])
        # fallback to normal assignment/call
    return super().parse_stmt()

def parse_switch(self):
    self.eat("SWITCH")
    expr = self.parse_expr()
    self.eat("SYMBOL")  # {
    cases = []
    default_block = None
    while self.peek()[0] != "SYMBOL" or self.peek()[1] != "}":
        if self.peek()[0] == "CASE":
            cases.append(self.parse_case())
        elif self.peek()[0] == "DEFAULT":
            default_block = self.parse_default()
        else:
            raise SyntaxError(f"Unexpected in switch: {self.peek()}")
    self.eat("SYMBOL")  # }
    return ASTNode(DGM_MAP["SWITCH"], expr, cases + ([default_block] if default_block else []))

def parse_case(self):
    self.eat("CASE")
    match_expr = self.parse_expr()
    block = self.parse_block()
    return ASTNode(DGM_MAP["CASE"], match_expr, [block])

def parse_default(self):
    self.eat("DEFAULT")
    block = self.parse_block()
    return ASTNode(DGM_MAP["DEFAULT"], None, [block])

def parse_switch(self):
    self.eat("SWITCH")
    expr = self.parse_expr()
    self.eat("SYMBOL")  # {
    cases = []
    default_block = None
    while self.peek()[1] != "}":
        if self.peek()[0] == "CASE":
            cases.append(self.parse_case())
        elif self.peek()[0] == "DEFAULT":
            default_block = self.parse_default()
        else:
            raise SyntaxError(f"Unexpected in switch: {self.peek()}")
    self.eat("SYMBOL")  # }
    return ASTNode(DGM_MAP["SWITCH"], expr, cases + ([default_block] if default_block else []))

def parse_case(self):
    self.eat("CASE")
    pattern = self.parse_pattern()
    block = self.parse_block()
    return ASTNode(DGM_MAP["CASE"], None, [pattern, block])

def parse_pattern(self):
    # tuple pattern: (a, b)
    if self.peek()[1] == "(":
        self.eat("SYMBOL")
        elems = []
        while self.peek()[1] != ")":
            elems.append(self.parse_pattern())
            if self.peek()[1] == ",":
                self.eat("SYMBOL")
        self.eat("SYMBOL")
        return ASTNode(DGM_MAP["PATTERN"], "tuple", elems)
    # range pattern: 1 .. 5
    elif self.peek()[0] == "NUMBER":
        _, start = self.eat("NUMBER")
        if self.peek()[1] == "..":
            self.eat("OP")
            _, end = self.eat("NUMBER")
            return ASTNode(DGM_MAP["PATTERN"], "range", [ASTNode(DGM_MAP["VALUE"], start), ASTNode(DGM_MAP["VALUE"], end)])
        return ASTNode(DGM_MAP["VALUE"], start)
    # wildcard
    elif self.peek()[0] == "UNDERSCORE":
        self.eat("UNDERSCORE")
        return ASTNode(DGM_MAP["PATTERN"], "wildcard")
    # identifier
    elif self.peek()[0] == "ID":
        _, name = self.eat("ID")
        return ASTNode(DGM_MAP["PATTERN"], name)
    else:
        raise SyntaxError(f"Unexpected pattern token {self.peek()}")

def parse_struct(self):
    self.eat("STRUCT")
    _, name = self.eat("ID")
    self.eat("SYMBOL")  # {
    fields, methods = [], []
    while self.peek()[1] != "}":
        if self.peek()[0] == "LET":
            fields.append(self.parse_let())
        elif self.peek()[0] == "FLOW":
            methods.append(self.parse_method_def(name))
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["STRUCT"], name, fields + methods)

def parse_method_def(self, struct_name):
    self.eat("FLOW")
    _, mname = self.eat("ID")
    self.eat("SYMBOL")  # (
    params = []
    while self.peek()[1] != ")":
        _, pname = self.eat("ID")
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
        params.append(pname)
    self.eat("SYMBOL")  # )
    block = self.parse_block()
    return ASTNode(DGM_MAP["METHOD_DEF"], (struct_name, mname), [ASTNode("params", params), block])

def parse_method_call(self, base):
    self.eat("SYMBOL")  # .
    _, mname = self.eat("ID")
    self.eat("SYMBOL")  # (
    args = []
    while self.peek()[1] != ")":
        args.append(self.parse_expr())
        if self.peek()[1] == ",":
            self.eat("SYMBOL")
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["METHOD_CALL"], (base, mname), args)

def parse_pattern(self):
    if self.peek()[1] == "(":
        self.eat("SYMBOL")
        elems = []
        while self.peek()[1] != ")":
            elems.append(self.parse_pattern())
            if self.peek()[1] == ",":
                self.eat("SYMBOL")
        self.eat("SYMBOL")
        return ASTNode(DGM_MAP["PATTERN"], "tuple", elems)

    elif self.peek()[0] == "ID":
        # could be struct pattern
        _, name = self.eat("ID")
        if self.peek()[1] == "(":
            self.eat("SYMBOL")
            fields = []
            while self.peek()[1] != ")":
                fields.append(self.parse_pattern())
                if self.peek()[1] == ",":
                    self.eat("SYMBOL")
            self.eat("SYMBOL")
            return ASTNode(DGM_MAP["PATTERN"], ("struct", name), fields)
        return ASTNode(DGM_MAP["PATTERN"], name)

    elif self.peek()[0] == "NUMBER":
        _, num = self.eat("NUMBER")
        return ASTNode(DGM_MAP["VALUE"], num)

    elif self.peek()[0] == "UNDERSCORE":
        self.eat("UNDERSCORE")
        return ASTNode(DGM_MAP["PATTERN"], "wildcard")

    else:
        raise SyntaxError(f"Unexpected pattern {self.peek()}")

def parse_trait(self):
    self.eat("TRAIT")
    _, tname = self.eat("ID")
    self.eat("SYMBOL")  # {
    methods = []
    while self.peek()[1] != "}":
        self.eat("FLOW")
        _, mname = self.eat("ID")
        self.eat("SYMBOL")  # ()
        self.eat("SYMBOL")  # )
        methods.append(mname)
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["TRAIT_DEF"], tname, methods)

def parse_impl(self):
    self.eat("IMPL")
    _, sname = self.eat("ID")
    _, tname = self.eat("ID")
    self.eat("SYMBOL")  # {
    methods = []
    while self.peek()[1] != "}":
        methods.append(self.parse_method_def(sname))
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["TRAIT_IMPL"], (sname, tname), methods)

def parse_let(self):
    self.eat("LET")
    if self.peek()[1] == "(":
        # tuple destructure
        self.eat("SYMBOL")
        names = []
        while self.peek()[1] != ")":
            _, n = self.eat("ID")
            names.append(n)
            if self.peek()[1] == ",":
                self.eat("SYMBOL")
        self.eat("SYMBOL")
        self.eat("OP")  # =
        expr = self.parse_expr()
        return ASTNode(DGM_MAP["DESTRUCT"], names, [expr])
    elif self.peek()[0] == "ID":
        _, name = self.eat("ID")
        if self.peek()[1] == "(":
            # struct destructure like Person(name, age)
            struct_name = name
            self.eat("SYMBOL")
            fields = []
            while self.peek()[1] != ")":
                _, fname = self.eat("ID")
                fields.append(fname)
                if self.peek()[1] == ",":
                    self.eat("SYMBOL")
            self.eat("SYMBOL")
            self.eat("OP")
            expr = self.parse_expr()
            return ASTNode(DGM_MAP["DESTRUCT"], (struct_name, fields), [expr])
        else:
            _, typ = self.eat("ID") if self.peek()[0] == "ID" else (None, None)
            self.eat("OP")
            expr = self.parse_expr()
            return ASTNode(DGM_MAP["VAR"], (name, typ), [expr])

def parse_trait(self):
    self.eat("TRAIT")
    _, tname = self.eat("ID")
    parent = None
    if self.peek()[0] == "EXTENDS":
        self.eat("EXTENDS")
        _, parent = self.eat("ID")
    self.eat("SYMBOL")  # {
    methods = []
    while self.peek()[1] != "}":
        self.eat("FLOW")
        _, mname = self.eat("ID")
        self.eat("SYMBOL")  # ()
        self.eat("SYMBOL")  # )
        methods.append(mname)
    self.eat("SYMBOL")
    return ASTNode(DGM_MAP["TRAIT_DEF"], (tname, parent), methods)

def parse_pattern(self):
    if self.peek()[0] == "ID":
        _, name = self.eat("ID")
        if self.peek()[1] == "(":
            self.eat("SYMBOL")
            fields = []
            while self.peek()[1] != ")":
                if self.peek()[0] == "ID":
                    _, fname = self.eat("ID")
                    fields.append(ASTNode(DGM_MAP["PATTERN"], fname))
                elif self.peek()[0] == "UNDERSCORE":
                    self.eat("UNDERSCORE")
                    fields.append(ASTNode(DGM_MAP["PATTERN"], "wildcard"))
                else:
                    fields.append(self.parse_pattern())
                if self.peek()[1] == ",":
                    self.eat("SYMBOL")
            self.eat("SYMBOL")
            return ASTNode(DGM_MAP["PATTERN"], ("struct", name), fields)
        else:
            return ASTNode(DGM_MAP["PATTERN"], name)
    return super().parse_pattern()

