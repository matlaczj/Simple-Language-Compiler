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
        self.main_function = ir.Function(
            module=self.module,
            ftype=ir.FunctionType(return_type=ir.IntType(32), args=[]),
            name="main",
        )
        self.entry_block = self.main_function.append_basic_block(name="entry")
        self.function_declaration = {}
        self.functions = []
        self.inside_block = False
        self.current_function = None
        self.temp_builder = None
        self.builder = ir.IRBuilder(self.entry_block)
        self.local_builder = None
        self.printf_counter = 0
        self.scanf_counter = 0
        self.if_counter = 0
        self.while_counter = 0

    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        return str(self.module)

    def visitDeclarationStatement(self, ctx):
        var_type = self.visit(ctx.type_())
        var_name = ctx.id_().getText()
        if var_name in self.variables and not self.inside_block:
            raise NameError(f"Variable '{var_name}' already declared.")

        if self.inside_block:
            var_name = self.function_declaration["name"] + "." + var_name
            alloca = self.builder.alloca(var_type, name=var_name)
            self.variables[var_name] = alloca
            return

        alloca = self.builder.alloca(var_type, name=var_name)
        self.variables[var_name] = alloca

    def visitAssignmentStatement(self, ctx):
        var_name = ctx.id_().getText()
        if self.inside_block:
            var_name = self.function_declaration["name"] + "." + var_name

        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not declared.")

        var_value = self.visit(ctx.expression())
        self.builder.store(var_value, self.variables[var_name])

    def visitId(self, ctx):
        var_name = ctx.getText()
        if self.inside_block and var_name not in [
            self.function_declaration["parameters"][i][1]
            for i in range(len(self.function_declaration["parameters"]))
        ]:
            var_name = self.function_declaration["name"] + "." + var_name

        if self.function_declaration.get("paramList", False):
            self.function_declaration["parameters"][-1].append(var_name)
            return

        if self.inside_block and var_name not in self.variables:
            for i in range(len(self.function_declaration["parameters"])):
                if var_name in self.function_declaration["parameters"][i]:
                    return self.current_function.args[i]
            raise NameError(f"Variable '{var_name}' is not declared.")

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
            raise NotImplementedError("String literals are not implemented yet.")

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
        llvm_type = None

        if type_name == "int":
            llvm_type = ir.IntType(32)
        elif type_name == "float":
            llvm_type = ir.FloatType()
        elif type_name == "bool":
            llvm_type = ir.IntType(1)
        elif type_name == "string":
            raise NotImplementedError("String literals are not implemented yet.")
        else:
            raise ValueError("Unknown type: " + type_name)

        if self.function_declaration.get("paramList", False):
            self.function_declaration["parameters"].append([llvm_type])
        return llvm_type

    def visitPrintStatement(self, ctx):
        value = self.visit(ctx.expression())
        if value.type == ir.IntType(32):
            printf_format = "%d\n"
        elif value.type == ir.FloatType():
            printf_format = "%f\n"
        elif value.type == ir.IntType(1):
            printf_format = "%s\n"
        else:
            printf_format = "%s\n"
        printf_func = self.module.globals.get("printf")
        if not printf_func:
            printf_func_type = ir.FunctionType(
                ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True
            )
            printf_func = ir.Function(self.module, printf_func_type, name="printf")
            self.module.globals["printf"] = printf_func
        printf_format_const = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(printf_format)),
            bytearray(printf_format.encode("utf8")),
        )
        printf_format_global = ir.GlobalVariable(
            self.module,
            printf_format_const.type,
            name=f"printf_format_{self.printf_counter}",
        )
        self.printf_counter += 1
        printf_format_global.linkage = "internal"
        printf_format_global.global_constant = True
        printf_format_global.initializer = printf_format_const
        printf_format_ptr = self.builder.bitcast(
            printf_format_global, ir.IntType(8).as_pointer()
        )
        self.builder.call(printf_func, [printf_format_ptr, value])

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

    def get_llvm_type(self, type_name):
        llvm_type = None
        if type_name == "int":
            llvm_type = ir.IntType(32)
        elif type_name == "float":
            llvm_type = ir.FloatType()
        elif type_name == "bool":
            llvm_type = ir.IntType(1)
        elif type_name == "string":
            raise NotImplementedError("String literals are not implemented yet.")
        else:
            raise ValueError("Unknown type: " + type_name)
        return llvm_type

    def visitFunctionDeclaration(self, ctx):
        return self.visitChildren(ctx)

    def visitParameterList(self, ctx):
        return self.visitChildren(ctx)

    def visitBlock(self, ctx):
        return_type = self.get_llvm_type(self.function_declaration["type"])
        parameter_types = [
            self.function_declaration["parameters"][i][0]
            for i in range(len(self.function_declaration["parameters"]))
        ]
        function_type = ir.FunctionType(return_type, parameter_types)

        self.current_function = ir.Function(
            self.module, function_type, name=self.function_declaration["name"]
        )
        self.inside_block = True
        basic_block = self.current_function.append_basic_block(name="entry")
        self.temp_builder = self.builder
        self.builder = ir.IRBuilder(basic_block)

        self.function_declaration["paramList"] = False
        self.visitChildren(ctx)
        self.builder = self.temp_builder
        self.inside_block = False

    def visitFunctionType(self, ctx):
        self.function_declaration["type"] = ctx.getText()
        self.function_declaration["parameters"] = []
        return self.visitChildren(ctx)

    def visitFunctionId(self, ctx):
        self.function_declaration["name"] = ctx.getText()
        self.function_declaration["paramList"] = True
        return self.visitChildren(ctx)

    def visitReturnStatement(self, ctx):
        self.builder.ret(self.visitExpression(ctx.expression()))

    def visitFunctionCall(self, ctx):
        function_name = ctx.getChild(0).getText()
        if function_name not in self.module.globals:
            raise NameError(f"Function '{function_name}' is not declared.")
        function = self.module.globals[function_name]
        arguments = ctx.argumentList().getText().split(",")
        args = [self.builder.load(self.variables[arg]) for arg in arguments]
        return self.builder.call(function, args)

    # TODO: Go back to entry block after if statement.
    def visitIfStatement(self, ctx):
        if_block = self.main_function.append_basic_block(name=f"if_block{self.if_counter}")
        else_block = self.main_function.append_basic_block(name=f"else_block{self.if_counter}")
        end_block = self.main_function.append_basic_block(name=f"end_block{self.if_counter}")
        condition = self.visitExpression(ctx.getChild(2))

        self.builder.position_at_end(self.entry_block)
        self.builder.cbranch(condition, if_block, else_block)

        self.builder.position_at_end(if_block)
        self.visitStatement(ctx.getChild(4))
        self.builder.branch(end_block)
        self.builder.position_at_end(else_block)
        self.visitStatement(ctx.getChild(6))
        self.builder.branch(end_block)
        self.builder.position_at_end(end_block)
        self.entry_block = end_block
        self.if_counter += 1

    def visitNormalBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitWhileLoop(self, ctx):
        loop_condition_block = self.main_function.append_basic_block(name=f"loop_condition_block{self.while_counter}")
        loop_block = self.main_function.append_basic_block(name=f"loop_block{self.while_counter}")
        end_block = self.main_function.append_basic_block(name=f"loop_end_block{self.while_counter}")
        self.builder.branch(loop_condition_block)
        self.builder.position_at_end(loop_condition_block)
        condition = self.visitExpression(ctx.getChild(2))
        self.builder.cbranch(condition, loop_block, end_block)
        self.builder.position_at_end(loop_block)
        self.visitStatement(ctx.getChild(4))
        self.builder.branch(loop_condition_block)
        self.builder.position_at_end(end_block)
        self.while_counter += 1

    def visitStructDefinition(self, ctx):
        struct_name = ctx.getChild(1).getText()
        types = self.visitChildren(ctx)
        struct_type = ir.LiteralStructType(types)

        struct_global = ir.GlobalVariable(self.module, struct_type, name=struct_name)
        struct_global.global_constant = True
        struct_global.initializer = None

    def visitStructBlock(self, ctx):
        return [self.get_llvm_type(ctx.getChild(i).getText()) for i in range(1, ctx.getChildCount()-1, 3)]

    def visitStructDeclaration(self, ctx):
        print(ctx.getText())
        return self.visitChildren(ctx)