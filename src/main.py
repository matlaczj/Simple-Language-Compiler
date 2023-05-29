# type: ignore
import antlr4
from llvmlite import ir
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from source_code import SOURCE_CODE

ruleNames = [
    "program",
    "statement",
    "declaration",
    "typed_id",
    "assignment",
    "value",
    "id",
    "expression",
    "operator",
    "type",
    "conditionalStatement",
    "loopStatement",
    "functionDeclaration",
    "parameters",
    "printStatement",
    "readStatement",
    "functionCall",
    "arguments",
]

convert = {
    "int": ir.IntType(32),
    "float": ir.FloatType(),
}


class SimpleLangVisitorImpl(SimpleLangVisitor):
    def __init__(self):
        self.module = ir.Module()
        self.variables = {}
        main_function_type = ir.FunctionType(ir.IntType(32), [])
        main_function = ir.Function(self.module, main_function_type, name="main")
        entry_block = main_function.append_basic_block(name="entry")
        # Set the IRBuilder to the entry block of the main function
        self.builder = ir.IRBuilder(entry_block)

    def visitProgram(self, ctx: SimpleLangParser.ProgramContext):
        for statement_ctx in ctx.statement():
            self.visit(statement_ctx)

    def visitDeclaration(self, ctx: SimpleLangParser.DeclarationContext):
        typed_id_ctx = ctx.typed_id()
        var_type = convert[self.visit(typed_id_ctx.type_())]
        var_name = typed_id_ctx.id_().getText()
        # Generate IR for declaration
        variable = self.builder.alloca(var_type, name=var_name)
        self.variables[var_name] = (variable, var_type)
        print(f"Declare variable: {var_type} {var_name} {variable}")

    def visitAssignment(self, ctx: SimpleLangParser.AssignmentContext):
        var_name = ctx.id_().getText()
        value = self.visit(ctx.value())
        # Generate IR for assignment
        print(f"Assign {value} to variable: {var_name}")
        self.builder.store(
            ir.Constant(self.variables[var_name][1], 1), self.variables[var_name][0]
        )

    def visitTyped_id(self, ctx: SimpleLangParser.Typed_idContext):
        return self.visit(ctx.type_())

    def visitExpression(self, ctx: SimpleLangParser.ExpressionContext):
        if ctx.operator():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            op = ctx.operator().getText()
            # Generate IR for binary expression
            result = f"{left} {op} {right}"
            print(f"Evaluate expression: {result}")
            return result
        elif ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.BOOL():
            return ctx.BOOL().getText()
        elif ctx.STRING():
            return ctx.STRING().getText()[1:-1]
        elif ctx.id_():
            return ctx.id_().getText()
        elif ctx.functionCall():
            return self.visit(ctx.functionCall())
        elif ctx.expression():
            return (
                self.visit(ctx.expression(0))
                + "("
                + self.visit(ctx.expression(1))
                + ")"
            )

    def visitOperator(self, ctx: SimpleLangParser.OperatorContext):
        return ctx.getText()

    def visitType(self, ctx: SimpleLangParser.TypeContext):
        return ctx.getText()

    def visitConditionalStatement(
        self, ctx: SimpleLangParser.ConditionalStatementContext
    ):
        condition = self.visit(ctx.expression())
        # Generate IR for conditional statement
        print(f"Evaluate condition: {condition}")
        self.visitChildren(ctx)

    def visitLoopStatement(self, ctx: SimpleLangParser.LoopStatementContext):
        condition = self.visit(ctx.expression())
        # Generate IR for loop statement
        print(f"Loop until condition: {condition}")
        self.visitChildren(ctx)

    def visitFunctionDeclaration(
        self, ctx: SimpleLangParser.FunctionDeclarationContext
    ):
        typed_id_ctx = ctx.typed_id()
        function_name = typed_id_ctx.id_().getText()
        parameters_ctx = ctx.parameters()
        parameters = ""
        if parameters_ctx:
            parameters = self.visit(parameters_ctx)
        # Generate IR for function declaration
        print(f"Declare function: {function_name}({parameters})")
        self.visitChildren(ctx)

    def visitParameters(self, ctx: SimpleLangParser.ParametersContext):
        params = []
        for typed_id_ctx in ctx.typed_id():
            param_type = self.visit(typed_id_ctx.type_())
            param_name = typed_id_ctx.id_().getText()
            params.append(f"{param_type} {param_name}")
        return ", ".join(params)

    def visitPrintStatement(self, ctx: SimpleLangParser.PrintStatementContext):
        value = self.visit(ctx.expression())
        # Generate IR for print statement
        print(f"Print: {value}")

    def visitReadStatement(self, ctx: SimpleLangParser.ReadStatementContext):
        var_name = ctx.ID().getText()
        # Generate IR for read statement
        print(f"Read input into variable: {var_name}")

    def visitFunctionCall(self, ctx: SimpleLangParser.FunctionCallContext):
        function_name = ctx.ID().getText()
        arguments_ctx = ctx.arguments()
        arguments = ""
        if arguments_ctx:
            arguments = self.visit(arguments_ctx)
        # Generate IR for function call
        result = f"{function_name}({arguments})"
        print(f"Call function: {result}")
        return result

    def visitArguments(self, ctx: SimpleLangParser.ArgumentsContext):
        arg_values = []
        for expression_ctx in ctx.expression():
            arg_values.append(self.visit(expression_ctx))
        return ", ".join(arg_values)

    def visitStatement(self, ctx: SimpleLangParser.StatementContext):
        self.visitChildren(ctx)


# Main program
lexer = SimpleLangLexer(antlr4.InputStream(SOURCE_CODE))
token_stream = antlr4.CommonTokenStream(lexer)
parser = SimpleLangParser(token_stream)
parse_tree = parser.program()
visitor = SimpleLangVisitorImpl()
visitor.visit(parse_tree)

print(visitor.module)  # LLVM
