#!/usr/bin/env python3
"""
Rinse Compiler (rinsec)
SRC -> LLVM -> NASM -> .exe
Executes inside VESE (Virtual Execution Simulated Env)
"""

import argparse
from rinsec.lexer import tokenize
from rinsec.parser import Parser
from rinsec.codegen_llvm import LLVMGenerator
from rinsec.codegen_nasm import NASMGenerator
from rinsec.vese_runtime import VESE

def main():
    parser = argparse.ArgumentParser(description="Rinse Compiler")
    parser.add_argument("source", help="Rinse source file (.rns)")
    parser.add_argument("--emit", choices=["llvm", "nasm", "exe"], default="exe")
    args = parser.parse_args()

    with open(args.source, "r") as f:
        source_code = f.read()

    tokens = tokenize(source_code)
    ast = Parser(tokens).parse()

    if args.emit == "llvm":
        LLVMGenerator().emit(ast)
    elif args.emit == "nasm":
        NASMGenerator().emit(ast)
    elif args.emit == "exe":
        ir = LLVMGenerator().emit(ast)
        asm = NASMGenerator().emit(ir)
        VESE().execute(asm)

if __name__ == "__main__":
    main()
