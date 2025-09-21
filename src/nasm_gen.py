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

