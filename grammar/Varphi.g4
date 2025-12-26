grammar Varphi;

// ======================================================
// PARSER RULES
// ======================================================

program : NEWLINE* transition (NEWLINE+ transition)* NEWLINE* EOF;

transition : current_state=state_id read_symbols next_state=state_id write_symbols shift_directions;

read_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

write_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

shift_directions : LPAREN direction (COMMA direction)* RPAREN;

state_id : ID | ALPHANUM | LEFT_KW | RIGHT_KW | STAY_KW | BLANK_KW;

// Updated: Symbol can now be a Variable instead of STAR
symbol : ALPHANUM | BLANK_KW | VARIABLE;

direction : LEFT_KW | RIGHT_KW | STAY_KW;

// ======================================================
// LEXER RULES
// ======================================================

LPAREN : '(';
RPAREN : ')';
COMMA  : ',';
// STAR rule removed

// New Lexer Rule for Variables (e.g., $x, $val_1)
VARIABLE : '$' [a-zA-Z0-9_]+;

// Keywords
LEFT_KW  : 'LEFT';
RIGHT_KW : 'RIGHT';
STAY_KW  : 'STAY';
BLANK_KW : 'BLANK';

// ------------------------------------------------------
// PRIORITY RULES
// ------------------------------------------------------

ALPHANUM : [a-zA-Z0-9];
ID : [a-zA-Z0-9_]+;

// ------------------------------------------------------

COMMENT       : '//' ~[\r\n]* -> skip;
MULTI_COMMENT : '/*' .*? '*/' -> skip;
WS            : [ \t]+ -> skip;
NEWLINE       : '\r'? '\n';