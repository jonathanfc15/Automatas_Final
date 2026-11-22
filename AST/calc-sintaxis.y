%code requires {
    #include "ast.h"
}
%{
#include <stdio.h>
#include <stdlib.h>
#include "ast.h"

int yylex(void);
void yyerror(const char *s);
extern FILE *yyin;
extern int yylineno;
%}

%union {
    Nodo *nodo;
    char *str;
    int num;
}

%token <str> ID
%token <num> NUMERO
%token INT BOOL VOID TRUE FALSE RETURN MAIN
%token PARA PARC LLAA LLAC PYC COMA
%token OP_RESTA OP_SUMA OP_MAYOR OP_MENOR OP_AND OP_OR
%token OP_DIV OP_MULT OP_IGUAL OP_ASIGN

%type <nodo> CODIGO SENTENCIA DECLARACION VAR VARS E
%start prog

%left OP_OR
%left OP_AND
%nonassoc OP_IGUAL OP_MAYOR OP_MENOR
%left OP_SUMA OP_RESTA
%left OP_MULT OP_DIV

%%
prog:
    TIPOM MAIN PARA PARC LLAA CODIGO LLAC {
        if (exportar_dot($6, "ast_tree") != 0)
            fprintf(stderr, "No se pudo generar ast_tree.dot/ast_tree.png\n");
        printf("\nArbol sintactico abstracto:\n");
        imprimir_nodo($6, 0);
        printf("\nResultado: %d\n", interpretar_programa($6));
        nodo_libre($6);
    }
;

TIPOM: INT | BOOL | VOID ;

CODIGO:
    %empty               { $$ = NULL; }
  | DECLARACION CODIGO   { $$ = nodo_seq($1, $2); }
  | SENTENCIA CODIGO     { $$ = nodo_seq($1, $2); }
;

DECLARACION: TIPO VARS PYC { $$ = $2; } ;
VARS:
    VAR                 { $$ = $1; }
  | VAR COMA VARS       { $$ = nodo_seq($1, $3); }
;
VAR:
    ID                 { $$ = nodo_decl($1, NULL); free($1); }
  | ID OP_ASIGN E      { $$ = nodo_decl($1, $3); free($1); }
;
TIPO: INT | BOOL ;

SENTENCIA:
    ID OP_ASIGN E PYC   { $$ = nodo_assign($1, $3); free($1); }
  | RETURN PYC          { $$ = nodo_return(NULL); }
  | RETURN E PYC        { $$ = nodo_return($2); }
;

E:
    E OP_SUMA E         { $$ = nodo_opBin(TOP_SUMA, $1, $3); }
  | E OP_RESTA E        { $$ = nodo_opBin(TOP_RESTA, $1, $3); }
  | E OP_MULT E         { $$ = nodo_opBin(TOP_MULT, $1, $3); }
  | E OP_DIV E          { $$ = nodo_opBin(TOP_DIV, $1, $3); }
  | E OP_IGUAL E        { $$ = nodo_opBin(TOP_IGUAL, $1, $3); }
  | E OP_MAYOR E        { $$ = nodo_opBin(TOP_MAYOR, $1, $3); }
  | E OP_MENOR E        { $$ = nodo_opBin(TOP_MENOR, $1, $3); }
  | E OP_AND E          { $$ = nodo_opBin(TOP_AND, $1, $3); }
  | E OP_OR E           { $$ = nodo_opBin(TOP_OR, $1, $3); }
  | PARA E PARC         { $$ = $2; }
  | ID                  { $$ = nodo_ID($1); free($1); }
  | NUMERO              { $$ = nodo_int($1); }
  | TRUE                { $$ = nodo_bool(1); }
  | FALSE               { $$ = nodo_bool(0); }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintactico en linea %d: %s\n", yylineno, s);
}

int main(int argc, char **argv) {
    if (argc > 2) {
        fprintf(stderr, "Uso: %s [archivo_de_entrada]\n", argv[0]);
        return EXIT_FAILURE;
    }
    if (argc == 2) {
        yyin = fopen(argv[1], "r");
        if (!yyin) { perror(argv[1]); return EXIT_FAILURE; }
    }
    int resultado = yyparse();
    if (argc == 2) fclose(yyin);
    return resultado == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
