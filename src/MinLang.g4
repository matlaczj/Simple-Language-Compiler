grammar MinLang;

// PARSER RULES
program: statement+;

statement:
	declarationStatement
	| assignmentStatement
	| printStatement
	| readStatement;

declarationStatement: type id ';';
assignmentStatement: id '=' expression ';';
id: ID;

expression:
	expression operator expression
    | '(' expression ')'
	| literal
	| id;

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
