grammar SimpleLang;

// PARSER RULES
program: statement*;

statement:
	assignment
	| conditionalStatement
	| loopStatement
	| functionDeclaration
	| printStatement
	| readStatement;

declaration: typed_id ';';

typed_id: type ID;

type: 'int' | 'float' | 'string' | 'bool';

assignment: ID '=' expression ';';

conditionalStatement:
	'if' expression '{' statement* '}' (
		'else' '{' statement* '}'
	)?;

loopStatement: 'while' expression '{' statement* '}';

functionDeclaration:
	'function' typed_id '(' parameters? ')' '{' statement* '}';

parameters: typed_id (',' typed_id)*;

printStatement: 'print' expression ';';

readStatement: 'read' ID ';';

expression:
	expression (
		'*'
		| '/'
		| '+'
		| '-'
		| '=='
		| '!='
		| '<'
		| '>'
		| '<='
		| '>='
	) expression
	| '(' expression ')'
	| functionCall
	| INT
	| FLOAT
	| STRING
	| BOOL
	| ID;

functionCall: ID '(' arguments? ')';

arguments: expression (',' expression)*;

// LEXER RULES
ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]*;
STRING: '"' .*? '"';
BOOL: 'true' | 'false';
WHITESPACE: [ \t\r\n]+ -> skip;
COMMENT: '//' .*? '\n' -> skip;
