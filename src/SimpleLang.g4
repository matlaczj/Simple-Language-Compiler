grammar SimpleLang;

// Parser rules
program: statement*;

statement:
	assignment
	| printStatement
	| conditionalStatement
	| loopStatement
	| functionDeclaration;

assignment: ID '=' expression ';';

printStatement: 'print' expression ';';

conditionalStatement:
	'if' expression '{' statement* '}' (
		'else' '{' statement* '}'
	)?;

loopStatement: 'while' expression '{' statement* '}';

functionDeclaration:
	'function' ID '(' parameters? ')' '{' statement* '}';

parameters: ID (',' ID)*;

expression:
	expression ('*' | '/' | '+' | '-') expression
	| '(' expression ')'
	| ID '(' arguments? ')'
	| INT
	| FLOAT
	| STRING
	| ID
	| ID '[' expression ']';

arguments: expression (',' expression)*;

// Lexer rules
ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]*;
STRING: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
