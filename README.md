🌊 Rinse Programming Language

“Noiseless. Hapless. Zero-cost. Progressive Process.”

---

## 🔹 Phase 1 – Core Compiler Skeleton (Python)

Directory layout (as you already drafted):

```
Rinse/
 ├─ src/
 │   ├─ lexer.py
 │   ├─ parser.py
 │   ├─ ast_dgm.py
 │   ├─ ir_gen.py
 │   ├─ nasm_gen.py
 │   └─ rinsec.py
 ├─ starbox/
 ├─ stdlib/
 │   ├─ io.rn
 │   ├─ net.rn
 │   └─ math.rn
 └─ tests/
```

### `lexer.py`

Tokenizes `.rn` code:

* Keywords: `init`, `item`, `flow`, `process`, `parallel`, `let`, `print`, `is`
* Operators: `+`, `-`, `*`, `/`, `=`
* Literals: ints, strings
* Symbols: `{`, `}`, `(`, `)`, `:` , `,`

### `parser.py`

Turns tokens into dodecagram-tagged AST nodes (from `ast_dgm.py`).

### `ast_dgm.py`

Defines node classes with **base-12 tags**:

* `0` → Program
* `1` → Block
* `2` → Statement
* `3` → Expression
* etc. (per your mapping)

### `ir_gen.py`

Translates AST → LLVM IR using `llvmlite`.

### `nasm_gen.py`

Takes LLVM IR → NASM `.asm` code.

### `rinsec.py`

CLI driver:

```bash
rinsec hello.rn -o hello.exe
```

---

## 🔹 Phase 2 – VESE (Virtual Execution Simulated Environment)

Instead of running on the host, `.exe` is a containerized VESE binary:

* Register-based model
* Immutable opcode execution
* Built-in checkpoints
* Parallel execution lanes
* Error handling at block scope

Prototype this with a **Python VM** that interprets the NASM-like output.

---

## 🔹 Phase 3 – Starbox Package Manager

* `starbox init` → creates `starbox.lock` (dodecagram lockfile).
* `starbox add io` → pulls standard lib package into VESE sandbox.

---

## 🔹 Phase 4 – rinsefmt Formatter

* Enforces **dualistic spacing** and **parametric indentation**.
* Guarantees “superior elegance formatting.”

---

## Example Flow

Input (`main.rn`):

```rinse
init main {
    let x: int = 12
    let y: int = 30
    print(x + y)
}
```

Run:

```bash
rinsec main.rn -o main.exe
```

Execution (inside VESE):

```
42
```

---


✅ Running:

(Bash)

cd Rinse/src
python rinsec.py ../tests/hello.rn


## -----

.rn → Lexer → Parser → Dodecagram AST → LLVM IR → NASM → VESE execution

🔹 Expected Run

(Bash)

cd Rinse/src

python rinsec.py ../tests/hello.rn

Output:

=== LLVM IR ===
; ModuleID = "main"
define i32 @main() {
entry:
  ...
}

12
30


## -----


🔹 Expected Run

(Bash)

cd Rinse/src
python rinsec.py ../tests/hello.rn

Output:

(Wasm)

=== LLVM IR ===
; ModuleID = "main"
define i32 @main() {
entry:
  %x = alloca i32, align 4
  %y = alloca i32, align 4
  store i32 12, i32* %x, align 4
  store i32 30, i32* %y, align 4
  ...
}

=== NASM ===
section .data
section .text
global _main
_main:
    mov eax, 12
    mov ebx, 30
    push eax
    call print_int
    push ebx
    call print_int
    xor eax, eax
    ret

=== VESE Execution ===
12
30

## ---

🔹 Expected Run

(Bash)

cd Rinse/src
python rinsec.py ../tests/arith.rn

Output:

=== LLVM IR ===
; ModuleID = "main"
...

=== NASM ===
section .data
section .text
global _main
_main:
    mov eax, 12
    mov ebx, 30
    mov eax, eax
    add eax, ebx
    push eax
    call print_int
    xor eax, eax
    ret

=== VESE Execution ===
42

