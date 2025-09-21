#!/usr/bin/env python3
"""
Rinse Programming Language Compiler (Executable Version)
Usage: rinsec-standalone.exe <file.rn> [-o output.exe]
"""
import sys
import os

# Add the current directory to Python path to find rinse modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from rinse.rinsec import main

if __name__ == "__main__":
    main()