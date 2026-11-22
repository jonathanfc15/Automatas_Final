%option noyywrap yylineno nounput noinput
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "calc-sintaxis.tab.h"
%}

%%
"//"[^\n]*                 ;
"/*"([^*]|\*+[^*/])*\*+"/"  ;
"int"                      { return INT; }
"bool"                     { return BOOL; }
"void"                     { return VOID; }
"main"                     { return MAIN; }
"true"                     { return TRUE; }
"false"                    { return FALSE; }
"return"                   { return RETURN; }
"&&"                       { return OP_AND; }
"||"                       { return OP_OR; }
"=="                       { return OP_IGUAL; }
"="                        { return OP_ASIGN; }
">"                        { return OP_MAYOR; }
"<"                        { return OP_MENOR; }
"+"                        { return OP_SUMA; }
"-"                        { return OP_RESTA; }
"*"                        { return OP_MULT; }
"/"                        { return OP_DIV; }
"("                        { return PARA; }
")"                        { return PARC; }
"{"                        { return LLAA; }
"}"                        { return LLAC; }
";"                        { return PYC; }
","                        { return COMA; }
[0-9]+                     { yylval.num = atoi(yytext); return NUMERO; }
[a-zA-Z_][a-zA-Z0-9_]*     {
                               yylval.str = malloc((size_t)yyleng + 1);
                               if (!yylval.str) { perror("malloc"); exit(EXIT_FAILURE); }
                               memcpy(yylval.str, yytext, (size_t)yyleng + 1);
                               return ID;
                           }
[ \t\r\n]+                 ;
.                          { fprintf(stderr, "Caracter no reconocido en linea %d: %s\n", yylineno, yytext); return yytext[0]; }
%%
