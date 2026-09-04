grammar Varphi;

// --- PARSER RULES ---

program : NEWLINE* transition (NEWLINE+ transition)* NEWLINE* EOF;

transition : current_state=state_id read_symbols next_state=state_id write_symbols shift_directions;

read_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

write_symbols : LPAREN symbol (COMMA symbol)* RPAREN;

shift_directions : LPAREN direction (COMMA direction)* RPAREN;

state_id : WORD | INT | HEX | LEFT_KW | RIGHT_KW | STAY_KW | BLANK_KW;

symbol : WORD | INT | HEX | LEFT_KW | RIGHT_KW | STAY_KW | BLANK_KW | VARIABLE;

direction : LEFT_KW | RIGHT_KW | STAY_KW;

// --- LEXER RULES ---

LPAREN : '(';
RPAREN : ')';
COMMA  : ',';

VARIABLE : '$' [a-zA-Z0-9_]+;

LEFT_KW  : 'LEFT';
RIGHT_KW : 'RIGHT';
STAY_KW  : 'STAY';
BLANK_KW : 'BLANK';

HEX : '0x' [0-9a-fA-F]+;

INT : [0-9]+;

COMMENT       : '//' ~[\r\n]* -> skip;
MULTI_COMMENT : '/*' .*? '*/' -> skip;
WHITESPACE    : [ \t]+ -> skip;
NEWLINE       : '\r'? '\n';

WORD : ~[ \t\r\n(),]+;