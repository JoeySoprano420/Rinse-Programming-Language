# vese.py — VESE Runtime
# Simulates NASM-like execution in a sandboxed VM

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []

    def exec(self, program):
        for line in program.splitlines():
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("section") or line.startswith("global"):
                continue

            parts = line.split()
            op = parts[0]

            if op == "mov":
                reg, val = parts[1].split(",")[0], parts[1].split(",")[1] if "," in parts[1] else parts[1]
                if "," in line:
                    reg, val = parts[1].strip(","), parts[2]
                self.registers[reg] = int(val)

            elif op == "add":
                reg1 = parts[1].strip(",")
                reg2 = parts[2]
                self.registers[reg1] += self.registers.get(reg2, int(reg2))

            elif op == "push":
                reg = parts[1]
                self.stack.append(self.registers[reg])

            elif op == "call" and parts[1] == "print_int":
                val = self.stack.pop()
                print(val)

            elif op == "xor":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] = self.registers[reg1] ^ self.registers[reg2]

            elif op == "ret":
                return 0

# vese.py — VESE Runtime (extended for add ops)

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []

    def exec(self, program):
        for line in program.splitlines():
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("section") or line.startswith("global"):
                continue

            parts = line.split()
            op = parts[0]

            if op == "mov":
                reg, val = parts[1].strip(","), parts[2]
                self.registers[reg] = self.registers.get(val, int(val)) if val in self.registers else int(val)

            elif op == "add":
                reg1 = parts[1].strip(",")
                reg2 = parts[2]
                if reg2 in self.registers:
                    self.registers[reg1] += self.registers[reg2]
                else:
                    self.registers[reg1] += int(reg2)

            elif op == "push":
                reg = parts[1]
                self.stack.append(self.registers[reg])

            elif op == "call" and parts[1] == "print_int":
                val = self.stack.pop()
                print(val)

            elif op == "xor":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] = self.registers[reg1] ^ self.registers[reg2]

            elif op == "ret":
                return 0

# vese.py — extended arithmetic runtime

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []

    def exec(self, program):
        for line in program.splitlines():
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("section") or line.startswith("global"):
                continue

            parts = line.split()
            op = parts[0]

            if op == "mov":
                reg, val = parts[1].strip(","), parts[2]
                self.registers[reg] = self.registers.get(val, int(val)) if val in self.registers else int(val)

            elif op == "add":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] += self.registers.get(reg2, int(reg2))

            elif op == "sub":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] -= self.registers.get(reg2, int(reg2))

            elif op == "imul":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] *= self.registers.get(reg2, int(reg2))

            elif op == "idiv":
                reg = parts[1]
                divisor = self.registers.get(reg, int(reg))
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero in VESE")
                self.registers["eax"] //= divisor
                self.registers["edx"] = self.registers["eax"] % divisor

            elif op == "push":
                reg = parts[1]
                self.stack.append(self.registers[reg])

            elif op == "pop":
                reg = parts[1]
                self.registers[reg] = self.stack.pop()

            elif op == "call" and parts[1] == "print_int":
                val = self.stack.pop()
                print(val)

            elif op == "xor":
                reg1, reg2 = parts[1].strip(","), parts[2]
                self.registers[reg1] = self.registers[reg1] ^ self.registers[reg2]

            elif op == "ret":
                return 0

# vese.py — VESE Runtime (full execution engine)

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []
        self.flags = {"cmp": 0}
        self.labels = {}
        self.pc = 0
        self.program = []
        self.heap = {}   # store structs, tuples, lists, arrays

    def load(self, nasm_code: str):
        """Preprocess NASM-like code into instructions and labels."""
        self.program = []
        self.labels = {}
        for i, line in enumerate(nasm_code.splitlines()):
            line = line.strip()
            if not line or line.startswith("section") or line.startswith("global"):
                continue
            if line.endswith(":"):  # label
                self.labels[line[:-1]] = len(self.program)
            else:
                self.program.append(line)

    def run(self):
        """Run program from start to end."""
        self.pc = 0
        while self.pc < len(self.program):
            line = self.program[self.pc]
            self.exec(line)
            self.pc += 1

    def exec(self, line: str):
        parts = line.split()
        op = parts[0]

        if op == "mov":
            reg, val = parts[1].strip(","), parts[2]
            self.registers[reg] = self.registers.get(val, int(val)) if val in self.registers else int(val)

        elif op == "add":
            r1, r2 = parts[1].strip(","), parts[2]
            self.registers[r1] += self.registers.get(r2, int(r2))

        elif op == "sub":
            r1, r2 = parts[1].strip(","), parts[2]
            self.registers[r1] -= self.registers.get(r2, int(r2))

        elif op == "imul":
            r1, r2 = parts[1].strip(","), parts[2]
            self.registers[r1] *= self.registers.get(r2, int(r2))

        elif op == "idiv":
            r = parts[1]
            divisor = self.registers.get(r, int(r))
            if divisor == 0:
                raise ZeroDivisionError("Division by zero in VESE")
            self.registers["eax"] //= divisor
            self.registers["edx"] = self.registers["eax"] % divisor

        elif op == "cmp":
            r1, r2 = parts[1].strip(","), parts[2]
            v1 = self.registers.get(r1, int(r1))
            v2 = self.registers.get(r2, int(r2))
            self.flags["cmp"] = v1 - v2

        elif op == "je":
            lbl = parts[1]
            if self.flags["cmp"] == 0:
                self.pc = self.labels[lbl] - 1

        elif op == "jne":
            lbl = parts[1]
            if self.flags["cmp"] != 0:
                self.pc = self.labels[lbl] - 1

        elif op == "jg":
            lbl = parts[1]
            if self.flags["cmp"] > 0:
                self.pc = self.labels[lbl] - 1

        elif op == "jl":
            lbl = parts[1]
            if self.flags["cmp"] < 0:
                self.pc = self.labels[lbl] - 1

        elif op == "push":
            reg = parts[1]
            self.stack.append(self.registers[reg])

        elif op == "pop":
            reg = parts[1]
            self.registers[reg] = self.stack.pop()

        elif op == "call":
            fn = parts[1]
            if fn == "print_int":
                val = self.stack.pop()
                print(val)
            elif fn == "print_str":
                val = self.stack.pop()
                print(str(val))

        elif op == "xor":
            r1, r2 = parts[1].strip(","), parts[2]
            self.registers[r1] = self.registers[r1] ^ self.registers[r2]

        elif op == "pow":
            base, exp = self.registers["eax"], self.registers["ebx"]
            self.registers["eax"] = pow(base, exp)

        elif op == "make_tuple":
            count = int(parts[1])
            elems = [self.stack.pop() for _ in range(count)][::-1]
            tup = tuple(elems)
            self.stack.append(tup)
            print(tup)

        elif op == "make_list":
            count = int(parts[1])
            elems = [self.stack.pop() for _ in range(count)][::-1]
            lst = list(elems)
            self.stack.append(lst)
            print(lst)

        elif op == "make_array":
            count = int(parts[1])
            elems = [self.stack.pop() for _ in range(count)][::-1]
            arr = elems
            self.stack.append(arr)
            print(arr)

        elif op == "make_struct":
            name = parts[1]

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []
        self.flags = {"cmp": 0}
        self.labels = {}
        self.pc = 0
        self.program = []
        self.heap = {}
        self.scope_stack = [{}]  # nested scopes for vars

    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        self.scope_stack.pop()

    def set_var(self, name, val):
        self.scope_stack[-1][name] = val

    def get_var(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable {name} not found")

    def exec(self, line: str):
        parts = line.split()
        op = parts[0]

        # [existing ops...]

        elif op == "inc":
            reg = parts[1]
            self.registers[reg] += 1

        elif op == "dec":
            reg = parts[1]
            self.registers[reg] -= 1

        elif op == "scope_push":
            self.push_scope()

        elif op == "scope_pop":
            self.pop_scope()

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []
        self.call_stack = []
        self.functions = {}
        self.heap = {}
        self.scope_stack = [{}]

    def push_scope(self):
        self.scope_stack.append({})
    def pop_scope(self):
        self.scope_stack.pop()
    def set_var(self, name, val):
        self.scope_stack[-1][name] = val
    def get_var(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable {name} not found")

    def define_func(self, name, params, block):
        self.functions[name] = (params, block)

    def call_func(self, name, args):
        params, block = self.functions[name]
        self.push_scope()
        for p, a in zip(params, args):
            self.set_var(p, a)
        result = None
        for stmt in block:
            result = self.exec_stmt(stmt)
        self.pop_scope()
        return result

    def exec_stmt(self, stmt):
        if stmt["type"] == "print":
            val = self.eval_expr(stmt["expr"])
            print(val)
        elif stmt["type"] == "let":
            self.set_var(stmt["name"], self.eval_expr(stmt["expr"]))
        elif stmt["type"] == "func_def":
            self.define_func(stmt["name"], stmt["params"], stmt["block"])
        elif stmt["type"] == "func_call":
            return self.call_func(stmt["name"], [self.eval_expr(a) for a in stmt["args"]])
        elif stmt["type"] == "field":
            obj, field = stmt["base"], stmt["field"]
            return self.heap[obj][field]

    def eval_expr(self, expr):
        if expr["type"] == "var":
            return self.get_var(expr["name"])
        elif expr["type"] == "value":
            return expr["val"]
        elif expr["type"] == "field":
            return self.exec_stmt(expr)
        elif expr["type"] == "binop":
            l = self.eval_expr(expr["left"])
            r = self.eval_expr(expr["right"])
            if expr["op"] == "+": return l + r
            if expr["op"] == "-": return l - r
            if expr["op"] == "*": return l * r
            if expr["op"] == "/": return l // r

class VESE:
    def __init__(self):
        self.registers = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
        self.stack = []
        self.call_stack = []
        self.functions = {}    # name -> (params, block)
        self.heap = {}
        self.scope_stack = [{}]
        self.return_flag = False
        self.return_value = None

    def push_scope(self): self.scope_stack.append({})
    def pop_scope(self): self.scope_stack.pop()

    def set_var(self, name, val): self.scope_stack[-1][name] = val
    def get_var(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope: return scope[name]
        raise NameError(f"Variable {name} not found")

    def define_func(self, name, params, block):
        self.functions[name] = (params, block)

    def call_func(self, name, args):
        if name not in self.functions:
            raise NameError(f"Function {name} not defined")
        params, block = self.functions[name]
        self.push_scope()
        for p, a in zip(params.value, args):
            self.set_var(p, self.eval_expr(a))
        self.return_flag = False
        self.return_value = None
        for stmt in block.children:
            self.exec_stmt(stmt)
            if self.return_flag:
                break
        self.pop_scope()
        return self.return_value

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["VAR"]:
            name, _ = stmt.value
            self.set_var(name, self.eval_expr(stmt.children[0]))
        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            print(self.eval_expr(stmt.children[0]))
        elif stmt.tag == DGM_MAP["FUNC_DEF"]:
            params, block = stmt.children
            self.define_func(stmt.value, params, block)
        elif stmt.tag == DGM_MAP["FUNC_CALL"]:
            return self.call_func(stmt.value, stmt.children)
        elif stmt.tag == DGM_MAP["RETURN"]:
            self.return_value = self.eval_expr(stmt.children[0])
            self.return_flag = True
        elif stmt.tag == DGM_MAP["IF"]:
            cond, then_block, else_block = stmt.children
            if self.eval_expr(cond):
                for s in then_block.children:
                    self.exec_stmt(s)
                    if self.return_flag: break
            elif else_block:
                for s in else_block.children:
                    self.exec_stmt(s)
                    if self.return_flag: break

    def eval_expr(self, expr):
        if expr.tag == DGM_MAP["VAR"]:
            return self.get_var(expr.value)
        elif expr.tag == DGM_MAP["VALUE"]:
            return expr.value
        elif expr.tag == DGM_MAP["EXPR"]:
            left, right = expr.children
            l = self.eval_expr(left)
            r = self.eval_expr(right)
            if expr.value == "+": return l + r
            if expr.value == "-": return l - r
            if expr.value == "*": return l * r
            if expr.value == "/": return l // r
            if expr.value == "<": return int(l < r)
            if expr.value == "<=": return int(l <= r)
            if expr.value == ">": return int(l > r)
            if expr.value == ">=": return int(l >= r)
            if expr.value == "==": return int(l == r)
            if expr.value == "!=": return int(l != r)
        elif expr.tag == DGM_MAP["FUNC_CALL"]:
            return self.call_func(expr.value, expr.children)

class VESE:
    def __init__(self):
        self.scope_stack = [{}]
        self.functions = {}
        self.return_flag = False
        self.return_value = None

    def push_scope(self): self.scope_stack.append({})
    def pop_scope(self): self.scope_stack.pop()
    def set_var(self, name, val): self.scope_stack[-1][name] = val
    def get_var(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope: return scope[name]
        raise NameError(f"Variable {name} not found")

    def define_func(self, name, params, block):
        self.functions[name] = (params, block)

    def call_func(self, name, args):
        if name not in self.functions:
            raise NameError(f"Function {name} not defined")
        params, block = self.functions[name]
        self.push_scope()
        for p, a in zip(params.value, args):
            self.set_var(p, self.eval_expr(a))
        self.return_flag = False
        self.return_value = None
        for stmt in block.children:
            self.exec_stmt(stmt)
            if self.return_flag:
                break
        self.pop_scope()
        return self.return_value

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["VAR"]:
            name, _ = stmt.value
            self.set_var(name, self.eval_expr(stmt.children[0]))
        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            print(self.eval_expr(stmt.children[0]))
        elif stmt.tag == DGM_MAP["FUNC_DEF"]:
            params, block = stmt.children
            self.define_func(stmt.value, params, block)
        elif stmt.tag == DGM_MAP["FUNC_CALL"]:
            return self.call_func(stmt.value, stmt.children)
        elif stmt.tag == DGM_MAP["RETURN"]:
            self.return_value = self.eval_expr(stmt.children[0])
            self.return_flag = True
        elif stmt.tag == DGM_MAP["STRUCT"]:
            struct_name = stmt.value
            fields = {}
            for field in stmt.children[0].children:
                fname, _ = field.value
                fields[fname] = self.eval_expr(field.children[0])
            self.set_var(struct_name, fields)
        elif stmt.tag == DGM_MAP["PROOF"]:
            cond, block = stmt.children
            if not self.eval_expr(cond):
                raise AssertionError("Proof failed in VESE")
            for s in block.children:
                self.exec_stmt(s)

    def eval_expr(self, expr):
        if expr.tag == DGM_MAP["VAR"]:
            return self.get_var(expr.value)
        elif expr.tag == DGM_MAP["VALUE"]:
            return expr.value
        elif expr.tag == DGM_MAP["BOOL"]:
            return expr.value
        elif expr.tag == DGM_MAP["FIELD"]:
            base, field = expr.value
            obj = self.get_var(base)
            return obj[field] if isinstance(obj, dict) else obj[int(field)]
        elif expr.tag == DGM_MAP["TUPLE"]:
            return tuple(self.eval_expr(e) for e in expr.children)
        elif expr.tag == DGM_MAP["LIST"]:
            return [self.eval_expr(e) for e in expr.children]
        elif expr.tag == DGM_MAP["ARRAY"]:
            return [self.eval_expr(e) for e in expr.children]
        elif expr.tag == DGM_MAP["FUNC_CALL"]:
            return self.call_func(expr.value, expr.children)
        elif expr.tag == DGM_MAP["EXPR"]:
            op = expr.value
            if op == "not":
                return not self.eval_expr(expr.children[0])
            left = self.eval_expr(expr.children[0])
            right = self.eval_expr(expr.children[1])
            if op == "+": return left + right
            if op == "-": return left - right
            if op == "*": return left * right
            if op == "/": return left // right
            if op == "and": return left and right
            if op == "or": return left or right
            if op == "<": return left < right
            if op == "<=": return left <= right
            if op == ">": return left > right
            if op == ">=": return left >= right
            if op == "==": return left == right
            if op == "!=": return left != right

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["VAR"]:
        name, _ = stmt.value
        self.set_var(name, self.eval_expr(stmt.children[0]))
    elif stmt.tag == DGM_MAP["ASSIGN"]:
        if len(stmt.children) == 1:
            # simple assignment x = expr
            value = self.eval_expr(stmt.children[0])
            self.set_var(stmt.value, value)
        else:
            # arr[index] = expr
            index = self.eval_expr(stmt.children[0])
            value = self.eval_expr(stmt.children[1])
            arr = self.get_var(stmt.value)
            if not isinstance(arr, list):
                raise TypeError(f"{stmt.value} is not indexable")
            arr[index] = value
            self.set_var(stmt.value, arr)
    elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
        print(self.eval_expr(stmt.children[0]))
    # ... keep the rest as before

def eval_expr(self, expr):
    if expr.tag == DGM_MAP["VAR"]:
        return self.get_var(expr.value)
    elif expr.tag == DGM_MAP["VALUE"]:
        return expr.value
    elif expr.tag == DGM_MAP["BOOL"]:
        return expr.value
    elif expr.tag == DGM_MAP["INDEX"]:
        arr = self.get_var(expr.value)
        idx = self.eval_expr(expr.children[0])
        return arr[idx]
    elif expr.tag == DGM_MAP["TUPLE"]:
        return tuple(self.eval_expr(e) for e in expr.children)
    elif expr.tag == DGM_MAP["LIST"]:
        return [self.eval_expr(e) for e in expr.children]
    elif expr.tag == DGM_MAP["ARRAY"]:
        return [self.eval_expr(e) for e in expr.children]
    elif expr.tag == DGM_MAP["EXPR"]:
        op = expr.value
        if op == "not":
            return not self.eval_expr(expr.children[0])
        l = self.eval_expr(expr.children[0])
        r = self.eval_expr(expr.children[1])
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l // r
        if op == "and": return l and r
        if op == "or": return l or r
        if op == "<": return l < r
        if op == "<=": return l <= r
        if op == ">": return l > r
        if op == ">=": return l >= r
        if op == "==": return l == r
        if op == "!=": return l != r

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["VAR"]:
        name, _ = stmt.value
        self.set_var(name, self.eval_expr(stmt.children[0]))

    elif stmt.tag == DGM_MAP["ASSIGN"]:
        if len(stmt.children) == 1:
            # x = expr
            value = self.eval_expr(stmt.children[0])
            self.set_var(stmt.value, value)
        else:
            # nested indexing assignment
            target = stmt.value
            indices = []
            base = stmt.children[0]
            if base.tag == DGM_MAP["INDEX"]:
                arr = self.eval_expr(base.children[0])
                idx = self.eval_expr(base.children[1])
                indices.append(idx)
                while base.children[0].tag == DGM_MAP["INDEX"]:
                    base = base.children[0]
                    idx = self.eval_expr(base.children[1])
                    indices.insert(0, idx)
                container = self.eval_expr(base.children[0])
                # walk indices
                ref = container
                for i in indices[:-1]:
                    ref = ref[i]
                ref[indices[-1]] = self.eval_expr(stmt.children[1])
                self.set_var(target, container)
            else:
                idx = self.eval_expr(stmt.children[0])
                value = self.eval_expr(stmt.children[1])
                arr = self.get_var(target)
                arr[idx] = value
                self.set_var(target, arr)

    elif stmt.tag == DGM_MAP["FOR"]:
        var = stmt.value
        start, end, block = stmt.children
        s = self.eval_expr(start)
        e = self.eval_expr(end)
        for i in range(s, e+1):
            self.push_scope()
            self.set_var(var, i)
            for sstmt in block.children:
                self.exec_stmt(sstmt)
                if self.return_flag: break
            self.pop_scope()

    elif stmt.tag == DGM_MAP["WHILE"]:
        cond, block = stmt.children
        while self.eval_expr(cond):
            self.push_scope()
            for sstmt in block.children:
                self.exec_stmt(sstmt)
                if self.return_flag: break
            self.pop_scope()
            if self.return_flag: break

    elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
        print(self.eval_expr(stmt.children[0]))
    # ... rest unchanged ...

def eval_expr(self, expr):
    if expr.tag == DGM_MAP["VAR"]:
        return self.get_var(expr.value)
    elif expr.tag == DGM_MAP["VALUE"]:
        return expr.value
    elif expr.tag == DGM_MAP["BOOL"]:
        return expr.value
    elif expr.tag == DGM_MAP["INDEX"]:
        base = self.eval_expr(expr.children[0])
        idx = self.eval_expr(expr.children[1])
        return base[idx]
    elif expr.tag == DGM_MAP["TUPLE"]:
        return tuple(self.eval_expr(e) for e in expr.children)
    elif expr.tag == DGM_MAP["LIST"]:
        return [self.eval_expr(e) for e in expr.children]
    elif expr.tag == DGM_MAP["ARRAY"]:
        return [self.eval_expr(e) for e in expr.children]
    elif expr.tag == DGM_MAP["EXPR"]:
        op = expr.value
        if op == "not":
            return not self.eval_expr(expr.children[0])
        l = self.eval_expr(expr.children[0])
        r = self.eval_expr(expr.children[1])
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l // r
        if op == "and": return l and r
        if op == "or": return l or r
        if op == "<": return l < r
        if op == "<=": return l <= r
        if op == ">": return l > r
        if op == ">=": return l >= r
        if op == "==": return l == r
        if op == "!=": return l != r

class VESE:
    def __init__(self):
        self.scope_stack = [{}]
        self.functions = {}
        self.return_flag = False
        self.return_value = None
        self.break_flag = False
        self.continue_flag = False

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["BREAK"]:
            self.break_flag = True
            return
        elif stmt.tag == DGM_MAP["CONTINUE"]:
            self.continue_flag = True
            return

        elif stmt.tag == DGM_MAP["FOR"]:
            var = stmt.value
            start, end, block = stmt.children
            s = self.eval_expr(start)
            e = self.eval_expr(end)
            for i in range(s, e+1):
                self.push_scope()
                self.set_var(var, i)
                for sstmt in block.children:
                    self.exec_stmt(sstmt)
                    if self.return_flag or self.break_flag:
                        break
                    if self.continue_flag:
                        self.continue_flag = False
                        break
                self.pop_scope()
                if self.return_flag or self.break_flag:
                    break
            self.break_flag = False  # reset after loop

        elif stmt.tag == DGM_MAP["WHILE"]:
            cond, block = stmt.children
            while self.eval_expr(cond):
                self.push_scope()
                for sstmt in block.children:
                    self.exec_stmt(sstmt)
                    if self.return_flag or self.break_flag:
                        break
                    if self.continue_flag:
                        self.continue_flag = False
                        break
                self.pop_scope()
                if self.return_flag or self.break_flag:
                    break
            self.break_flag = False

        elif stmt.tag == DGM_MAP["RETURN"]:
            self.return_value = self.eval_expr(stmt.children[0])
            self.return_flag = True

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            print(self.eval_expr(stmt.children[0]))
        # ... keep rest as before ...

    def eval_expr(self, expr):
        if expr.tag == DGM_MAP["ARRAY"]:
            return [self.eval_expr(e) for e in expr.children]
        elif expr.tag == DGM_MAP["LIST"]:
            return [self.eval_expr(e) for e in expr.children]
        elif expr.tag == DGM_MAP["TUPLE"]:
            return tuple(self.eval_expr(e) for e in expr.children)
        elif expr.tag == DGM_MAP["STRUCT"]:
            fields = {}
            for f in expr.children:
                fname, _ = f.value
                fields[fname] = self.eval_expr(f.children[0])
            return fields
        # ... keep booleans, arithmetic, etc.

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["SWITCH"]:
        value = self.eval_expr(stmt.value)
        matched = False
        for child in stmt.children:
            if child.tag == DGM_MAP["CASE"]:
                match_val = self.eval_expr(child.value)
                if value == match_val and not matched:
                    matched = True
                    for s in child.children[0].children:
                        self.exec_stmt(s)
                    break
            elif child.tag == DGM_MAP["DEFAULT"] and not matched:
                for s in child.children[0].children:
                    self.exec_stmt(s)

    elif stmt.tag == DGM_MAP["FIELD_ASSIGN"]:
        base, field = stmt.value
        val = self.eval_expr(stmt.children[0])
        obj = self.get_var(base)
        if isinstance(obj, dict):
            obj[field] = val
            self.set_var(base, obj)
        else:
            raise TypeError(f"{base} is not a struct")

    # loop, assign, break/continue remain as before...

def eval_expr(self, expr):
    if expr.tag == DGM_MAP["INDEX"]:
        base = self.eval_expr(expr.children[0])
        idx = self.eval_expr(expr.children[1])
        return base[idx]
    elif expr.tag == DGM_MAP["FIELD"]:
        base, field = expr.value
        obj = self.get_var(base)
        if isinstance(obj, dict):
            return obj[field]
        elif isinstance(obj, list):  # array of structs
            raise RuntimeError("Direct FIELD on list requires INDEX first")
    return super().eval_expr(expr)

def match_pattern(self, pattern, value):
    if pattern.tag == DGM_MAP["VALUE"]:
        return pattern.value == value
    elif pattern.tag == DGM_MAP["PATTERN"]:
        if pattern.value == "tuple":
            if not isinstance(value, tuple) or len(value) != len(pattern.children):
                return False
            return all(self.match_pattern(p, v) for p, v in zip(pattern.children, value))
        elif pattern.value == "range":
            start = int(pattern.children[0].value)
            end = int(pattern.children[1].value)
            return start <= value <= end
        elif pattern.value == "wildcard":
            return True
        else:
            return False
    return False

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["SWITCH"]:
        value = self.eval_expr(stmt.value)
        executed = False
        for child in stmt.children:
            if child.tag == DGM_MAP["CASE"]:
                pattern, block = child.children
                if self.match_pattern(pattern, value) and not executed:
                    executed = True
                    for s in block.children:
                        self.exec_stmt(s)
            elif child.tag == DGM_MAP["DEFAULT"] and not executed:
                for s in child.children[0].children:
                    self.exec_stmt(s)

    elif stmt.tag == DGM_MAP["METHOD_DEF"]:
        struct_name, mname = stmt.value
        if struct_name not in self.functions:
            self.functions[struct_name] = {}
        self.functions[struct_name][mname] = (stmt.children[0], stmt.children[1])

    elif stmt.tag == DGM_MAP["METHOD_CALL"]:
        base, mname = stmt.value
        obj = self.get_var(base)
        params, block = self.functions[type(obj).__name__][mname]
        self.push_scope()
        self.set_var("self", obj)
        for p, a in zip(params.value, stmt.children):
            self.set_var(p, self.eval_expr(a))
        for s in block.children:
            self.exec_stmt(s)
            if self.return_flag:
                break
        obj = self.get_var("self")
        self.set_var(base, obj)
        self.pop_scope()

def match_pattern(self, pattern, value):
    if pattern.tag == DGM_MAP["VALUE"]:
        return pattern.value == value
    elif pattern.tag == DGM_MAP["PATTERN"]:
        if pattern.value == "tuple":
            if not isinstance(value, tuple) or len(value) != len(pattern.children):
                return False
            return all(self.match_pattern(p, v) for p, v in zip(pattern.children, value))

        elif isinstance(pattern.value, tuple) and pattern.value[0] == "struct":
            _, sname = pattern.value
            if not isinstance(value, dict) or value.get("__type__") != sname:
                return False
            return True  # deeper field matching to be expanded later

        elif pattern.value == "wildcard":
            return True
    return False

class VESE:
    def __init__(self):
        self.struct_methods = {}   # {struct_name: {method_name: [overloads]}}
        self.traits = {}           # {trait_name: [methods]}
        self.impls = {}            # {(struct, trait): methods}

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["METHOD_DEF"]:
            struct_name, mname = stmt.value
            if struct_name not in self.struct_methods:
                self.struct_methods[struct_name] = {}
            if mname not in self.struct_methods[struct_name]:
                self.struct_methods[struct_name][mname] = []
            self.struct_methods[struct_name][mname].append((stmt.children[0], stmt.children[1]))

        elif stmt.tag == DGM_MAP["METHOD_CALL"]:
            base, mname = stmt.value
            obj = self.get_var(base)
            sname = obj.get("__type__", type(obj).__name__)
            overloads = self.struct_methods.get(sname, {}).get(mname, [])
            for params, block in overloads:
                if len(params.value) == len(stmt.children):
                    self.push_scope()
                    self.set_var("self", obj)
                    for p, a in zip(params.value, stmt.children):
                        self.set_var(p, self.eval_expr(a))
                    for s in block.children:
                        self.exec_stmt(s)
                        if self.return_flag: break
                    obj = self.get_var("self")
                    self.set_var(base, obj)
                    self.pop_scope()
                    return self.return_value

        elif stmt.tag == DGM_MAP["TRAIT_DEF"]:
            self.traits[stmt.value] = stmt.children

        elif stmt.tag == DGM_MAP["TRAIT_IMPL"]:
            sname, tname = stmt.value
            self.impls[(sname, tname)] = stmt.children

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["DESTRUCT"]:
        val = self.eval_expr(stmt.children[0])
        if isinstance(stmt.value, list):  # tuple destructure
            for name, v in zip(stmt.value, val):
                self.set_var(name, v)
        elif isinstance(stmt.value, tuple):  # struct destructure
            struct_name, fields = stmt.value
            for f, v in zip(fields, val):
                self.set_var(f, v)

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["TRAIT_DEF"]:
        tname, parent = stmt.value
        self.traits[tname] = {"methods": stmt.children, "parent": parent}

    elif stmt.tag == DGM_MAP["TRAIT_IMPL"]:
        sname, tname = stmt.value
        methods = stmt.children
        required = list(self.traits[tname]["methods"])
        # inherit parent's methods if any
        parent = self.traits[tname]["parent"]
        while parent:
            required += self.traits[parent]["methods"]
            parent = self.traits[parent]["parent"]
        impl_methods = [m.value[1] for m in methods]
        for r in required:
            if r not in impl_methods:
                raise Exception(f"{sname} missing trait method {r} from {tname}")
        self.impls[(sname, tname)] = methods

def match_pattern(self, pattern, value):
    if isinstance(pattern.value, tuple) and pattern.value[0] == "struct":
        _, sname = pattern.value
        if not isinstance(value, dict) or value.get("__type__") != sname:
            return False
        for child, (fname, fval) in zip(pattern.children, [(k,v) for k,v in value.items() if k != "__type__"]):
            if child.value == "wildcard":
                continue
            elif self.is_identifier(child.value):
                self.set_var(child.value, fval)
            elif not self.match_pattern(child, fval):
                return False
        return True
    return super().match_pattern(pattern, value)

class VESE:
    def __init__(self):
        self.generic_traits = {}  # { (trait, type_params): methods }
        self.generic_impls = {}   # { (struct, trait, type_args): methods }

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["GENERIC_TRAIT"]:
            tname, type_params, parent = stmt.value
            self.generic_traits[(tname, tuple(type_params))] = {"methods": stmt.children, "parent": parent}

        elif stmt.tag == DGM_MAP["GENERIC_IMPL"]:
            sname, tname, type_args = stmt.value
            self.generic_impls[(sname, tname, tuple(type_args))] = stmt.children

        # reuse trait enforcement logic

class VESE:
    def __init__(self):
        self.enums = {}   # {enum_name: {variant: fields}}

    def exec_stmt(self, stmt):
        if stmt.tag == DGM_MAP["ENUM_DEF"]:
            ename, params = stmt.value
            self.enums[ename] = {v.value[0]: v.value[1] for v in stmt.children}

    def construct_variant(self, ename, vname, values):
        return {"__enum__": ename, "__variant__": vname, "fields": values}

    def match_pattern(self, pattern, value):
        if isinstance(pattern.value, tuple) and pattern.value[0] == "struct":
            _, sname = pattern.value
            if value.get("__enum__") != sname and value.get("__type__") != sname:
                return False
            # handle field binding
            for child, field in zip(pattern.children, value.get("fields", [])):
                if child.value == "wildcard":
                    continue
                elif self.is_identifier(child.value):
                    self.set_var(child.value, field)
                elif not self.match_pattern(child, field):
                    return False
            return True
        return super().match_pattern(pattern, value)

def construct_variant(self, ename, vname, values):
    return {"__enum__": ename, "__variant__": vname, "fields": values}

def match_pattern(self, pattern, value):
    if isinstance(value, dict) and "__enum__" in value:
        # variant pattern: e.g. Cons(h,t)
        if isinstance(pattern.value, tuple) and pattern.value[0] == "struct":
            _, vname = pattern.value
            if value["__variant__"] != vname:
                return False
            for child, field in zip(pattern.children, value["fields"]):
                if child.value == "wildcard":
                    continue
                elif self.is_identifier(child.value):
                    self.set_var(child.value, field)
                elif not self.match_pattern(child, field):
                    return False
            return True
    return super().match_pattern(pattern, value)

def eval_binop(self, op, left, right):
    if op == ">>=":
        monad = left
        f = right  # function closure node
        # get struct/enum type
        if isinstance(monad, dict) and "__enum__" in monad:
            ename = monad["__enum__"]
            impl = self.impls.get((ename, "Monad"), None)
            if impl:
                for stmt in impl:
                    if stmt.value[1] == "bind":
                        return self.exec_method(monad, stmt, [f])
        raise Exception("No monad bind impl")
    return super().eval_binop(op, left, right)

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["DO_BLOCK"]:
        expr = None
        for child in stmt.children:
            if child.tag == DGM_MAP["MONAD_BIND"]:
                var, monad_expr = child.value, child.children[0]
                monad_val = self.eval_expr(monad_expr)
                def cont(x, rest=stmt.children[stmt.children.index(child)+1:]):
                    self.set_var(var, x)
                    if rest:
                        return self.exec_do(rest)
                    return x
                expr = self.monad_bind(monad_val, cont)
            elif child.tag == "RETURN":
                expr = self.eval_expr(child.children[0])
        return expr

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["FOR_BLOCK"]:
        expr = None
        for child in stmt.children:
            if child.tag == DGM_MAP["MONAD_BIND"]:
                var, monad_expr = child.value, child.children[0]
                monad_val = self.eval_expr(monad_expr)
                def cont(x, rest=stmt.children[stmt.children.index(child)+1:]):
                    self.set_var(var, x)
                    if rest:
                        return self.exec_for(rest)
                    return x
                expr = self.monad_bind(monad_val, cont)
            elif child.tag == DGM_MAP["MONAD_YIELD"]:
                expr = self.eval_expr(child.children[0])
        return expr

def monad_bind(self, monad, cont):
    if isinstance(monad, dict) and "__enum__" in monad:
        ename = monad["__enum__"]
        impl = self.impls.get((ename, "Monad"), None)
        if impl:
            for stmt in impl:
                if stmt.value[1] == "bind":
                    # call bind with cont
                    return self.exec_method(monad, stmt, [cont])
    return monad

def monad_bind(self, monad, cont):
    if isinstance(monad, dict) and "__enum__" in monad:
        ename = monad["__enum__"]
        impl = self.impls.get((ename, "Monad"), None)
        if impl:
            for stmt in impl:
                if stmt.value[1] == "bind":
                    return self.exec_method(monad, stmt, [cont])
    return monad

def eval_expr(self, node):
    if node.tag == "LIST_COMPREHENSION":
        expr = node.children[0]
        binds = [c for c in node.children[1:] if c.tag == DGM_MAP["MONAD_BIND"]]
        cond  = node.children[-1] if node.children and node.children[-1].tag not in (DGM_MAP["MONAD_BIND"],) else None

        def loop(i, env):
            if i >= len(binds):
                val = self.eval_expr(expr)
                return self.construct_variant("List", "Cons", [val, self.construct_variant("List", "Nil", [])])
            var, src = binds[i].value, binds[i].children[0]
            src_val = self.eval_expr(src)
            result = self.construct_variant("List", "Nil", [])
            if src_val["__variant__"] == "Cons":
                h, t = src_val["fields"]
                self.set_var(var, h)
                rest = loop(i+1, env)
                result = self.concat(result, rest)
                if t["__variant__"] != "Nil":
                    self.set_var(var, t)
                    result = self.concat(result, loop(i, env))
            return result

        return loop(0, {})
    return super().eval_expr(node)

def run_io(self, io):
    return io["run"]()

def run_state(self, state, init):
    return state["run"](init)

def run_reader(self, reader, env):
    return reader["run"](env)

def run_writer(self, writer):
    return (writer["value"], writer["log"])

def exec_stmt(self, stmt):
    if stmt.tag == DGM_MAP["EFFECT_BLOCK"]:
        mname, tparam = stmt.value
        # Wrap body into monad expansion
        result = None
        for s in stmt.children:
            result = self.exec_stmt(s)
        return result

