## Helpful links
http://lab.antlr.org/
https://alive2.llvm.org/ce/

## Generating parse-tree
```bash
antlr4-parse /workspaces/simple_lang_compiler/src/MinLang.g4 program -gui
```
```bash
antlr4-parse /workspaces/simple_lang_compiler/src/MinLang.g4 program -gui /workspaces/simple_lang_compiler/src/input.txt
```

## Generating python3 parser, lexer, visitor
```bash
    antlr4 -Dlanguage=Python3 -visitor /workspaces/simple_lang_compiler/src/MinLang.g4 -o /workspaces/simple_lang_compiler/src/antlr
```