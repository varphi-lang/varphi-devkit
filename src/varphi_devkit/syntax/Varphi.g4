grammar Varphi;

// ======================================================
// PARSER RULES
// ======================================================

program     : (line? NEWLINE)* line? EOF;

line        : state input_tuple state write_tuple move_tuple;

input_tuple : LPAREN tape_char (COMMA tape_char)* RPAREN;

write_tuple : LPAREN tape_char (COMMA tape_char)* RPAREN;

move_tuple  : LPAREN direction (COMMA direction)* RPAREN;

state       : ID | LEFT_KW | RIGHT_KW | STAY_KW;

tape_char   : CHAR_LITERAL;

direction   : LEFT_KW | RIGHT_KW | STAY_KW;

// ======================================================
// LEXER RULES
// ======================================================

LPAREN : '(';
RPAREN : ')';
COMMA  : ',';

LEFT_KW  : 'LEFT';
RIGHT_KW : 'RIGHT';
STAY_KW  : 'STAY';

// Matches 'x' (1 char) OR '' (0 chars)
CHAR_LITERAL : '\'' .? '\''; 

ID : ~[ \t\r\n(),']+;

COMMENT       : '//' ~[\r\n]* -> skip;
MULTI_COMMENT : '/*' .*? '*/' -> skip;
WS            : [ \t]+ -> skip;
NEWLINE       : '\r'? '\n';