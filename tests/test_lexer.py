import unittest

from compiler.lexer import Lexer
from compiler.tokens import LexerError, TokenType


class LexerTests(unittest.TestCase):
    def test_reconoce_programa_basico(self):
        tokens = Lexer('ent edad = 20; muestrame("hola");').tokenize()
        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.TYPE,
                TokenType.IDENTIFIER,
                TokenType.EQUAL,
                TokenType.INTEGER,
                TokenType.SEMICOLON,
                TokenType.PRINT,
                TokenType.LEFT_PAREN,
                TokenType.STRING,
                TokenType.RIGHT_PAREN,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )

    def test_ignora_comentarios_y_actualiza_linea(self):
        tokens = Lexer("// comentario\nsimon verdad {").tokenize()
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[0].line, 2)

    def test_rechaza_caracter_invalido(self):
        with self.assertRaises(LexerError):
            Lexer("entero edad = @;").tokenize()


if __name__ == "__main__":
    unittest.main()
