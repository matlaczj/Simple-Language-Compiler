# simple_lang_compiler

The aim of the project is to independently design a very simple programming language and implement its compiler. The project covers all stages of source code processing, up to the creation of machine code. Tools supporting the work of the compiler developer should be used.

The front end of the compiler, i.e. the lexical-syntactic analysis should be performed using the **ANTLR** analyzer generator or other similar tools. From the resulting **AST** tree, an intermediate representation (**IR**) in a form compliant with the **LLVM** specification should be generated. The optimization of the intermediate representation as well as the generation of the machine code will be performed by the tool available in LLVM.

## Stage 1: Simple Variable Operations (15 pts)
### Minimum requirements (10 points):
- support for two types of variables: integer, real,
- basic support for standard input-output (e.g. read and print commands),
- support for basic arithmetic operations,
- identifying errors during lexical and syntactic analysis.
### Extensions:
- support for array variables (3 points),
- number matrix support (5 points),
- support for logical values (2 points),
- support for numbers with different precision (e.g. Float32, Float64) (5 points),
- support for the type of string (string) (3 points).

## Stage 2: Program flow control (15 pts)
For the final defense of the project, bring a printed **short manual** of the designed language. The manual should describe the syntax of the language, its capabilities and limitations from the user's point of view.
### Minimum requirements (10 points):
- conditional statement, loop,
- the ability to create functions,
- variable scope support (local and global).
### Suggested extensions:
- support for structures (5 points),
- class support (5 points),
- dynamic typing (values in boxes) (5 points).

# installation
- install docker
- install vscode
- install "ms-vscode-remote.remote-containers" extention in vscode
- reload window
- accept to reopen in dev container
- wait for installation and be patient
- congrats, now your development environment is under your full control