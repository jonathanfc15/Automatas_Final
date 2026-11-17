"""Analizador léxico del lenguaje Lumo."""

from compiler.tokens import LexerError, Token, TokenType


class Lexer:
    """Convierte el código fuente de Lumo en una secuencia de tokens."""

    KEYWORDS = {
        "ent": TokenType.TYPE,
        "dec": TokenType.TYPE,
        "txt": TokenType.TYPE,
        "bool": TokenType.TYPE,
        "simon": TokenType.IF,
        "nosimon": TokenType.ELSE,
        "mientras": TokenType.WHILE,
        "funchion": TokenType.FUNCTION,
        "retorno": TokenType.RETURN,
        "muestrame": TokenType.PRINT,
        "verdad": TokenType.TRUE,
        "falso": TokenType.FALSE,
        "Y": TokenType.AND,
        "O": TokenType.OR,
        "NONES": TokenType.NOT,
    }

    SINGLE_CHARACTERS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,
        "=": TokenType.EQUAL,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
    }

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        """Tokeniza todo el código y agrega un token EOF al final."""
        tokens: list[Token] = []
        while not self._at_end():
            character = self._advance()

            if character in " \t\r":
                continue
            if character == "\n":
                self.line += 1
                self.column = 1
                continue
            if character == "/" and self._match("/"):
                self._skip_comment()
                continue
            if character.isalpha() or character == "_":
                tokens.append(self._identifier(character))
                continue
            if character.isdigit():
                tokens.append(self._number(character))
                continue
            if character == '"':
                tokens.append(self._string())
                continue
            if character in self.SINGLE_CHARACTERS:
                tokens.append(
                    Token(
                        self.SINGLE_CHARACTERS[character],
                        character,
                        self.line,
                        self.column - 1,
                    )
                )
                continue
            if character in "<>!=":
                tokens.append(self._comparison(character))
                continue

            raise LexerError(f"carácter no reconocido: {character!r}", self.line, self.column - 1)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _at_end(self) -> bool:
        return self.position >= len(self.source)

    def _advance(self) -> str:
        character = self.source[self.position]
        self.position += 1
        self.column += 1
        return character

    def _match(self, expected: str) -> bool:
        if self._at_end() or self.source[self.position] != expected:
            return False
        self.position += 1
        self.column += 1
        return True

    def _skip_comment(self) -> None:
        while not self._at_end() and self.source[self.position] != "\n":
            self._advance()

    def _identifier(self, first_character: str) -> Token:
        start_column = self.column - 1
        lexeme = first_character
        while not self._at_end() and (
            self.source[self.position].isalnum() or self.source[self.position] == "_"
        ):
            lexeme += self._advance()
        token_type = self.KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        return Token(token_type, lexeme, self.line, start_column)

    def _number(self, first_character: str) -> Token:
        start_column = self.column - 1
        lexeme = first_character
        while not self._at_end() and self.source[self.position].isdigit():
            lexeme += self._advance()

        token_type = TokenType.INTEGER
        if not self._at_end() and self.source[self.position] == ".":
            token_type = TokenType.DECIMAL
            lexeme += self._advance()
            if self._at_end() or not self.source[self.position].isdigit():
                raise LexerError("un número decimal debe tener dígitos después del punto", self.line, self.column - 1)
            while not self._at_end() and self.source[self.position].isdigit():
                lexeme += self._advance()
        return Token(token_type, lexeme, self.line, start_column)

    def _string(self) -> Token:
        start_column = self.column - 1
        value = []
        while not self._at_end() and self.source[self.position] != '"':
            if self.source[self.position] == "\n":
                raise LexerError("la cadena no puede ocupar varias líneas", self.line, self.column)
            value.append(self._advance())
        if self._at_end():
            raise LexerError("cadena sin comilla de cierre", self.line, start_column)
        self._advance()
        return Token(TokenType.STRING, "".join(value), self.line, start_column)

    def _comparison(self, first_character: str) -> Token:
        start_column = self.column - 1
        lexeme = first_character
        if self._match("="):
            lexeme += "="
        token_types = {
            "=": TokenType.EQUAL,
            "==": TokenType.EQUAL_EQUAL,
            "!": TokenType.NOT,
            "!=": TokenType.NOT_EQUAL,
            "<": TokenType.LESS,
            "<=": TokenType.LESS_EQUAL,
            ">": TokenType.GREATER,
            ">=": TokenType.GREATER_EQUAL,
        }
        if lexeme == "!":
            raise LexerError("se esperaba '=' después de '!'", self.line, start_column)
        return Token(token_types[lexeme], lexeme, self.line, start_column)
