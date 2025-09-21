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
