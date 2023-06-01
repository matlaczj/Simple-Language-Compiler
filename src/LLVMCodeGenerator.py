# type: ignore

from llvmlite import ir
from antlr.MinLangVisitor import MinLangVisitor
from antlr.MinLangParser import MinLangParser


class LLVMCodeGenerator(MinLangVisitor):
    def __init__(self):
        super().__init__()
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.variables = {}
        entry_block = ir.Function(
            module=self.module,
            ftype=ir.FunctionType(return_type=ir.IntType(32), args=[]),
            name="main",
        ).append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        self.printf_counter = 0
        self.scanf_counter = 0
        self.to_be_declared = []

    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        return str(self.module)

    def visitDeclarationStatement(self, ctx):
        var_type = self.visit(ctx.type_())
        var_name = ctx.id_().getText()
        if var_type == "string": # string is a special case, declare when size is known
            self.to_be_declared.append(var_name)
            return

        alloca = self.builder.alloca(var_type, name=var_name)
        self.variables[var_name] = alloca

    def visitAssignmentStatement(self, ctx):
        var_name = ctx.id_().getText()
        if var_name not in self.variables and var_name not in self.to_be_declared:
            raise NameError(f"Variable '{var_name}' is not declared.")
        var_value = self.visit(ctx.expression())

        if type(var_value) == tuple:
            _, literal = var_value
            string_value = self.createStringGlobalVariable(literal.replace('"', ""))
            self.to_be_declared.remove(var_name)
            self.variables[var_name] = string_value
        else:
            self.builder.store(var_value, self.variables[var_name])

    def visitId(self, ctx):
        var_name = ctx.getText()
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not declared.")
        return self.builder.load(self.variables[var_name])

    def visitLiteral(self, ctx):
        literal = ctx.getText()
        literal_type = ctx.start.type
        if literal_type == MinLangParser.INT:
            return ir.Constant(ir.IntType(32), int(literal))
        elif literal_type == MinLangParser.FLOAT:
            return ir.Constant(ir.FloatType(), float(literal))
        elif literal_type == MinLangParser.BOOL:
            return ir.Constant(ir.IntType(1), int(literal == "true"))
        elif literal_type == MinLangParser.STRING:
            return literal_type, literal

    def visitArithmeticOperator(self, ctx):
        operator = ctx.getText()
        if operator == "+":
            return "add"
        elif operator == "-":
            return "sub"
        elif operator == "*":
            return "mul"
        elif operator == "/":
            return "div"

    def visitRelationalOperator(self, ctx):
        operator = ctx.getText()
        if operator == ">":
            return "cmp_sgt"
        elif operator == "<":
            return "cmp_slt"
        elif operator == ">=":
            return "cmp_sge"
        elif operator == "<=":
            return "cmp_sle"
        elif operator == "==":
            return "cmp_eq"
        elif operator == "!=":
            return "cmp_ne"

    def visitExpression(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        else:
            left = self.visit(ctx.getChild(0))
            right = self.visit(ctx.getChild(2))
            operator = self.visit(ctx.getChild(1))
            if left.type != right.type:
                raise ValueError("Mismatched types in arithmetic expression.")
            if operator in ["add", "sub", "mul", "div"]:
                if isinstance(left.type, ir.types.FloatType):
                    if operator == "add":
                        return self.builder.fadd(left, right, "addtmp")
                    elif operator == "sub":
                        return self.builder.fsub(left, right, "subtmp")
                    elif operator == "mul":
                        return self.builder.fmul(left, right, "multmp")
                    elif operator == "div":
                        return self.builder.fdiv(left, right, "divtmp")
                elif isinstance(left.type, ir.types.IntType):
                    if operator == "add":
                        return self.builder.add(left, right, "addtmp")
                    elif operator == "sub":
                        return self.builder.sub(left, right, "subtmp")
                    elif operator == "mul":
                        return self.builder.mul(left, right, "multmp")
                    elif operator == "div":
                        return self.builder.sdiv(left, right, "divtmp")
                else:
                    raise ValueError("Unsupported type in arithmetic expression.")
            elif operator in [
                "cmp_sgt",
                "cmp_slt",
                "cmp_sge",
                "cmp_sle",
                "cmp_eq",
                "cmp_ne",
            ]:
                if isinstance(left.type, ir.types.FloatType):
                    if operator == "cmp_sgt":
                        return self.builder.fcmp_ordered(">", left, right, "sgttmp")
                    elif operator == "cmp_slt":
                        return self.builder.fcmp_ordered("<", left, right, "slttmp")
                    elif operator == "cmp_sge":
                        return self.builder.fcmp_ordered(">=", left, right, "sgetmp")
                    elif operator == "cmp_sle":
                        return self.builder.fcmp_ordered("<=", left, right, "sletmp")
                    elif operator == "cmp_eq":
                        return self.builder.fcmp_ordered("==", left, right, "eqtmp")
                    elif operator == "cmp_ne":
                        return self.builder.fcmp_ordered("!=", left, right, "netmp")
                elif isinstance(left.type, ir.types.IntType):
                    if operator == "cmp_sgt":
                        return self.builder.icmp_signed(">", left, right, "sgttmp")
                    elif operator == "cmp_slt":
                        return self.builder.icmp_signed("<", left, right, "slttmp")
                    elif operator == "cmp_sge":
                        return self.builder.icmp_signed(">=", left, right, "sgetmp")
                    elif operator == "cmp_sle":
                        return self.builder.icmp_signed("<=", left, right, "sletmp")
                    elif operator == "cmp_eq":
                        return self.builder.icmp_signed("==", left, right, "eqtmp")
                    elif operator == "cmp_ne":
                        return self.builder.icmp_signed("!=", left, right, "netmp")
                else:
                    raise ValueError("Unsupported type in relational expression.")

    def visitOperator(self, ctx):
        return self.visitChildren(ctx)

    def visitType(self, ctx):
        type_name = ctx.getText()
        if type_name == "int":
            return ir.IntType(32)
        elif type_name == "float":
            return ir.FloatType()
        elif type_name == "bool":
            return ir.IntType(1)
        elif type_name == "string":
            return "string"
        else:
            raise ValueError("Unknown type: " + type_name)

    def visitPrintStatement(self, ctx):
        value = self.visit(ctx.expression())
        var_name = ctx.expression().getText()
        # Handle string literals
        if isinstance(value, tuple):
            _, string_value = value
            value = self.createStringGlobalVariable(string_value)

        printf_format = self.getPrintfFormat(value.type)
        printf_func = self.getPrintfFunction()

        printf_format_global = self.createPrintfFormatGlobal(printf_format)
        if isinstance(value.type, ir.ArrayType):
            var_name = ctx.expression().getText()
            self.builder.call(printf_func, [self.builder.bitcast(self.variables[var_name], ir.IntType(8).as_pointer())])
        else:
            self.builder.call(printf_func, [printf_format_global, value])

    def createStringGlobalVariable(self, string_value):
        string_value = string_value.replace('"', "")
        string_length = len(string_value) + 1
        value = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), string_length), name=f"string_literal_{self.printf_counter}")
        value.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), string_length), bytearray(string_value + "\0", 'utf8'))
        value.linkage = 'internal'
        self.printf_counter += 1
        return value

    def getPrintfFormat(self, value_type):
        if value_type == ir.IntType(32):
            return "%d\n"
        elif value_type == ir.FloatType():
            return "%f\n"
        elif value_type == ir.IntType(1):
            return "%s\n"
        else:
            return "%s\n"  # Default to string format

    def getPrintfFunction(self):
        printf_func = self.module.globals.get("printf")
        if not printf_func:
            printf_func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
            printf_func = ir.Function(self.module, printf_func_type, name="printf")
            self.module.globals["printf"] = printf_func
        return printf_func

    def createPrintfFormatGlobal(self, printf_format):
        printf_format_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(printf_format)), bytearray(printf_format.encode("utf8")))
        printf_format_global = ir.GlobalVariable(self.module, printf_format_const.type, name=f"printf_format_{self.printf_counter}")
        self.printf_counter += 1
        printf_format_global.linkage = "internal"
        printf_format_global.global_constant = True
        printf_format_global.initializer = printf_format_const
        return self.builder.bitcast(printf_format_global, ir.IntType(8).as_pointer())

    def visitReadStatement(self, ctx):
        var_name = ctx.id_().getText()
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not declared.")
        var_type = self.variables[var_name].type.pointee
        scanf_func = self.module.globals.get("scanf")
        if not scanf_func:
            scanf_func_type = ir.FunctionType(
                ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True
            )
            scanf_func = ir.Function(self.module, scanf_func_type, name="scanf")
            self.module.globals["scanf"] = scanf_func
        scan_format = "%d" if var_type == ir.IntType(32) else "%f"
        scan_format_const = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(scan_format)),
            bytearray(scan_format.encode("utf8")),
        )
        scan_format_global = ir.GlobalVariable(
            self.module,
            scan_format_const.type,
            name=f"scan_format_{self.scanf_counter}",
        )
        self.scanf_counter += 1
        scan_format_global.linkage = "internal"
        scan_format_global.global_constant = True
        scan_format_global.initializer = scan_format_const
        scan_format_ptr = self.builder.bitcast(
            scan_format_global, ir.IntType(8).as_pointer()
        )
        var_alloca = self.variables[var_name]
        self.builder.call(scanf_func, [scan_format_ptr, var_alloca])
