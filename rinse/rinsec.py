# rinsec.py — CLI compiler for Rinse
import sys
from .lexer import tokenize
from .parser import Parser
from .ir_gen import gen_ir
from .nasm_gen import gen_nasm
from .vese import VESE

def main():
    if len(sys.argv) < 2:
        print("Usage: rinsec <file.rn>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    # Generate IR
    ir = gen_ir(ast)
    print("=== LLVM IR ===")
    print(ir)

    # Generate NASM
    nasm = gen_nasm(ast)
    print("\n=== NASM ===")
    print(nasm)

    # Execute in VESE
    print("\n=== VESE Execution ===")
    vm = VESE()
    vm.exec(nasm)

if __name__ == "__main__":
    main()
