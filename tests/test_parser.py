import unittest

from compiler.ast import Binary, FunctionDeclaration, IfStatement, VarDeclaration
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserError


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


class ParserTests(unittest.TestCase):
    def test_parsea_variable_y_expresion(self):
        program = parse("ent resultado = 2 + 3 * 4;")
        declaration = program.declarations[0]
        self.assertIsInstance(declaration, VarDeclaration)
        self.assertIsInstance(declaration.initializer, Binary)
        self.assertEqual(declaration.initializer.operator, "+")

    def test_parsea_funcion_y_condicional(self):
        program = parse("funchion ent mayor(ent edad) { simon edad > 17 { retorno edad; } }")
        self.assertIsInstance(program.declarations[0], FunctionDeclaration)
        self.assertIsInstance(program.declarations[0].body.statements[0], IfStatement)

    def test_reporta_error_sintactico(self):
        with self.assertRaises(ParserError) as error:
            parse("ent edad = 20")
        self.assertIn("Línea 1, columna", str(error.exception))


if __name__ == "__main__":
    unittest.main()
