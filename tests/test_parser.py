import unittest

import ply.yacc as yacc

import compiler.parser as parser_module
from compiler.ast import (
    Assignment, Binary, Call, FunctionDeclaration, IfStatement, Literal,
    PrintStatement, Unary, VarDeclaration, WhileStatement,
)
from compiler.lexer import Lexer
from compiler.parser import Parser, ParserError


def parse(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def errors_of(source: str):
    _, errors = Parser(Lexer(source).tokenize()).parse_all()
    return errors


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

    def test_precedencia_y_asociatividad(self):
        expression = parse("ent r = 10 - 4 - 3 * 2;").declarations[0].initializer
        # (10 - 4) - (3 * 2)
        self.assertEqual(expression.operator, "-")
        self.assertEqual(expression.left.operator, "-")
        self.assertEqual(expression.right.operator, "*")

    def test_logicos_comparacion_y_unarios(self):
        expression = parse("bool b = NONES a < 1 Y -x == 2 O verdad;").declarations[0].initializer
        self.assertEqual(expression.operator, "O")
        self.assertEqual(expression.left.operator, "Y")
        self.assertIsInstance(expression.left.left.left, Unary)  # (NONES a) < 1
        self.assertIsInstance(expression.right, Literal)

    def test_llamadas_asignacion_while_e_impresion(self):
        program = parse(
            'x = suma(1, 2 + 3, otra());'
            'mientras x < 10 { x = x + 1; }'
            'muestrame("fin");'
        )
        assignment, loop, printing = program.declarations
        self.assertIsInstance(assignment, Assignment)
        self.assertIsInstance(assignment.value, Call)
        self.assertEqual(len(assignment.value.arguments), 3)
        self.assertIsInstance(loop, WhileStatement)
        self.assertIsInstance(printing, PrintStatement)

    def test_programa_vacio(self):
        self.assertEqual(parse("").declarations, [])
        self.assertEqual(parse("// nada").declarations, [])

    def test_posiciones_en_el_arbol(self):
        declaration = parse("\n  ent edad = 20;").declarations[0]
        self.assertEqual((declaration.line, declaration.column), (2, 7))

    def test_mensaje_de_punto_y_coma_apunta_al_final_de_la_linea_anterior(self):
        errors = errors_of("ent edad = 20\nmuestrame(edad);")
        self.assertEqual(len(errors), 1)
        self.assertEqual((errors[0].line, errors[0].column), (1, 14))
        self.assertIn("';'", errors[0].message)

    def test_reporta_varios_errores_sintacticos(self):
        errors = errors_of("ent a = 1 + ;\nent b = 2 3;\nent c = (4;\nmuestrame(a);")
        self.assertEqual([e.line for e in errors], [1, 2, 3])
        with self.assertRaises(ParserError) as raised:
            parse("ent a = 1 + ;\nent b = 2 3;")
        self.assertEqual(len(raised.exception.errors), 2)

    def test_mensajes_utiles(self):
        self.assertIn("'}'", errors_of("mientras x < 3 { x = x + 1;")[0].message)
        self.assertIn("'{'", errors_of("simon x > 3 muestrame(1);")[0].message)
        self.assertIn("')'", errors_of('muestrame("hola";')[0].message)
        self.assertIn("expresión", errors_of("ent x = ;")[0].message)

    def test_gramatica_sin_conflictos(self):
        class Capture:
            def __init__(self):
                self.messages = []

            def _add(self, message, *args, **kwargs):
                self.messages.append(message % args if args else message)

            warning = error = info = debug = critical = _add

        capture = Capture()
        yacc.yacc(module=parser_module, write_tables=False, debug=False, errorlog=capture)
        self.assertEqual(capture.messages, [])


if __name__ == "__main__":
    unittest.main()
