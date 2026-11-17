"""Tipos y representación de tokens del lenguaje Lumo."""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Categorías de elementos reconocidos por el lexer."""

    INTEGER = auto()
    DECIMAL = auto()
    STRING = auto()
    IDENTIFIER = auto()

    TYPE = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FUNCTION = auto()
    RETURN = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    """Token reconocido, incluyendo su ubicación en el código fuente."""

    type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.type.name}({self.lexeme!r}) [{self.line}:{self.column}]"


class LexerError(Exception):
    """Error producido por un carácter o literal inválido."""

    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Línea {line}, columna {column}: {message}")
        self.message = message
        self.line = line
        self.column = column
