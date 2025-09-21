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

