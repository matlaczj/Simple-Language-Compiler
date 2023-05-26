grammar SimpleLang;

// PARSER RULES
program: statement+;

statement:
	declaration
	| assignment
	| loopStatement
	| functionDeclaration
	| functionCall
	| conditionalStatement
	| printStatement
	| readStatement;

declaration: typed_id ';';
typed_id: type id;

assignment: id '=' value ';';

value: expression;
id: ID;

expression:
	expression operator expression
	| INT
	| FLOAT
	| BOOL
	| STRING
	| id
	| functionCall
	| expression operator '(' expression ')';

operator:
	'+'
	| '-'
	| '*'
	| '/'
	| '>'
	| '<'
	| '>='
	| '<='
	| '==';

type: 'int' | 'float' | 'bool' | 'string';

conditionalStatement:
	'if' expression '{' statement* '}' (
		'else' '{' statement* '}'
	)?;

loopStatement: 'while' expression '{' statement* '}';

functionDeclaration:
	'function' typed_id '(' parameters? ')' '{' statement* 'return' expression ';' '}';
parameters: typed_id (',' typed_id)*;

printStatement: 'print' expression ';';

readStatement: 'read' ID ';';

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
