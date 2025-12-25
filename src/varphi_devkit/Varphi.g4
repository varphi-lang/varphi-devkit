grammar Varphi;

// ======================================================
// PARSER RULES
// ======================================================

program : NEWLINE* transition (NEWLINE+ transition)* NEWLINE* EOF;

transition : current_state=state_id read_symbols next_state=state_id write_symbols shift_directions;

read_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

write_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

shift_directions : LPAREN direction (COMMA direction)* RPAREN;

// States can be named "scan" (ID) or just "s" (ALPHANUM).
// We must allow both because the Lexer forces single chars into ALPHANUM.
state_id : ID | ALPHANUM | LEFT_KW | RIGHT_KW | STAY_KW | BLANK_KW;

// Symbols are a single alphanumeric, BLANK, or *
symbol : ALPHANUM | BLANK_KW | STAR;

direction : LEFT_KW | RIGHT_KW | STAY_KW;

// ======================================================
// LEXER RULES
// ======================================================

LPAREN : '(';
RPAREN : ')';
COMMA  : ',';
STAR   : '*';

// Keywords
LEFT_KW  : 'LEFT';
RIGHT_KW : 'RIGHT';
STAY_KW  : 'STAY';
BLANK_KW : 'BLANK';

// ------------------------------------------------------
// PRIORITY RULES
// ------------------------------------------------------

// Single Alphanumeric Character
ALPHANUM : [a-zA-Z0-9];

// Identifier (Multi-char or containing underscore)
ID : [a-zA-Z0-9_]+;

// ------------------------------------------------------

COMMENT       : '//' ~[\r\n]* -> skip;
MULTI_COMMENT : '/*' .*? '*/' -> skip;
WS            : [ \t]+ -> skip;
NEWLINE       : '\r'? '\n';