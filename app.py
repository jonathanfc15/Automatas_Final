import sys
from dataclasses import fields, is_dataclass

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidgetItem,
    QTreeWidgetItem,
    QWidget,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QKeySequence, QPixmap
from PySide6.QtCore import Qt

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
        self._crear_busqueda_central()
        self.fondo = QLabel(self)
        self.fondo.setScaledContents(False)
        self.fondo.setPixmap(
            QPixmap(":/fondo/cuadricula.png")
        )
        self.fondo.lower()
        self.actualizar_fondo()

        self.actionNuevo.triggered.connect(self.nuevo_archivo)
        self.actionAbrir.triggered.connect(self.abrir_archivo)
        self.actionGuardar.triggered.connect(self.guardar_archivo)
        self.actionCopiar.triggered.connect(self.plainTextEdit.copy)
        self.actionPegar.triggered.connect(self.plainTextEdit.paste)
        self.actionCortar.triggered.connect(self.plainTextEdit.cut)
        self.actionAcercaDe.triggered.connect(self.acerca_de)
        self.botonCompilar.clicked.connect(self.compilar_ejecutar)
        self.plainTextEdit.cursorPositionChanged.connect(self.actualizar_posicion_cursor)
        self.acceso_busqueda = self.addAction("")
        self.acceso_busqueda.setShortcut(QKeySequence("Ctrl+F"))
        self.acceso_busqueda.triggered.connect(self.buscarTexto.setFocus)
        self.actualizar_posicion_cursor()

    def _crear_busqueda_central(self):
        espaciador_izquierdo = QWidget(self.barraHerramientas)
        espaciador_izquierdo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        contenedor = QWidget(self.barraHerramientas)
        contenedor.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(6)

        self.buscarTexto = QLineEdit(contenedor)
        self.buscarTexto.setPlaceholderText("Buscar...")
        self.buscarTexto.setFixedWidth(220)
        self.buscarTexto.setClearButtonEnabled(True)
        self.buscarTexto.setStyleSheet("""
            QLineEdit {
                background-color: rgba(10, 15, 18, 230);
                color: #d6e4dc;
                border: 1px solid #1f8f4e;
                border-radius: 8px;
                padding: 7px 12px;
                selection-background-color: #1f8f4e;
                selection-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #39A0FF;
            }
        """)
        self.buscarTexto.returnPressed.connect(self.buscar_siguiente)

        self.botonBuscar = QPushButton("Buscar", contenedor)
        self.botonBuscar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.botonBuscar.setFixedHeight(34)
        self.botonBuscar.setStyleSheet("""
            QPushButton {
                background-color: #12301f;
                color: #39A0FF;
                border: 1px solid #39A0FF;
                border-radius: 8px;
                padding: 7px 18px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1a4a2e;
                color: #7dffa8;
                border: 1px solid #7dffa8;
            }
            QPushButton:pressed {
                background-color: #39A0FF;
                color: #05080a;
                border: 1px solid #39A0FF;
            }
        """)
        self.botonBuscar.clicked.connect(self.buscar_siguiente)

        layout.addWidget(self.buscarTexto)
        layout.addWidget(self.botonBuscar)

        espaciador_derecho = QWidget(self.barraHerramientas)
        espaciador_derecho.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.barraHerramientas.addWidget(espaciador_izquierdo)
        self.barraHerramientas.addWidget(contenedor)
        self.barraHerramientas.addWidget(espaciador_derecho)

    def buscar_siguiente(self):
        texto = self.buscarTexto.text()
        if not texto:
            return
        if not self.plainTextEdit.find(texto):
            cursor = self.plainTextEdit.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            self.plainTextEdit.setTextCursor(cursor)
            self.plainTextEdit.find(texto)

    def actualizar_fondo(self):
        pixmap = QPixmap(":/fondo/cuadricula.png")
        if pixmap.isNull():
            return
        escalada = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.fondo.setPixmap(escalada)
        self.fondo.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        self.actualizar_fondo()

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
            self.tablaErrores.setRowCount(1)
            self.tablaErrores.setItem(
                0, 0, QTableWidgetItem(str(getattr(error, "line", 1)))
            )
            self.tablaErrores.setItem(
                0, 1, QTableWidgetItem(str(getattr(error, "column", 1)))
            )
            self.tablaErrores.setItem(
                0, 2, QTableWidgetItem(str(error))
            )
            self.panelesResultados.setCurrentWidget(self.pestañasErrores)
            self.barraEstado.showMessage("El programa contiene errores")

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


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec())
