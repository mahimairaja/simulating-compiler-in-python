/* 
To run the program :
>> lex 4-token-separation.l
>> gcc lex.yy.c -o out
>> ./out
>> int main ( ) { }
* --- Output on console --- *
>> < Keyword : int >
>> < Keyword : main >
>> < Punctuation : ( >
>> < Punctuation : ) >
>> < Punctuation : { >
>> < Punctuation : } >
 */


/* Declaration */
%{ 
#include<stdio.h>
int keyCount = 0;
int opCount = 0;
int puncCount = 0;
int idCount = 0;
int constCount = 0;
%}

/* Rules */
%%
bool|int|float|main|return {keyCount++; printf("< Keyword : %s >\n", yytext);}
[!%^&*=+]+ {opCount++; printf("< Operators : %s >\n", yytext);}
[,.'"(){};]+ {puncCount++; printf("< Punctuation : %s >\n", yytext);}
[a-zA-Z]+ {idCount++; printf("< Identifier : %s >\n", yytext);}
[-,+]?[0-9] {constCount++; printf("< Constant : %s >\n", yytext);}
%%


int yywrap(void){
    printf("\n- _ - _ - Count - _ - _ -\n");
    printf("< Keyword count: %d\n", keyCount);
    printf("Operators count: %d\n", opCount);
    printf("Punctuation count: %d\n", puncCount);
    printf("Identifier count: %d\n", idCount);
    printf("Constant count: %d\n", constCount);
    fflush(stdout);
    return 1;
}

int main()
{
    yylex();
    return 0;
}
