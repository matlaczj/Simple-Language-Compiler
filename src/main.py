# type: ignore

import antlr4
from antlr.MinLangParser import MinLangParser
from antlr.MinLangLexer import MinLangLexer
from LLVMCodeGenerator import LLVMCodeGenerator
from source_code import SOURCE_CODE

# Generate LLVM IR code
lexer = MinLangLexer(antlr4.InputStream(SOURCE_CODE))
token_stream = antlr4.CommonTokenStream(lexer)
parser = MinLangParser(token_stream)
parse_tree = parser.program()
generator = LLVMCodeGenerator()
generator.visit(parse_tree)
llvm_ir_code = generator.module

# Save LLVM IR code to file
# pylint: disable=unspecified-encoding
with open("/workspaces/simple_lang_compiler/src/output.ll", "w") as file:
    file.write(str(llvm_ir_code))
