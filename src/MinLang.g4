grammar MinLang;

// PARSER RULES
program: statement+;

statement:
	declarationStatement
	| assignmentStatement
	| printStatement
	| readStatement
    | functionDeclaration
    | functionCall
    | ifStatement
    | whileLoop;

declarationStatement: type id ';';
assignmentStatement: id '=' expression ';';
id: ID;

expression:
	expression operator expression
    | '(' expression ')'
	| literal
	| id
    | functionCall;

literal: INT | FLOAT | BOOL | STRING;

operator:
	arithmeticOperator | relationalOperator;

arithmeticOperator:
    '+'
    | '-'
    | '*'
    | '/';

relationalOperator:
    '>'
    | '<'
    | '>='
    | '<='
    | '=='
    | '!=';

functionDeclaration: 'function' type id '(' parameterList ')' return_block;
parameterList: typed_id (',' typed_id)*;
typed_id: type id;
return_block: '{' statement* returnStatement '}';
returnStatement: 'return' expression ';';
functionCall: id '(' argumentList ')';
argumentList: expression (',' expression)*;

block: '{' statement* '}';
ifStatement: 'if' '(' expression ')' block 'else' block;
whileLoop: 'while' '(' expression ')' block;

type: 'int' | 'float' | 'bool' | 'string';
printStatement: 'print' expression ';';
readStatement: 'read' id ';';

// LEXER RULES
WHITESPACE: [ \t\r\n]+ -> skip;
COMMENT: '//' .*? '\n' -> skip;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]*;
STRING: '"' .*? '"';
BOOL: 'true' | 'false';
ID: [a-zA-Z_][a-zA-Z0-9_]*;
