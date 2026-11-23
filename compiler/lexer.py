"""Analizador léxico de Lumo, construido con PLY (``ply.lex``).

Aquí se definen los tokens del lenguaje, las palabras reservadas y la
expresión regular de cada token. PLY junta todas las reglas ``t_...`` de este
módulo en una sola expresión regular y reconoce el texto de izquierda a
derecha:

* Las reglas escritas como *función* se prueban en el orden en que aparecen
  en este archivo (por eso ``DECIMAL`` va antes que ``INTEGER``).
* Las reglas escritas como *cadena* (operadores y signos) se prueban después,
  de la expresión más larga a la más corta (por eso ``==`` gana a ``=``).
"""

import sys

import ply.lex as lex

from compiler.tokens import LexerError, Token, TokenType

# --------------------------------------------------------------------------
# Palabras reservadas: se reconocen como identificador y luego se reclasifican
#   'texto en Lumo' : 'NOMBRE_DEL_TOKEN'
# --------------------------------------------------------------------------
reserved = {
    "ent": "TYPE",
    "dec": "TYPE",
    "txt": "TYPE",
    "bool": "TYPE",
    "simon": "IF",
    "nosimon": "ELSE",
    "mientras": "WHILE",
    "funchion": "FUNCTION",
    "retorno": "RETURN",
    "returno": "RETURN",
    "muestrame": "PRINT",
    "verdad": "TRUE",
    "vdd": "TRUE",
    "falso": "FALSE",
    "Y": "AND",
    "O": "OR",
    "NONES": "NOT",
}

# --------------------------------------------------------------------------
# Lista de tokens (la exige PLY)
# --------------------------------------------------------------------------
tokens = (
    # Literales e identificadores
    "INTEGER", "DECIMAL", "STRING", "IDENTIFIER",
    # Palabras reservadas
    "TYPE", "IF", "ELSE", "WHILE", "FUNCTION", "RETURN", "PRINT",
    "TRUE", "FALSE", "AND", "OR", "NOT",
    # Operadores
    "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",
    "EQUAL", "EQUAL_EQUAL", "NOT_EQUAL",
    "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL",
    # Signos
    "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
    "COMMA", "SEMICOLON",
)

# --------------------------------------------------------------------------
# Reglas de cadena: operadores y signos
# --------------------------------------------------------------------------
t_PLUS = r"\+"
t_MINUS = r"-"
t_STAR = r"\*"
t_SLASH = r"/"
t_PERCENT = r"%"
t_EQUAL_EQUAL = r"=="
t_NOT_EQUAL = r"!="
t_LESS_EQUAL = r"<="
t_GREATER_EQUAL = r">="
t_EQUAL = r"="
t_LESS = r"<"
t_GREATER = r">"
t_LEFT_PAREN = r"\("
t_RIGHT_PAREN = r"\)"
t_LEFT_BRACE = r"\{"
t_RIGHT_BRACE = r"\}"
t_COMMA = r","
t_SEMICOLON = r";"

# Caracteres que se ignoran entre tokens
t_ignore = " \t\r"


def find_column(source: str, position: int) -> int:
    """Columna (empezando en 1) de la posición ``position`` dentro de ``source``."""
    last_newline = source.rfind("\n", 0, position)
    return position - last_newline


# --------------------------------------------------------------------------
# Reglas de función (se prueban en este orden)
# --------------------------------------------------------------------------
def t_COMMENT(t):
    r"//.*"
    # No regresa token: el comentario se descarta.


def t_DECIMAL(t):
    r"\d+\.\d+"
    return t


def t_BAD_DECIMAL(t):
    r"\d+\.(?!\d)"
    column = find_column(t.lexer.lexdata, t.lexpos)
    t.lexer.errors.append(
        LexerError("un número decimal debe tener dígitos después del punto", t.lineno, column)
    )


def t_INTEGER(t):
    r"\d+"
    return t


def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # el lexema no incluye las comillas
    return t


def t_UNTERMINATED_STRING(t):
    r'"[^"\n]*'
    column = find_column(t.lexer.lexdata, t.lexpos)
    t.lexer.errors.append(
        LexerError("cadena sin comilla de cierre (no puede ocupar varias líneas)", t.lineno, column)
    )


def t_IDENTIFIER(t):
    r"[^\W\d]\w*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    column = find_column(t.lexer.lexdata, t.lexpos)
    character = t.value[0]
    if character == "!":
        message = "se esperaba '=' después de '!' (para negar usa NONES)"
    else:
        message = f"carácter no reconocido: {character!r}"
    t.lexer.errors.append(LexerError(message, t.lineno, column))
    t.lexer.skip(1)


# --------------------------------------------------------------------------
# Interfaz que usa el resto del proyecto
# --------------------------------------------------------------------------
class Lexer:
    """Envuelve al lexer de PLY y entrega objetos ``Token`` con línea y columna."""

    def __init__(self, source: str):
        self.source = source
        self.errors: list[LexerError] = []

    def scan(self) -> tuple[list[Token], list[LexerError]]:
        """Tokeniza todo el código sin detenerse en el primer error.

        Regresa ``(tokens, errores)``. Los caracteres inválidos se saltan y se
        anotan en ``errores``; la lista de tokens siempre termina con ``EOF``.
        """
        plylexer = lex.lex(module=sys.modules[__name__])
        plylexer.errors = []
        plylexer.input(self.source)

        result = [
            Token(
                TokenType[ply_token.type],
                ply_token.value,
                ply_token.lineno,
                find_column(self.source, ply_token.lexpos),
            )
            for ply_token in plylexer
        ]
        result.append(
            Token(
                TokenType.EOF,
                "",
                plylexer.lineno,
                find_column(self.source, len(self.source)),
            )
        )
        self.errors = plylexer.errors
        return result, self.errors

    def tokenize(self) -> list[Token]:
        """Tokeniza el código; si hay errores léxicos lanza ``LexerError``.

        La excepción es el primer error y su atributo ``errors`` trae todos.
        """
        result, errors = self.scan()
        if errors:
            first = errors[0]
            first.errors = list(errors)
            raise first
        return result
