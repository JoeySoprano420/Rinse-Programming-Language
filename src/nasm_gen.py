# nasm_gen.py — Rinse v0.2.0
# AST → NASM assembly (string form)

from ast_dgm import DGM_MAP

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            val = stmt.children[0].value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            lines.append(f"    mov {reg}, {val}")

        elif stmt.tag == DGM_MAP["FLOW"]:
            # print flow
            name = stmt.children[0].value
            reg = var_map[name]
            lines.append(f"    push {reg}")
            lines.append("    call print_int")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)

# nasm_gen.py (extended for add expr)

from ast_dgm import DGM_MAP

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            val = stmt.children[0].value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            lines.append(f"    mov {reg}, {val}")

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            expr = stmt.children[0]
            if expr.tag == DGM_MAP["VAR"]:
                reg = var_map[expr.value]
                lines.append(f"    push {reg}")
                lines.append("    call print_int")

            elif expr.tag == DGM_MAP["EXPR"]:
                op = expr.value
                left, right = expr.children

                # move left operand into eax
                if left.tag == DGM_MAP["VAR"]:
                    lines.append(f"    mov eax, {var_map[left.value]}")
                else:
                    lines.append(f"    mov eax, {left.value}")

                # apply operator with right operand
                if right.tag == DGM_MAP["VAR"]:
                    lines.append(f"    add eax, {var_map[right.value]}")
                else:
                    lines.append(f"    add eax, {right.value}")

                lines.append("    push eax")
                lines.append("    call print_int")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)

# nasm_gen.py (extended for add expr)

from ast_dgm import DGM_MAP

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            val = stmt.children[0].value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            lines.append(f"    mov {reg}, {val}")

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            expr = stmt.children[0]
            if expr.tag == DGM_MAP["VAR"]:
                reg = var_map[expr.value]
                lines.append(f"    push {reg}")
                lines.append("    call print_int")

            elif expr.tag == DGM_MAP["EXPR"]:
                op = expr.value
                left, right = expr.children

                # move left operand into eax
                if left.tag == DGM_MAP["VAR"]:
                    lines.append(f"    mov eax, {var_map[left.value]}")
                else:
                    lines.append(f"    mov eax, {left.value}")

                # apply operator with right operand
                if right.tag == DGM_MAP["VAR"]:
                    lines.append(f"    add eax, {var_map[right.value]}")
                else:
                    lines.append(f"    add eax, {right.value}")

                lines.append("    push eax")
                lines.append("    call print_int")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)

# nasm_gen.py — extended arithmetic

from ast_dgm import DGM_MAP

def emit_expr(expr, var_map, lines):
    if expr.tag == DGM_MAP["VAR"]:
        lines.append(f"    mov eax, {var_map[expr.value]}")
    elif expr.tag == DGM_MAP["VALUE"]:
        lines.append(f"    mov eax, {expr.value}")
    elif expr.tag == DGM_MAP["EXPR"]:
        op = expr.value
        left, right = expr.children
        emit_expr(left, var_map, lines)
        lines.append("    push eax")  # save left
        emit_expr(right, var_map, lines)
        lines.append("    mov ebx, eax")  # right → ebx
        lines.append("    pop eax")       # left → eax
        if op == "+":
            lines.append("    add eax, ebx")
        elif op == "-":
            lines.append("    sub eax, ebx")
        elif op == "*":
            lines.append("    imul eax, ebx")
        elif op == "/":
            lines.append("    xor edx, edx")  # clear high bits
            lines.append("    idiv ebx")

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            val = stmt.children[0].value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            lines.append(f"    mov {reg}, {val}")

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            expr = stmt.children[0]
            emit_expr(expr, var_map, lines)
            lines.append("    push eax")
            lines.append("    call print_int")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    def emit_expr(expr, var_map, lines):
        if expr.tag == DGM_MAP["VAR"]:
            lines.append(f"    mov eax, {var_map[expr.value]}")
        elif expr.tag == DGM_MAP["VALUE"]:
            lines.append(f"    mov eax, {expr.value}")
        elif expr.tag == DGM_MAP["EXPR"]:
            op = expr.value
            left, right = expr.children
            emit_expr(left, var_map, lines)
            lines.append("    push eax")
            emit_expr(right, var_map, lines)
            lines.append("    mov ebx, eax")
            lines.append("    pop eax")
            if op == "+":
                lines.append("    add eax, ebx")
            elif op == "-":
                lines.append("    sub eax, ebx")
            elif op == "*":
                lines.append("    imul eax, ebx")
            elif op == "/":
                lines.append("    xor edx, edx")
                lines.append("    idiv ebx")

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            emit_expr(stmt.children[0], var_map, lines)
            lines.append(f"    mov {reg}, eax")

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            emit_expr(stmt.children[0], var_map, lines)
            lines.append("    push eax")
            lines.append("    call print_int")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)


- **Structs/Tuples/Lists**:  
- Represented in VESE as Python dicts/lists.  
- NASM representation is abstracted to “heap-like” allocations.  

- **Proofs**:  
- Compile to conditionals, but with an assertion that halts VESE if false.  

---

# 🔹 VESE Runtime Extensions (sketch)

```python
elif op == "cmp":
 reg1, reg2 = parts[1].strip(","), parts[2]
 self.flags["cmp"] = self.registers[reg1] - self.registers.get(reg2, int(reg2))

elif op == "jg":
 if self.flags["cmp"] > 0:
     self.pc = self.labels[parts[1]]

elif op == "jl":
 if self.flags["cmp"] < 0:
     self.pc = self.labels[parts[1]]

elif op == "je":
 if self.flags["cmp"] == 0:
     self.pc = self.labels[parts[1]]

elif op == "pow":
 base, exp = self.registers["eax"], self.registers["ebx"]
 self.registers["eax"] = pow(base, exp)

elif op == "assert":
 cond = self.stack.pop()
 if not cond:
     raise AssertionError("Proof failed")

label_counter = 0
def new_label(prefix="L"):
    global label_counter
    label = f"{prefix}{label_counter}"
    label_counter += 1
    return label

def gen_nasm(ast):
    lines = []
    lines.append("section .data")
    lines.append("section .text")
    lines.append("global _main")
    lines.append("_main:")

    registers = ["eax", "ebx", "ecx", "edx"]
    reg_idx = 0
    var_map = {}

    def emit_expr(expr, var_map, lines):
        if expr.tag == DGM_MAP["VAR"]:
            lines.append(f"    mov eax, {var_map[expr.value]}")
        elif expr.tag == DGM_MAP["VALUE"]:
            lines.append(f"    mov eax, {expr.value}")
        elif expr.tag == DGM_MAP["BOOL"]:
            lines.append(f"    mov eax, {1 if expr.value == 'true' else 0}")
        elif expr.tag == DGM_MAP["EXPR"]:
            op = expr.value
            left, right = expr.children
            emit_expr(left, var_map, lines)
            lines.append("    push eax")
            emit_expr(right, var_map, lines)
            lines.append("    mov ebx, eax")
            lines.append("    pop eax")
            if op == "+": lines.append("    add eax, ebx")
            elif op == "-": lines.append("    sub eax, ebx")
            elif op == "*": lines.append("    imul eax, ebx")
            elif op == "/":
                lines.append("    xor edx, edx")
                lines.append("    idiv ebx")
            elif op == "^":  # exponentiation loop
                lines.append("    mov ecx, ebx")
                lines.append("    mov ebx, eax")
                lines.append("    mov eax, 1")
                pow_loop = new_label("pow")
                lines.append(f"{pow_loop}:")
                lines.append("    imul eax, ebx")
                lines.append("    loop " + pow_loop)

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            reg = registers[reg_idx % len(registers)]
            reg_idx += 1
            var_map[name] = reg
            emit_expr(stmt.children[0], var_map, lines)
            lines.append(f"    mov {reg}, eax")

        elif stmt.tag == DGM_MAP["FLOW"] and stmt.value == "print":
            emit_expr(stmt.children[0], var_map, lines)
            lines.append("    push eax")
            lines.append("    call print_int")

        elif stmt.tag == DGM_MAP["IF"]:
            cond, block, else_block = stmt.children
            emit_expr(cond, var_map, lines)
            lines.append("    cmp eax, 0")
            lbl_else, lbl_end = new_label("else"), new_label("endif")
            lines.append(f"    je {lbl_else}")
            for s in block.children:
                lines.append("    ; then branch")
            lines.append(f"    jmp {lbl_end}")
            lines.append(f"{lbl_else}:")
            if else_block:
                for s in else_block.children:
                    lines.append("    ; else branch")
            lines.append(f"{lbl_end}:")

        elif stmt.tag == DGM_MAP["PROOF"]:
            cond, block = stmt.children
            emit_expr(cond, var_map, lines)
            lines.append("    cmp eax, 0")
            fail_lbl = new_label("fail")
            lines.append(f"    je {fail_lbl}")
            for s in block.children:
                lines.append("    ; proof block")
            lines.append(f"{fail_lbl}: ; assertion fail")

    lines.append("    xor eax, eax")
    lines.append("    ret")
    return "\n".join(lines)

