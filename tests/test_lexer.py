import unittest

from compiler import lexer as lexer_module
from compiler.lexer import Lexer
from compiler.tokens import LexerError, TokenType


def kinds(source):
    return [token.type for token in Lexer(source).tokenize()]


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

    def test_igualdad_es_un_solo_token(self):
        self.assertEqual(
            kinds("a == b != c <= d >= e"),
            [
                TokenType.IDENTIFIER, TokenType.EQUAL_EQUAL,
                TokenType.IDENTIFIER, TokenType.NOT_EQUAL,
                TokenType.IDENTIFIER, TokenType.LESS_EQUAL,
                TokenType.IDENTIFIER, TokenType.GREATER_EQUAL,
                TokenType.IDENTIFIER, TokenType.EOF,
            ],
        )

    def test_palabras_reservadas_y_alias(self):
        self.assertEqual(kinds("retorno returno")[:2], [TokenType.RETURN, TokenType.RETURN])
        self.assertEqual(kinds("verdad vdd falso")[:3], [TokenType.TRUE, TokenType.TRUE, TokenType.FALSE])
        self.assertEqual(kinds("Y O NONES")[:3], [TokenType.AND, TokenType.OR, TokenType.NOT])
        # Distingue mayúsculas: 'y' es un identificador, 'Y' es el operador.
        self.assertEqual(kinds("y")[0], TokenType.IDENTIFIER)

    def test_numeros_y_cadenas(self):
        tokens = Lexer('12 3.5 "hola mundo"').tokenize()
        self.assertEqual([t.type for t in tokens[:3]], [TokenType.INTEGER, TokenType.DECIMAL, TokenType.STRING])
        self.assertEqual(tokens[2].lexeme, "hola mundo")

    def test_columnas(self):
        tokens = Lexer("ent x = 1;\n  ent y = 2;").tokenize()
        self.assertEqual((tokens[0].line, tokens[0].column), (1, 1))
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 5))
        self.assertEqual((tokens[5].line, tokens[5].column), (2, 3))

    def test_reporta_todos_los_errores_lexicos(self):
        tokens, errors = Lexer('ent x = 3. @ "abc\n!').scan()
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        self.assertEqual(
            [(e.line, e.column) for e in errors],
            [(1, 9), (1, 12), (1, 14), (2, 1)],
        )
        with self.assertRaises(LexerError) as raised:
            Lexer('ent x = 3. @').tokenize()
        self.assertEqual(len(raised.exception.errors), 2)

    def test_tokens_de_ply_coinciden_con_token_type(self):
        ply_tokens = set(lexer_module.tokens)
        enum_tokens = {t.name for t in TokenType} - {"EOF"}
        self.assertEqual(ply_tokens, enum_tokens)
        self.assertTrue(set(lexer_module.reserved.values()) <= ply_tokens)


if __name__ == "__main__":
    unittest.main()
