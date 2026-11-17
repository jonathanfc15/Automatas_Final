import unittest

from compiler.ast import Binary, Literal, PrintStatement, Program, VarDeclaration


class AstTests(unittest.TestCase):
    def test_crea_arbol_basico(self):
        tree = Program(
            declarations=[
                VarDeclaration(
                    type_name="entero",
                    name="edad",
                    initializer=Literal(20),
                ),
                PrintStatement(
                    expression=Binary(Literal(2), "+", Literal(3)),
                ),
            ]
        )

        self.assertEqual(tree.declarations[0].name, "edad")
        self.assertEqual(tree.declarations[1].expression.right.value, 3)


if __name__ == "__main__":
    unittest.main()
