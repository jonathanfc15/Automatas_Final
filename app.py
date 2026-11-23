import sys
from dataclasses import fields, is_dataclass

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QTreeWidgetItem,
)

from principal import Ui_EditorLumo
import recursos_rc
from compiler.lexer import Lexer
from compiler.tokens import LexerError
from compiler.parser import Parser, ParserError
from compiler.semantic import SemanticAnalyzer, SemanticError
from compiler.interpreter import Interpreter, RuntimeErrorLumo


class Window(QMainWindow, Ui_EditorLumo):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("Lumo - Editor y compilador")
        self.archivo_actual = None

        self.actionNuevo.triggered.connect(self.nuevo_archivo)
        self.actionAbrir.triggered.connect(self.abrir_archivo)
        self.actionGuardar.triggered.connect(self.guardar_archivo)
        self.actionCopiar.triggered.connect(self.plainTextEdit.copy)
        self.actionPegar.triggered.connect(self.plainTextEdit.paste)
        self.actionCortar.triggered.connect(self.plainTextEdit.cut)
        self.actionAcercaDe.triggered.connect(self.acerca_de)
        self.botonCompilar.clicked.connect(self.compilar_ejecutar)
        self.plainTextEdit.cursorPositionChanged.connect(self.actualizar_posicion_cursor)
        self.actualizar_posicion_cursor()

    def actualizar_posicion_cursor(self):
        cursor = self.plainTextEdit.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.barraEstado.showMessage(
            f"Lumo  |  Línea {linea}  Columna {columna}"
        )

    def mostrar_ast(self, valor):
        self.arbolAST.clear()
        root = QTreeWidgetItem([valor.__class__.__name__])
        self.arbolAST.addTopLevelItem(root)
        self.agregar_nodo_ast(root, valor)

    def agregar_nodo_ast(self, parent, valor):
        if is_dataclass(valor):
            for campo in fields(valor):
                clave = campo.name
                contenido = getattr(valor, clave)
                if isinstance(contenido, list):
                    lista = QTreeWidgetItem([f"{clave} ({len(contenido)})"])
                    parent.addChild(lista)
                    for elemento in contenido:
                        if is_dataclass(elemento):
                            nodo = QTreeWidgetItem([elemento.__class__.__name__])
                            lista.addChild(nodo)
                            self.agregar_nodo_ast(nodo, elemento)
                        else:
                            lista.addChild(QTreeWidgetItem([repr(elemento)]))
                elif is_dataclass(contenido):
                    nodo = QTreeWidgetItem([f"{clave}: {contenido.__class__.__name__}"])
                    parent.addChild(nodo)
                    self.agregar_nodo_ast(nodo, contenido)
                else:
                    parent.addChild(QTreeWidgetItem([f"{clave}: {contenido!r}"]))

    def compilar_ejecutar(self):
        source = self.plainTextEdit.toPlainText()
        self.tablaTokens.setRowCount(0)
        self.arbolAST.clear()
        self.tablaErrores.setRowCount(0)
        self.textoSalida.clear()

        try:
            tokens = Lexer(source).tokenize()
            self.tablaTokens.setRowCount(len(tokens))
            for fila, token in enumerate(tokens):
                self.tablaTokens.setItem(
                    fila, 0, QTableWidgetItem(str(token.line))
                )
                self.tablaTokens.setItem(
                    fila, 1, QTableWidgetItem(token.type.name)
                )
                self.tablaTokens.setItem(
                    fila, 2, QTableWidgetItem(token.lexeme)
                )

            program = Parser(tokens).parse()
            SemanticAnalyzer().analyze(program)

            self.mostrar_ast(program)
            output = Interpreter().execute(program)
            self.textoSalida.setPlainText(output)
            self.panelesResultados.setCurrentWidget(self.pestañasSalida)
            self.barraEstado.showMessage("Compilación y ejecución completadas")
        except (LexerError, ParserError, SemanticError, RuntimeErrorLumo) as error:
            # El lexer y el parser (PLY) reportan todos sus errores en
            # `error.errors`; los demás errores traen uno solo.
            errores = getattr(error, "errors", [error])
            self.tablaErrores.setRowCount(len(errores))
            for fila, err in enumerate(errores):
                self.tablaErrores.setItem(
                    fila, 0, QTableWidgetItem(str(getattr(err, "line", 1)))
                )
                self.tablaErrores.setItem(
                    fila, 1, QTableWidgetItem(str(getattr(err, "column", 1)))
                )
                self.tablaErrores.setItem(
                    fila, 2, QTableWidgetItem(getattr(err, "message", str(err)))
                )
            self.panelesResultados.setCurrentWidget(self.pestañasErrores)
            self.barraEstado.showMessage(
                f"El programa contiene {len(errores)} error(es)"
            )

    def nuevo_archivo(self):
        self.plainTextEdit.clear()
        self.archivo_actual = None
        self.barraEstado.showMessage("Archivo nuevo")

    def abrir_archivo(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            "",
            "Archivos Lumo (*.lumo *.ism);;Todos los archivos (*.*)"
        )

        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            self.plainTextEdit.setPlainText(contenido)
            self.archivo_actual = archivo
            self.barraEstado.showMessage(f"Archivo abierto: {archivo}")

    def guardar_archivo(self):

        archivo = self.archivo_actual
        if not archivo:
            archivo, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo",
                "",
                "Archivos Lumo (*.lumo);;Archivos de texto (*.ism)"
            )

        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(self.plainTextEdit.toPlainText())

            self.archivo_actual = archivo
            self.barraEstado.showMessage(f"Archivo guardado: {archivo}")

    def acerca_de(self):
        QMessageBox.about(self, "Acerca de", "Editor Lumo")


def main():
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
