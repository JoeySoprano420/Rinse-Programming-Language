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

            if line.endswith(":"):
                continue  # Skip labels

            parts = line.split()
            if not parts:
                continue

            op = parts[0]

            if op == "mov":
                if "," in line:
                    reg, val = parts[1].strip(","), parts[2]
                    if val in self.registers:
                        self.registers[reg] = self.registers[val]
                    else:
                        self.registers[reg] = int(val)

            elif op == "add":
                reg1 = parts[1].strip(",")
                reg2 = parts[2]
                if reg2 in self.registers:
                    self.registers[reg1] += self.registers[reg2]
                else:
                    self.registers[reg1] += int(reg2)

            elif op == "sub":
                reg1 = parts[1].strip(",")
                reg2 = parts[2]
                if reg2 in self.registers:
                    self.registers[reg1] -= self.registers[reg2]
                else:
                    self.registers[reg1] -= int(reg2)

            elif op == "imul":
                reg1 = parts[1].strip(",")
                reg2 = parts[2]
                if reg2 in self.registers:
                    self.registers[reg1] *= self.registers[reg2]
                else:
                    self.registers[reg1] *= int(reg2)

            elif op == "idiv":
                reg = parts[1]
                if reg in self.registers:
                    self.registers["eax"] = self.registers["eax"] // self.registers[reg]
                else:
                    self.registers["eax"] = self.registers["eax"] // int(reg)

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
                if reg1 == reg2:
                    self.registers[reg1] = 0
                else:
                    self.registers[reg1] = self.registers[reg1] ^ self.registers[reg2]

            elif op == "ret":
                return 0
