#ifndef AST_H
#define AST_H

typedef enum {
    NODO_DECL, NODO_ASSIGN, NODO_RETURN, NODO_OP,
    NODO_INT, NODO_BOOL, NODO_ID, NODO_SEQ
} TipoNodo;

typedef enum {
    TOP_SUMA, TOP_RESTA, TOP_MULT, TOP_DIV,
    TOP_IGUAL, TOP_OR, TOP_AND, TOP_MAYOR, TOP_MENOR
} TipoOP;

typedef struct Nodo {
    TipoNodo tipo;
    union {
        int val_int;
        int val_bool;
        char *nombre;
        struct { struct Nodo *izq, *der; TipoOP op; } opBinaria;
        struct { char *id; struct Nodo *expr; } assign;
        struct Nodo *ret_expr;
    };
} Nodo;

Nodo *nodo_ID(const char *nombre);
Nodo *nodo_int(int valor);
Nodo *nodo_bool(int valor);
Nodo *nodo_opBin(TipoOP op, Nodo *izq, Nodo *der);
Nodo *nodo_assign(const char *id, Nodo *expr);
Nodo *nodo_return(Nodo *expr);
Nodo *nodo_seq(Nodo *primero, Nodo *resto);
Nodo *nodo_decl(const char *id, Nodo *expr);
void nodo_libre(Nodo *nodo);
int exportar_dot(const Nodo *nodo, const char *nombre_base);
void imprimir_nodo(const Nodo *nodo, int nivel);
int interpretar_programa(const Nodo *programa);

#endif
