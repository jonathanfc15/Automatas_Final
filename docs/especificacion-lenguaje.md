# Especificación del lenguaje Lumo

Lumo es un lenguaje de programación imperativo y sencillo, con variables tipadas, condicionales, ciclos y funciones. Se escribe en el editor del proyecto, y el compilador lo analiza con **PLY** (Python Lex-Yacc) para decir si el programa es válido o dónde tiene errores.

| Etapa | Archivo | Qué define |
|---|---|---|
| Análisis léxico | `compiler/lexer.py` | Tokens, palabras reservadas y expresiones regulares |
| Análisis sintáctico | `compiler/parser.py` | Gramática (producciones), precedencia y mensajes de error |
| Árbol sintáctico | `compiler/ast.py` | Nodos que construye el parser |

Este documento describe el **léxico y la sintaxis** de Lumo. Todo lo que aparece aquí sale de los dos archivos de PLY anteriores.

---

## 1. Estructura de un programa

Un programa es una lista (posiblemente vacía) de declaraciones e instrucciones, que se ejecutan en el orden en que aparecen. Las instrucciones terminan en `;`; los bloques se delimitan con `{ }`.

```lumo
// Programa mínimo
ent edad = 20;
muestrame(edad);
```

---

## 2. Elementos léxicos

### 2.1 Espacios y comentarios

- Los espacios, tabuladores y saltos de línea separan tokens y se ignoran.
- Un comentario empieza con `//` y llega hasta el final de la línea. No existen comentarios de varias líneas.

### 2.2 Identificadores

Nombres de variables y funciones. Empiezan con una letra o guion bajo y siguen con letras, dígitos o guion bajo (se aceptan letras con acento y la `ñ`). Distinguen mayúsculas de minúsculas.

Válidos: `edad`, `_total`, `precio2`, `año`. Inválido: `2x` (empieza con dígito: se lee como el número `2` seguido del identificador `x`).

### 2.3 Literales

| Literal | Ejemplos | Notas |
|---|---|---|
| Entero | `0`, `42` | Solo dígitos |
| Decimal | `3.14`, `0.5` | Debe haber dígitos antes **y** después del punto (`3.` es un error) |
| Cadena | `"hola mundo"` | Entre comillas dobles, en una sola línea, sin secuencias de escape |
| Booleano | `verdad`, `vdd`, `falso` | `vdd` es un alias de `verdad` |

### 2.4 Palabras reservadas

No pueden usarse como identificadores.

| Palabra | Token | Significado |
|---|---|---|
| `ent`, `dec`, `txt`, `bool` | `TYPE` | Tipos: entero, decimal, texto y booleano |
| `simon` | `IF` | Condicional |
| `nosimon` | `ELSE` | Rama alternativa del condicional |
| `mientras` | `WHILE` | Ciclo |
| `funchion` | `FUNCTION` | Declaración de función |
| `retorno`, `returno` | `RETURN` | Regresar de una función (`returno` es un alias) |
| `muestrame` | `PRINT` | Imprimir un valor |
| `verdad`, `vdd` | `TRUE` | Valor booleano verdadero |
| `falso` | `FALSE` | Valor booleano falso |
| `Y` | `AND` | Conjunción lógica |
| `O` | `OR` | Disyunción lógica |
| `NONES` | `NOT` | Negación lógica |

`Y`, `O` y `NONES` se escriben en mayúsculas: `y` u `o` en minúscula son identificadores comunes.

### 2.5 Operadores y signos

| Token | Símbolo | Expresión regular | Uso |
|---|---|---|---|
| `PLUS` | `+` | `\+` | Suma |
| `MINUS` | `-` | `-` | Resta y negativo |
| `STAR` | `*` | `\*` | Multiplicación |
| `SLASH` | `/` | `/` | División |
| `PERCENT` | `%` | `%` | Residuo |
| `EQUAL` | `=` | `=` | Asignación |
| `EQUAL_EQUAL` | `==` | `==` | Igual que |
| `NOT_EQUAL` | `!=` | `!=` | Distinto de |
| `LESS` | `<` | `<` | Menor que |
| `LESS_EQUAL` | `<=` | `<=` | Menor o igual |
| `GREATER` | `>` | `>` | Mayor que |
| `GREATER_EQUAL` | `>=` | `>=` | Mayor o igual |
| `LEFT_PAREN` / `RIGHT_PAREN` | `(` `)` | `\(` `\)` | Agrupar, llamadas y condiciones |
| `LEFT_BRACE` / `RIGHT_BRACE` | `{` `}` | `\{` `\}` | Bloques |
| `COMMA` | `,` | `,` | Separar parámetros y argumentos |
| `SEMICOLON` | `;` | `;` | Terminar instrucciones |

Un `!` suelto no es válido: la negación se escribe con `NONES`.

### 2.6 Expresiones regulares de los demás tokens

| Token | Expresión regular (`compiler/lexer.py`) |
|---|---|
| `INTEGER` | `\d+` |
| `DECIMAL` | `\d+\.\d+` |
| `STRING` | `"[^"\n]*"` |
| `IDENTIFIER` | `[^\W\d]\w*` (luego se reclasifica si es palabra reservada) |
| Comentario | `//.*` (se descarta) |

PLY prueba las reglas en este orden: comentario, `DECIMAL`, `INTEGER`, `STRING`, `IDENTIFIER`, y después los operadores de mayor a menor longitud (por eso `==` se reconoce como un solo token y no como dos `=`).

---

## 3. Gramática

Notación: los **no terminales** van en minúsculas, los **tokens** en MAYÚSCULAS, `|` separa alternativas y `ε` es la producción vacía. Son las mismas producciones `p_...` de `compiler/parser.py`; el símbolo inicial es `program`.

```text
program            : declaration_list

declaration_list   : declaration_list declaration
                   | ε

declaration        : var_declaration
                   | function_declaration
                   | statement
                   | error SEMICOLON              (recuperación de errores)

var_declaration    : TYPE IDENTIFIER EQUAL expression SEMICOLON

function_declaration : FUNCTION TYPE IDENTIFIER LEFT_PAREN parameters RIGHT_PAREN block

parameters         : ε
                   | parameter_list
parameter_list     : parameter_list COMMA parameter
                   | parameter
parameter          : TYPE IDENTIFIER

statement          : print_statement
                   | if_statement
                   | while_statement
                   | return_statement
                   | assignment
                   | expression_statement

print_statement    : PRINT LEFT_PAREN expression RIGHT_PAREN SEMICOLON
if_statement       : IF expression block
                   | IF expression block ELSE block
while_statement    : WHILE expression block
return_statement   : RETURN SEMICOLON
                   | RETURN expression SEMICOLON
assignment         : IDENTIFIER EQUAL expression SEMICOLON
expression_statement : expression SEMICOLON

block              : LEFT_BRACE declaration_list RIGHT_BRACE

expression         : expression PLUS expression
                   | expression MINUS expression
                   | expression STAR expression
                   | expression SLASH expression
                   | expression PERCENT expression
                   | expression LESS expression
                   | expression LESS_EQUAL expression
                   | expression GREATER expression
                   | expression GREATER_EQUAL expression
                   | expression EQUAL_EQUAL expression
                   | expression NOT_EQUAL expression
                   | expression AND expression
                   | expression OR expression
                   | MINUS expression              %prec UNARY
                   | NOT expression                %prec UNARY
                   | LEFT_PAREN expression RIGHT_PAREN
                   | INTEGER | DECIMAL | STRING | TRUE | FALSE
                   | IDENTIFIER
                   | IDENTIFIER LEFT_PAREN arguments RIGHT_PAREN

arguments          : ε
                   | argument_list
argument_list      : argument_list COMMA expression
                   | expression
```

### 3.1 Precedencia y asociatividad

De **mayor** a **menor** prioridad. Todos los operadores binarios asocian de izquierda a derecha.

| Nivel | Operadores | Asociatividad |
|---|---|---|
| 1 (más alto) | `-` (negativo), `NONES` | derecha (prefijos) |
| 2 | `*`  `/`  `%` | izquierda |
| 3 | `+`  `-` | izquierda |
| 4 | `<`  `<=`  `>`  `>=` | izquierda |
| 5 | `==`  `!=` | izquierda |
| 6 | `Y` | izquierda |
| 7 (más bajo) | `O` | izquierda |

Por ejemplo, `10 - 4 - 3 * 2` se agrupa como `(10 - 4) - (3 * 2)`.

### 3.2 Reglas que conviene recordar

- **Declarar una variable exige valor inicial:** `ent x = 0;`. No existe `ent x;`.
- **La condición de `simon` y `mientras` no necesita paréntesis** (`simon x > 3 { ... }`), aunque puede llevarlos porque son una expresión agrupada.
- **Las ramas siempre son bloques con llaves.** `nosimon` solo admite un bloque `{ ... }`; no hay `nosimon simon` encadenado, hay que anidar un `simon` dentro de un bloque.
- **`=` es una instrucción, no una expresión:** `x = 5;` es válido, pero `x + 1 = 5;` y `ent a = (b = 3);` no.
- **Una expresión sola puede ser una instrucción** si termina en `;`, lo que permite llamar funciones como `suma(1, 2);`.
- **Las funciones pueden declararse dentro de cualquier bloque**, y las llamadas aceptan cualquier expresión como argumento.
- **`retorno;`** sin valor y **`retorno expresión;`** son ambos válidos.

---

## 4. Ejemplos válidos

### 4.1 Variables, operaciones e impresión

```lumo
ent base = 6;
ent altura = 4;
dec area = 0.5 * base * altura;
txt etiqueta = "Area del triangulo:";
muestrame(etiqueta);
muestrame(area);
```

### 4.2 Condicionales

```lumo
ent edad = 20;
simon edad >= 18 {
    muestrame("Mayor de edad");
} nosimon {
    muestrame("Menor de edad");
}
```

### 4.3 Ciclo

```lumo
ent i = 1;
mientras i <= 5 {
    muestrame(i * i);
    i = i + 1;
}
```

### 4.4 Funciones

```lumo
funchion ent mayor(ent a, ent b) {
    simon a > b {
        retorno a;
    } nosimon {
        retorno b;
    }
}

ent resultado = mayor(4, 9);
muestrame(resultado);
```

### 4.5 Operadores lógicos y comparaciones

```lumo
ent x = 7;
bool esValido = x > 0 Y x < 10 Y NONES (x == 5);
simon esValido O falso {
    muestrame("x esta en el rango");
}
```

---

## 5. Ejemplos con errores

El compilador reporta línea y columna, y puede mostrar varios errores a la vez. Los mensajes son los que genera el analizador.

### 5.1 Errores léxicos

| Código | Mensaje |
|---|---|
| `ent x = 5 @ 2;` | Línea 1, columna 11: carácter no reconocido: '@' |
| `dec d = 3.;` | Línea 1, columna 9: un número decimal debe tener dígitos después del punto |
| `txt t = "abc;` | Línea 1, columna 9: cadena sin comilla de cierre (no puede ocupar varias líneas) |
| `bool b = !verdad;` | Línea 1, columna 10: se esperaba '=' después de '!' (para negar usa NONES) |

### 5.2 Errores sintácticos

| Código | Mensaje |
|---|---|
| `ent edad = 20` + salto de línea + `muestrame(edad);` | Línea 1, columna 14: se esperaba ';' al final de la instrucción (se encontró 'muestrame') |
| `ent x = ;` | Línea 1, columna 9: se esperaba una expresión, pero se encontró ';' |
| `ent 2x = 1;` | Línea 1, columna 5: se esperaba un identificador, pero se encontró '2' |
| `muestrame("hola";` | Línea 1, columna 17: se esperaba ')', pero se encontró ';' |
| `simon x > 3 muestrame(1);` | Línea 1, columna 13: se esperaba '{' para abrir el bloque, pero se encontró 'muestrame' |
| `mientras x < 3 { x = x + 1;` | Línea 1, columna 28: se esperaba '}' para cerrar el bloque, pero el programa terminó |
| `nosimon { }` | Línea 1, columna 1: 'nosimon' sin un 'simon' antes |
| `funchion ent f(ent a { retorno a; }` | Línea 1, columna 22: se esperaba ')', pero se encontró '{' |
| `x + 1 = 5;` | Línea 1, columna 6: se esperaba ';' al final de la instrucción (se encontró '=') |

### 5.3 Varios errores en un mismo programa

```lumo
ent a = 1 + ;
ent b = 2 3;
ent c = (4;
```

```text
Línea 1, columna 13: se esperaba una expresión, pero se encontró ';'
Línea 2, columna 10: se esperaba ';' al final de la instrucción (se encontró '3')
Línea 3, columna 11: se esperaba ')', pero se encontró ';'
```

---

## 6. Cómo se manejan los errores

- **Léxicos:** `t_error` y las reglas de error de `lexer.py` anotan el problema, saltan el carácter inválido y siguen leyendo, por lo que se reportan todos los errores léxicos del programa.
- **Sintácticos:** cuando el parser no puede continuar, calcula qué tokens habría aceptado en ese punto y arma el mensaje con esa información. Después se recupera descartando tokens hasta el siguiente `;` (producción `declaration : error SEMICOLON`) y sigue analizando, así que puede reportar más de un error.
- Si un programa tiene errores léxicos, el análisis sintáctico no se ejecuta hasta corregirlos.
- Tras un error, PLY ignora los siguientes tres tokens para no repetir errores en cascada; por eso un segundo error muy cercano al primero puede aparecer hasta corregir el primero.