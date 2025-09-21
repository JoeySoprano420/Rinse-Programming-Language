# rinsec.py — CLI compiler
import sys
from lexer import tokenize
from parser import Parser
from ir_gen import gen_ir
from vese import run

def main():
    if len(sys.argv) < 2:
        print("Usage: rinsec <file.rn>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    ir = gen_ir(ast)
    print("=== LLVM IR ===")
    print(ir)

    # Simulate VESE execution
    run([("print", 42)])  # stub: replace with real lowering

if __name__ == "__main__":
    main()
