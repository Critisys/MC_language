// 1711700

grammar MC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program  : decl+ EOF ;

decl: var_decl|func_decl ;

prim_type: INTTYPE|STRINGTYPE|FLOATTYPE|BOOLTYPE;

one_id: ID (LSB INTLIT RSB)? ;

var_decl: prim_type one_id (CM one_id)* SEMI;

func_decl: all_type ID LB para_list RB block_stmt;

all_type: prim_type (LSB RSB)? | VOIDTYPE; 

para_list: (para(CM para)*)?;

para: prim_type ID (LSB RSB)?;

exp: exp1 ASSIGN exp|exp1;

exp1: exp1 OR exp2|exp2;

exp2: exp2 AND exp3|exp3;

exp3: exp4 (EQUAL|NEQUAL) exp4|exp4;

exp4: exp5 (LESS|LESSEQ|GREATEQ|GREATER) exp5|exp5;

exp5: exp5 (ADD|SUB) exp6|exp6;

exp6: exp6 (MUL|DIV|MOD) exp7|exp7;

exp7: (SUB|NOT) exp7|indexexp;

indexexp:  exp8 LSB exp RSB| exp8;

funcall: ID LB (exp (CM exp)*)? RB; 

exp8: LB exp RB|ID|literal|funcall;

literal: INTLIT|STRINGLIT|BOOLLIT|FLOATLIT;

stmt:if_stmt|for_stmt|dowhile_stmt|break_stmt|continue_stmt|return_stmt|exp SEMI|block_stmt ;

other_stmt: for_stmt|dowhile_stmt|break_stmt|continue_stmt|return_stmt|exp SEMI|block_stmt ;

if_stmt: match_if|unmatch_if ;

match_if: IF LB exp RB (match_if|other_stmt) ELSE stmt;

unmatch_if: IF LB exp RB stmt ;

for_stmt: FOR LB exp SEMI exp SEMI exp RB stmt ;

dowhile_stmt: DO stmt+ WHILE exp SEMI ;

break_stmt: BREAK SEMI;

continue_stmt: CONTINUE SEMI;

return_stmt: RETURN (exp)? SEMI;

block_stmt: LP body* RP ;

body: var_decl|stmt ;




INTTYPE: 'int' ;

VOIDTYPE: 'void' ;

STRINGTYPE: 'string' ;

FLOATTYPE:'float' ;

BOOLTYPE: 'boolean';


LB: '(' ;

RB: ')' ;

LP: '{' ;

RP: '}' ;

LSB: '[' ;

RSB: ']' ;

CM: ',' ;

SEMI: ';' ;

IF: 'if' ;

ELSE: 'else' ;

FOR: 'for' ;

DO: 'do' ;

WHILE: 'while';

BREAK: 'break' ;

CONTINUE: 'continue' ;

RETURN: 'return';

ADD: '+';

SUB: '-';

MUL: '*';

DIV: '/';

MOD: '%';

NOT: '!';

OR: '||';

AND: '&&';

EQUAL: '==';

NEQUAL: '!=';

ASSIGN: '=';

LESS: '<';

GREATER: '>';

LESSEQ: '<=';

GREATEQ: '>=';

BOOLLIT: 'true'|'false';

ID: [_a-zA-Z][_a-zA-Z0-9]*;

INTLIT: [0-9]+;

fragment EXPONENT: [eE] '-'? [0-9]+;

FLOATLIT:   [0-9]+ '.' [0-9]* EXPONENT?
            |[0-9]+'.'?[0-9]* EXPONENT
            |[0-9]*'.'[0-9]+ EXPONENT?
            |[0-9]*'.'?[0-9]+ EXPONENT ;

    
fragment ESCSEQ: '\\'[bfrnt"\\];

COMMENT: '/*'.*? '*/' -> skip;

LINECOMMENT: '//' ~[\r\n]* ->skip;

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs, newlines, formfeed


ERROR_CHAR: .{
    raise ErrorToken(self.text)
};

STRINGLIT: '"' (ESCSEQ|~[\r\n"\\])* '"'
    {
        s=self.text[1:-1]
        self.text=s
    } ;

ILLEGAL_ESCAPE
    : '"' (ESCSEQ| ~["\\])*? ([\\] ~[bfrnt'"\\]) 
        {
           raise IllegalEscape(self.text[1:])
        }
    ;
UNCLOSE_STRING
    :  '"' (ESCSEQ | ~["\r\n])* ('\n'| EOF)
        {
            if self.text[-1]=='\n':
                 raise UncloseString(self.text[1:-1])
            else:
                raise UncloseString(self.text[1:])
        }
    ;
