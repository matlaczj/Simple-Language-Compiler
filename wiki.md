## Helpful links
http://lab.antlr.org/

## Generating parse-tree
```bash
antlr4-parse /workspaces/simple_lang_compiler/src/SimpleLang.g4 program -gui
```
```bash
antlr4-parse /workspaces/simple_lang_compiler/src/SimpleLang.g4 program -gui input.txt
```

## Generating python3 parser, lexer, visitor
```bash
    antlr4 -Dlanguage=Python3 -visitor /workspaces/simple_lang_compiler/src/SimpleLang.g4 -o /workspaces/simple_lang_compiler/src
```