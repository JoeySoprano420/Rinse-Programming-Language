"""
VESE (Virtual Execution Simulated Environment)
Runs NASM-like instructions in a sandboxed VM
"""

class VESE:
    def __init__(self):
        self.registers = {"eax":0, "ebx":0, "ecx":0, "edx":0}
        self.stack = []

    def execute(self, asm_lines):
        for line in asm_lines.splitlines():
            parts = line.strip().split()
            if not parts: continue
            op = parts[0]
            if op == "mov":
                self.registers[parts[1].strip(",")] = int(parts[2])
            elif op == "add":
                self.registers[parts[1].strip(",")] += int(parts[2])
            elif op == "push":
                self.stack.append(self.registers[parts[1]])
            elif op == "print":
                print(self.registers[parts[1]])
            elif op == "ret":
                return
