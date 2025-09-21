# ir_gen.py — Rinse v0.1.0
# AST → LLVM IR (via llvmlite)

from llvmlite import ir
from .ast_dgm import DGM_MAP

def gen_ir(ast):
    module = ir.Module(name="main")
    func_type = ir.FunctionType(ir.IntType(32), [])
    main = ir.Function(module, func_type, name="main")
    block = main.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Declare print_int function once
    fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
    printf = ir.Function(module, fnty, name="print_int")

    variables = {}

    for stmt in ast.children[0].children:
        if stmt.tag == DGM_MAP["VAR"]:
            name, typ = stmt.value
            val_node = stmt.children[0]
            alloca = builder.alloca(ir.IntType(32), name=name)
            builder.store(ir.Constant(ir.IntType(32), val_node.value), alloca)
            variables[name] = alloca

        elif stmt.tag == DGM_MAP["FLOW"]:
            var_name = stmt.children[0].value
            val = builder.load(variables[var_name], name=var_name)
            builder.call(printf, [val])

    builder.ret(ir.Constant(ir.IntType(32), 0))
    return str(module)
