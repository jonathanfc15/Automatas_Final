"""Pruebas automatizadas para el analizador léxico y sintáctico de Lumo."""

import os
import sys


RUTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_RAIZ not in sys.path:
    sys.path.insert(0, RUTA_RAIZ)

from compiler.lexer import Lexer
from compiler.parser import Parser, ParserError
from compiler.tokens import LexerError


def analizar_codigo(codigo: str, nombre_prueba: str = "Fragmento") -> bool:
    """Ejecuta el análisis léxico y sintáctico sobre una cadena de código Lumo."""
    print(f"\n=== Analizando: {nombre_prueba} ===")
    try:
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()
        print(f"  [OK] Análisis léxico exitoso ({len(tokens)} tokens detectados).")

        parser = Parser(tokens)
        programa_ast = parser.parse()
        print(f"  [OK] Análisis sintáctico exitoso ({len(programa_ast.declarations)} declaraciones raíz).")
        return True

    except LexerError as error_lexico:
        print(f"  [ERROR LÉXICO] {error_lexico}")
        return False
    except ParserError as error_sintactico:
        print(f"  [ERROR SINTÁCTICO] {error_sintactico}")
        return False


def ejecutar_bateria_pruebas() -> None:
    """Evalúa todos los archivos .lumo dentro de la carpeta examples/."""
    carpeta_ejemplos = os.path.join(RUTA_RAIZ, "examples")
    archivos = sorted(f for f in os.listdir(carpeta_ejemplos) if f.endswith(".lumo"))

    if not archivos:
        print("No se encontraron archivos .lumo en la carpeta examples/.")
        return

    exitosos = 0
    con_errores = 0

    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_ejemplos, archivo)
        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido = f.read()

        if analizar_codigo(contenido, archivo):
            exitosos += 1
        else:
            con_errores += 1

    print("\n" + "=" * 45)
    print(f"Resumen de pruebas: {exitosos} válidos | {con_errores} con errores detectados")
    print("=" * 45)


if __name__ == "__main__":
    ejecutar_bateria_pruebas()