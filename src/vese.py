# vese.py — VESE Runtime
# Executes NASM-like opcodes in a sandbox

def run(program):
    for instr in program:
        if instr[0] == "print":
            print(instr[1])
