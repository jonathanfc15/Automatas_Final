#define _POSIX_C_SOURCE 200809L
#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void *reservar(size_t tam) {
    void *p = calloc(1, tam);
    if (!p) { perror("calloc"); exit(EXIT_FAILURE); }
    return p;
}
static char *copiar(const char *s) {
    size_t n = strlen(s) + 1;
    char *p = reservar(n);
    memcpy(p, s, n);
    return p;
}
static Nodo *nuevo(TipoNodo tipo) {
    Nodo *n = reservar(sizeof(*n));
    n->tipo = tipo;
    return n;
}
Nodo *nodo_ID(const char *s) { Nodo *n=nuevo(NODO_ID); n->nombre=copiar(s); return n; }
Nodo *nodo_int(int v) { Nodo *n=nuevo(NODO_INT); n->val_int=v; return n; }
Nodo *nodo_bool(int v) { Nodo *n=nuevo(NODO_BOOL); n->val_bool=v; return n; }
Nodo *nodo_opBin(TipoOP op, Nodo *a, Nodo *b) {
    Nodo *n=nuevo(NODO_OP); n->opBinaria.op=op; n->opBinaria.izq=a; n->opBinaria.der=b; return n;
}
Nodo *nodo_assign(const char *s, Nodo *e) {
    Nodo *n=nuevo(NODO_ASSIGN); n->assign.id=copiar(s); n->assign.expr=e; return n;
}
Nodo *nodo_decl(const char *s, Nodo *e) {
    Nodo *n=nuevo(NODO_DECL); n->assign.id=copiar(s); n->assign.expr=e; return n;
}
Nodo *nodo_return(Nodo *e) { Nodo *n=nuevo(NODO_RETURN); n->ret_expr=e; return n; }
Nodo *nodo_seq(Nodo *a, Nodo *b) {
    Nodo *n=nuevo(NODO_SEQ); n->opBinaria.izq=a; n->opBinaria.der=b; return n;
}
void nodo_libre(Nodo *n) {
    if (!n) return;
    switch(n->tipo) {
        case NODO_SEQ: case NODO_OP:
            nodo_libre(n->opBinaria.izq); nodo_libre(n->opBinaria.der); break;
        case NODO_DECL: case NODO_ASSIGN:
            free(n->assign.id); nodo_libre(n->assign.expr); break;
        case NODO_RETURN: nodo_libre(n->ret_expr); break;
        case NODO_ID: free(n->nombre); break;
        default: break;
    }
    free(n);
}
static const char *operador(TipoOP op) {
    switch(op) {
        case TOP_SUMA: return "+"; case TOP_RESTA: return "-";
        case TOP_MULT: return "*"; case TOP_DIV: return "/";
        case TOP_IGUAL: return "=="; case TOP_OR: return "||";
        case TOP_AND: return "&&"; case TOP_MAYOR: return ">";
        case TOP_MENOR: return "<";
    }
    return "?";
}
static void etiqueta(const Nodo *n, char *buf, size_t tam) {
    switch(n->tipo) {
        case NODO_SEQ: snprintf(buf,tam,"SEQ"); break;
        case NODO_DECL: snprintf(buf,tam,"DECL %s",n->assign.id); break;
        case NODO_ASSIGN: snprintf(buf,tam,"ASSIGN %s",n->assign.id); break;
        case NODO_RETURN: snprintf(buf,tam,"RETURN"); break;
        case NODO_OP: snprintf(buf,tam,"%s",operador(n->opBinaria.op)); break;
        case NODO_INT: snprintf(buf,tam,"%d",n->val_int); break;
        case NODO_BOOL: snprintf(buf,tam,"%s",n->val_bool?"true":"false"); break;
        case NODO_ID: snprintf(buf,tam,"%s",n->nombre); break;
    }
}
/* Escapar etiquetas para que nombres especiales no rompan el formato DOT. */
static void escribir_etiqueta(FILE *f, const char *s) {
    for (; *s; ++s) {
        if (*s=='"' || *s=='\\') fputc('\\',f);
        if (*s=='\n') { fputs("\\n",f); continue; }
        fputc(*s,f);
    }
}
static int escribir_rec(FILE *f, const Nodo *n, int *contador) {
    if (!n) return -1;
    int id=(*contador)++;
    char buf[256]; etiqueta(n,buf,sizeof(buf));
    fprintf(f,"  nodo%d [label=\"",id);
    escribir_etiqueta(f,buf);
    if (n->tipo==NODO_SEQ) fputs("\", fillcolor=lightgray];\n",f);
    else if (n->tipo==NODO_RETURN) fputs("\", fillcolor=lightpink];\n",f);
    else fputs("\"];\n",f);
    const Nodo *a=NULL,*b=NULL;
    if (n->tipo==NODO_SEQ || n->tipo==NODO_OP) {
        a=n->opBinaria.izq; b=n->opBinaria.der;
    } else if (n->tipo==NODO_DECL || n->tipo==NODO_ASSIGN) a=n->assign.expr;
    else if (n->tipo==NODO_RETURN) a=n->ret_expr;
    if (a) { int hijo=escribir_rec(f,a,contador); fprintf(f,"  nodo%d -> nodo%d;\n",id,hijo); }
    if (b) { int hijo=escribir_rec(f,b,contador); fprintf(f,"  nodo%d -> nodo%d%s;\n",id,hijo,n->tipo==NODO_SEQ?" [style=dashed]":""); }
    return id;
}
int exportar_dot(const Nodo *n, const char *base) {
    char dot[512],png[512],cmd[1200];
    if (snprintf(dot,sizeof(dot),"%s.dot",base)>=(int)sizeof(dot) ||
        snprintf(png,sizeof(png),"%s.png",base)>=(int)sizeof(png)) return -1;
    FILE *f=fopen(dot,"w");
    if (!f) { perror(dot); return -1; }
    fputs("digraph AST {\n  graph [rankdir=TB];\n  node [shape=box, style=filled, fillcolor=white, fontname=\"Arial\"];\n",f);
    int contador=0;
    escribir_rec(f,n,&contador);
    fputs("}\n",f);
    if (fclose(f)!=0) return -1;
    /* Nombres de salida internos, sin argumentos de usuario sin validar. */
    if (snprintf(cmd,sizeof(cmd),"dot -Tpng \"%s\" -o \"%s\"",dot,png)>=(int)sizeof(cmd)) return -1;
    int estado=system(cmd);
    if (estado!=0) {
        fprintf(stderr,"No se pudo ejecutar Graphviz. Prueba: dot -Tpng %s -o %s\n",dot,png);
        return -1;
    }
    printf("Generados: %s y %s\n",dot,png);
    return 0;
}
void imprimir_nodo(const Nodo *n, int nivel) {
    if (!n) return;
    char buf[256]; etiqueta(n,buf,sizeof(buf));
    printf("%*s%s\n",nivel*2,"",buf);
    switch(n->tipo) {
        case NODO_SEQ: case NODO_OP:
            imprimir_nodo(n->opBinaria.izq,nivel+1);
            imprimir_nodo(n->opBinaria.der,nivel+1); break;
        case NODO_DECL: case NODO_ASSIGN: imprimir_nodo(n->assign.expr,nivel+1); break;
        case NODO_RETURN: imprimir_nodo(n->ret_expr,nivel+1); break;
        default: break;
    }
}
/* Tabla de simbolos minima para interpretar declaraciones y asignaciones. */
typedef struct Simbolo { char *id; int valor; int inicializado; struct Simbolo *sig; } Simbolo;
static Simbolo *tabla=NULL;
static Simbolo *buscar(const char *id) {
    for (Simbolo *s=tabla;s;s=s->sig) if (strcmp(s->id,id)==0) return s;
    return NULL;
}
static void error_semantico(const char *msg,const char *id) {
    fprintf(stderr,"Error semantico: %s: %s\n",msg,id); exit(EXIT_FAILURE);
}
static int evaluar(const Nodo *n, int *retorno) {
    if (!n || *retorno) return 0;
    switch(n->tipo) {
        case NODO_INT: return n->val_int;
        case NODO_BOOL: return n->val_bool;
        case NODO_ID: {
            Simbolo *s=buscar(n->nombre);
            if (!s || !s->inicializado) error_semantico("variable no declarada o no inicializada",n->nombre);
            return s->valor;
        }
        case NODO_OP: {
            int a=evaluar(n->opBinaria.izq,retorno);
            if (n->opBinaria.op==TOP_AND && !a) return 0;
            if (n->opBinaria.op==TOP_OR && a) return 1;
            int b=evaluar(n->opBinaria.der,retorno);
            switch(n->opBinaria.op) {
                case TOP_SUMA: return a+b; case TOP_RESTA: return a-b;
                case TOP_MULT: return a*b;
                case TOP_DIV: if (!b) error_semantico("division por cero","/"); return a/b;
                case TOP_IGUAL: return a==b; case TOP_MAYOR: return a>b;
                case TOP_MENOR: return a<b; case TOP_AND: return a&&b;
                case TOP_OR: return a||b;
            }
            return 0;
        }
        case NODO_DECL: {
            if (buscar(n->assign.id)) error_semantico("variable ya declarada",n->assign.id);
            Simbolo *s=reservar(sizeof(*s)); s->id=copiar(n->assign.id);
            s->inicializado=n->assign.expr!=NULL;
            if (s->inicializado) s->valor=evaluar(n->assign.expr,retorno);
            s->sig=tabla; tabla=s; return 0;
        }
        case NODO_ASSIGN: {
            Simbolo *s=buscar(n->assign.id);
            if (!s) error_semantico("variable no declarada",n->assign.id);
            s->valor=evaluar(n->assign.expr,retorno); s->inicializado=1;
            return s->valor;
        }
        case NODO_RETURN: {
            int v=n->ret_expr?evaluar(n->ret_expr,retorno):0;
            *retorno=1; return v;
        }
        case NODO_SEQ: {
            int v=evaluar(n->opBinaria.izq,retorno);
            if (*retorno) return v;
            return n->opBinaria.der?evaluar(n->opBinaria.der,retorno):v;
        }
    }
    return 0;
}
int interpretar_programa(const Nodo *programa) {
    int retorno=0;
    int resultado=evaluar(programa,&retorno);
    while(tabla) { Simbolo *s=tabla; tabla=s->sig; free(s->id); free(s); }
    return resultado;
}
