# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfazArchivo.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QToolBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_EditorLumo(object):
    def setupUi(self, EditorLumo):
        if not EditorLumo.objectName():
            EditorLumo.setObjectName(u"EditorLumo")
        EditorLumo.resize(1200, 655)
        EditorLumo.setMinimumSize(QSize(800, 450))
        EditorLumo.setStyleSheet(u"QMainWindow {\n"
"    background-color: #05080a;\n"
"}\n"
"QWidget#centralwidget {\n"
"    background-color: #05080a;\n"
"}\n"
"QWidget {\n"
"    color: #c9d1d9;\n"
"    font-family: \"Inter\", \"Segoe UI\", \"Noto Sans\", sans-serif;\n"
"    font-size: 10pt;\n"
"}\n"
"QFrame#marcoPrincipal {\n"
"    background-color: rgba(8, 12, 14, 235);\n"
"    border: 1px solid #1f8f4e;\n"
"    border-radius: 14px;\n"
"}\n"
"QPlainTextEdit#plainTextEdit {\n"
"    background-color: #0a0f12;\n"
"    color: #d6e4dc;\n"
"    border: 1px solid #1c2a26;\n"
"    border-radius: 8px;\n"
"    padding: 8px;\n"
"    selection-background-color: #1f8f4e;\n"
"    selection-color: #ffffff;\n"
"    font-family: \"JetBrains Mono\", \"Fira Code\", \"DejaVu Sans Mono\", \"Consolas\", monospace;\n"
"    font-size: 11pt;\n"
"}\n"
"QPlainTextEdit#plainTextEdit:focus {\n"
"    border: 1px solid #2ee66b;\n"
"}\n"
"QPushButton#botonCompilar {\n"
"    background-color: #12301f;\n"
"    color: #2ee66b;\n"
"    border: 1px solid #2ee66b;\n"
"    borde"
                        "r-radius: 8px;\n"
"    padding: 8px 20px;\n"
"    font-weight: 600;\n"
"    min-height: 22px;\n"
"}\n"
"QPushButton#botonCompilar:hover {\n"
"    background-color: #1a4a2e;\n"
"    color: #7dffa8;\n"
"    border: 1px solid #7dffa8;\n"
"}\n"
"QPushButton#botonCompilar:pressed {\n"
"    background-color: #2ee66b;\n"
"    color: #05080a;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: 1px solid #1c2a26;\n"
"    border-radius: 8px;\n"
"    background-color: #0a0f12;\n"
"    top: -1px;\n"
"}\n"
"QTabBar::tab {\n"
"    background-color: #0d1417;\n"
"    color: #7f9a8d;\n"
"    padding: 6px 18px;\n"
"    border: 1px solid #1c2a26;\n"
"    border-bottom: none;\n"
"    border-top-left-radius: 6px;\n"
"    border-top-right-radius: 6px;\n"
"    margin-right: 2px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background-color: #12301f;\n"
"    color: #2ee66b;\n"
"    border-color: #1f8f4e;\n"
"}\n"
"QTreeWidget, QTableWidget, QPlainTextEdit#textoSalida, QListWidget {\n"
"    background-color: #0a0f12;\n"
"    color: #d6e4dc;\n"
""
                        "    border: none;\n"
"    alternate-background-color: #0d1417;\n"
"    gridline-color: #1c2a26;\n"
"    font-family: \"JetBrains Mono\", \"Fira Code\", \"DejaVu Sans Mono\", \"Consolas\", monospace;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #0d1417;\n"
"    color: #2ee66b;\n"
"    border: none;\n"
"    border-bottom: 1px solid #1f8f4e;\n"
"    padding: 4px 8px;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #05080a;\n"
"    color: #c9d1d9;\n"
"    border-bottom: 1px solid #1c2a26;\n"
"}\n"
"QMenuBar::item {\n"
"    padding: 5px 12px;\n"
"    background: transparent;\n"
"}\n"
"QMenuBar::item:selected {\n"
"    background-color: #12301f;\n"
"    color: #2ee66b;\n"
"    border-radius: 4px;\n"
"}\n"
"QMenu {\n"
"    background-color: #0a0f12;\n"
"    border: 1px solid #1f8f4e;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"QMenu::item {\n"
"    padding: 6px 24px;\n"
"    border-radius: 4px;\n"
"}\n"
"QMenu::item:selected {\n"
"    background-color: #12301f;\n"
"    color: #2ee66b;\n"
""
                        "}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #1c2a26;\n"
"    margin: 4px 8px;\n"
"}\n"
"QToolBar {\n"
"    background-color: #070b0d;\n"
"    border: none;\n"
"    border-bottom: 1px solid #1c2a26;\n"
"    spacing: 6px;\n"
"    padding: 4px;\n"
"}\n"
"QToolButton {\n"
"    background: transparent;\n"
"    color: #c9d1d9;\n"
"    border: 1px solid transparent;\n"
"    border-radius: 6px;\n"
"    padding: 4px 10px;\n"
"}\n"
"QToolButton:hover {\n"
"    background-color: #12301f;\n"
"    border: 1px solid #1f8f4e;\n"
"    color: #2ee66b;\n"
"}\n"
"QStatusBar {\n"
"    background-color: #070b0d;\n"
"    color: #7f9a8d;\n"
"    border-top: 1px solid #1c2a26;\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: #070b0d;\n"
"    width: 10px;\n"
"    margin: 0;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #1f8f4e;\n"
"    border-radius: 5px;\n"
"    min-height: 24px;\n"
"}\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }\n"
"QScrollBar:horizontal {\n"
""
                        "    background: #070b0d;\n"
"    height: 10px;\n"
"    margin: 0;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #1f8f4e;\n"
"    border-radius: 5px;\n"
"    min-width: 24px;\n"
"}\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }\n"
"QSplitter::handle {\n"
"    background-color: #1c2a26;\n"
"}\n"
"QSplitter::handle:hover {\n"
"    background-color: #2ee66b;\n"
"}")
        self.actionNuevo = QAction(EditorLumo)
        self.actionNuevo.setObjectName(u"actionNuevo")
        self.actionAbrir = QAction(EditorLumo)
        self.actionAbrir.setObjectName(u"actionAbrir")
        self.actionGuardar = QAction(EditorLumo)
        self.actionGuardar.setObjectName(u"actionGuardar")
        self.actionCopiar = QAction(EditorLumo)
        self.actionCopiar.setObjectName(u"actionCopiar")
        self.actionPegar = QAction(EditorLumo)
        self.actionPegar.setObjectName(u"actionPegar")
        self.actionCortar = QAction(EditorLumo)
        self.actionCortar.setObjectName(u"actionCortar")
        self.actionAcercaDe = QAction(EditorLumo)
        self.actionAcercaDe.setObjectName(u"actionAcercaDe")
        self.centralwidget = QWidget(EditorLumo)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutCentral = QVBoxLayout(self.centralwidget)
        self.layoutCentral.setSpacing(8)
        self.layoutCentral.setObjectName(u"layoutCentral")
        self.layoutCentral.setContentsMargins(16, 16, 16, 16)
        self.marcoPrincipal = QFrame(self.centralwidget)
        self.marcoPrincipal.setObjectName(u"marcoPrincipal")
        self.marcoPrincipal.setFrameShape(QFrame.StyledPanel)
        self.marcoPrincipal.setFrameShadow(QFrame.Plain)
        self.layoutMarco = QVBoxLayout(self.marcoPrincipal)
        self.layoutMarco.setSpacing(10)
        self.layoutMarco.setObjectName(u"layoutMarco")
        self.layoutMarco.setContentsMargins(12, 12, 12, 12)
        self.splitterPrincipal = QSplitter(self.marcoPrincipal)
        self.splitterPrincipal.setObjectName(u"splitterPrincipal")
        self.splitterPrincipal.setOrientation(Qt.Vertical)
        self.splitterPrincipal.setHandleWidth(4)
        self.contenedorEditor = QWidget(self.splitterPrincipal)
        self.contenedorEditor.setObjectName(u"contenedorEditor")
        self.layoutEditor = QVBoxLayout(self.contenedorEditor)
        self.layoutEditor.setSpacing(8)
        self.layoutEditor.setObjectName(u"layoutEditor")
        self.layoutEditor.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit = QPlainTextEdit(self.contenedorEditor)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        font = QFont()
        font.setFamilies([u"Monospace"])
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEdit.setTabStopDistance(32.000000000000000)

        self.layoutEditor.addWidget(self.plainTextEdit)

        self.layoutBotonEjecutar = QHBoxLayout()
        self.layoutBotonEjecutar.setObjectName(u"layoutBotonEjecutar")
        self.espaciadorIzquierdo = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutBotonEjecutar.addItem(self.espaciadorIzquierdo)

        self.botonCompilar = QPushButton(self.contenedorEditor)
        self.botonCompilar.setObjectName(u"botonCompilar")
        self.botonCompilar.setMinimumSize(QSize(180, 36))
        self.botonCompilar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutBotonEjecutar.addWidget(self.botonCompilar)


        self.layoutEditor.addLayout(self.layoutBotonEjecutar)

        self.splitterPrincipal.addWidget(self.contenedorEditor)
        self.panelesResultados = QTabWidget(self.splitterPrincipal)
        self.panelesResultados.setObjectName(u"panelesResultados")
        self.pestañasTokens = QWidget()
        self.pestañasTokens.setObjectName(u"pesta\u00f1asTokens")
        self.layoutTokens = QVBoxLayout(self.pestañasTokens)
        self.layoutTokens.setObjectName(u"layoutTokens")
        self.layoutTokens.setContentsMargins(0, 0, 0, 0)
        self.tablaTokens = QTableWidget(self.pestañasTokens)
        if (self.tablaTokens.columnCount() < 3):
            self.tablaTokens.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaTokens.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaTokens.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaTokens.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tablaTokens.setObjectName(u"tablaTokens")
        self.tablaTokens.setAlternatingRowColors(True)
        self.tablaTokens.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaTokens.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaTokens.horizontalHeader().setStretchLastSection(True)
        self.tablaTokens.verticalHeader().setVisible(False)

        self.layoutTokens.addWidget(self.tablaTokens)

        self.panelesResultados.addTab(self.pestañasTokens, "")
        self.pestañasAST = QWidget()
        self.pestañasAST.setObjectName(u"pesta\u00f1asAST")
        self.layoutAST = QVBoxLayout(self.pestañasAST)
        self.layoutAST.setObjectName(u"layoutAST")
        self.layoutAST.setContentsMargins(0, 0, 0, 0)
        self.arbolAST = QTreeWidget(self.pestañasAST)
        self.arbolAST.setObjectName(u"arbolAST")
        self.arbolAST.setAlternatingRowColors(True)

        self.layoutAST.addWidget(self.arbolAST)

        self.panelesResultados.addTab(self.pestañasAST, "")
        self.pestañasErrores = QWidget()
        self.pestañasErrores.setObjectName(u"pesta\u00f1asErrores")
        self.layoutErrores = QVBoxLayout(self.pestañasErrores)
        self.layoutErrores.setObjectName(u"layoutErrores")
        self.layoutErrores.setContentsMargins(0, 0, 0, 0)
        self.tablaErrores = QTableWidget(self.pestañasErrores)
        if (self.tablaErrores.columnCount() < 3):
            self.tablaErrores.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaErrores.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaErrores.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaErrores.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tablaErrores.setObjectName(u"tablaErrores")
        self.tablaErrores.setAlternatingRowColors(True)
        self.tablaErrores.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaErrores.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaErrores.horizontalHeader().setStretchLastSection(True)
        self.tablaErrores.verticalHeader().setVisible(False)

        self.layoutErrores.addWidget(self.tablaErrores)

        self.panelesResultados.addTab(self.pestañasErrores, "")
        self.pestañasSalida = QWidget()
        self.pestañasSalida.setObjectName(u"pesta\u00f1asSalida")
        self.layoutSalida = QVBoxLayout(self.pestañasSalida)
        self.layoutSalida.setObjectName(u"layoutSalida")
        self.layoutSalida.setContentsMargins(0, 0, 0, 0)
        self.textoSalida = QPlainTextEdit(self.pestañasSalida)
        self.textoSalida.setObjectName(u"textoSalida")
        font1 = QFont()
        font1.setFamilies([u"Monospace"])
        font1.setPointSize(10)
        self.textoSalida.setFont(font1)
        self.textoSalida.setReadOnly(True)

        self.layoutSalida.addWidget(self.textoSalida)

        self.panelesResultados.addTab(self.pestañasSalida, "")
        self.splitterPrincipal.addWidget(self.panelesResultados)

        self.layoutMarco.addWidget(self.splitterPrincipal)


        self.layoutCentral.addWidget(self.marcoPrincipal)

        EditorLumo.setCentralWidget(self.centralwidget)
        self.barraMenu = QMenuBar(EditorLumo)
        self.barraMenu.setObjectName(u"barraMenu")
        self.barraMenu.setGeometry(QRect(0, 0, 1200, 30))
        self.menuArchivo = QMenu(self.barraMenu)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuEditar = QMenu(self.barraMenu)
        self.menuEditar.setObjectName(u"menuEditar")
        self.menuAyuda = QMenu(self.barraMenu)
        self.menuAyuda.setObjectName(u"menuAyuda")
        EditorLumo.setMenuBar(self.barraMenu)
        self.barraHerramientas = QToolBar(EditorLumo)
        self.barraHerramientas.setObjectName(u"barraHerramientas")
        self.barraHerramientas.setMovable(False)
        self.barraHerramientas.setToolButtonStyle(Qt.ToolButtonTextOnly)
        EditorLumo.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.barraHerramientas)
        self.barraEstado = QStatusBar(EditorLumo)
        self.barraEstado.setObjectName(u"barraEstado")
        self.barraEstado.setSizeGripEnabled(True)
        EditorLumo.setStatusBar(self.barraEstado)
        QWidget.setTabOrder(self.plainTextEdit, self.botonCompilar)
        QWidget.setTabOrder(self.botonCompilar, self.panelesResultados)
        QWidget.setTabOrder(self.panelesResultados, self.tablaTokens)
        QWidget.setTabOrder(self.tablaTokens, self.arbolAST)
        QWidget.setTabOrder(self.arbolAST, self.tablaErrores)
        QWidget.setTabOrder(self.tablaErrores, self.textoSalida)

        self.barraMenu.addAction(self.menuArchivo.menuAction())
        self.barraMenu.addAction(self.menuEditar.menuAction())
        self.barraMenu.addAction(self.menuAyuda.menuAction())
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionAbrir)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuEditar.addAction(self.actionCopiar)
        self.menuEditar.addAction(self.actionPegar)
        self.menuEditar.addAction(self.actionCortar)
        self.menuAyuda.addAction(self.actionAcercaDe)
        self.barraHerramientas.addAction(self.actionNuevo)
        self.barraHerramientas.addAction(self.actionAbrir)
        self.barraHerramientas.addAction(self.actionGuardar)
        self.barraHerramientas.addSeparator()
        self.barraHerramientas.addAction(self.actionCopiar)
        self.barraHerramientas.addAction(self.actionPegar)
        self.barraHerramientas.addAction(self.actionCortar)

        self.retranslateUi(EditorLumo)

        self.panelesResultados.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(EditorLumo)
    # setupUi

    def retranslateUi(self, EditorLumo):
        EditorLumo.setWindowTitle(QCoreApplication.translate("EditorLumo", u"Editor Lumo", None))
        self.actionNuevo.setText(QCoreApplication.translate("EditorLumo", u"Nuevo", None))
#if QT_CONFIG(shortcut)
        self.actionNuevo.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbrir.setText(QCoreApplication.translate("EditorLumo", u"Abrir", None))
#if QT_CONFIG(shortcut)
        self.actionAbrir.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionGuardar.setText(QCoreApplication.translate("EditorLumo", u"Guardar", None))
#if QT_CONFIG(shortcut)
        self.actionGuardar.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionCopiar.setText(QCoreApplication.translate("EditorLumo", u"Copiar", None))
#if QT_CONFIG(shortcut)
        self.actionCopiar.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionPegar.setText(QCoreApplication.translate("EditorLumo", u"Pegar", None))
#if QT_CONFIG(shortcut)
        self.actionPegar.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.actionCortar.setText(QCoreApplication.translate("EditorLumo", u"Cortar", None))
#if QT_CONFIG(shortcut)
        self.actionCortar.setShortcut(QCoreApplication.translate("EditorLumo", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionAcercaDe.setText(QCoreApplication.translate("EditorLumo", u"Acerca de", None))
        self.plainTextEdit.setPlaceholderText(QCoreApplication.translate("EditorLumo", u"// Escribe tu codigo Lumo aqui...", None))
#if QT_CONFIG(tooltip)
        self.botonCompilar.setToolTip(QCoreApplication.translate("EditorLumo", u"Compilar y ejecutar el codigo (F5)", None))
#endif // QT_CONFIG(tooltip)
        self.botonCompilar.setText(QCoreApplication.translate("EditorLumo", u"\u25b6  Compilar / Ejecutar", None))
#if QT_CONFIG(shortcut)
        self.botonCompilar.setShortcut(QCoreApplication.translate("EditorLumo", u"F5", None))
#endif // QT_CONFIG(shortcut)
        ___qtablewidgetitem = self.tablaTokens.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("EditorLumo", u"Linea", None))
        ___qtablewidgetitem1 = self.tablaTokens.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("EditorLumo", u"Tipo", None))
        ___qtablewidgetitem2 = self.tablaTokens.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("EditorLumo", u"Lexema", None))
        self.panelesResultados.setTabText(self.panelesResultados.indexOf(self.pestañasTokens), QCoreApplication.translate("EditorLumo", u"Tokens", None))
        ___qtreewidgetitem = self.arbolAST.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("EditorLumo", u"Nodo", None))
        self.panelesResultados.setTabText(self.panelesResultados.indexOf(self.pestañasAST), QCoreApplication.translate("EditorLumo", u"AST", None))
        ___qtablewidgetitem3 = self.tablaErrores.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("EditorLumo", u"Linea", None))
        ___qtablewidgetitem4 = self.tablaErrores.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("EditorLumo", u"Columna", None))
        ___qtablewidgetitem5 = self.tablaErrores.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("EditorLumo", u"Descripcion", None))
        self.panelesResultados.setTabText(self.panelesResultados.indexOf(self.pestañasErrores), QCoreApplication.translate("EditorLumo", u"Errores", None))
        self.textoSalida.setPlaceholderText(QCoreApplication.translate("EditorLumo", u"La salida del programa aparecera aqui...", None))
        self.panelesResultados.setTabText(self.panelesResultados.indexOf(self.pestañasSalida), QCoreApplication.translate("EditorLumo", u"Salida", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("EditorLumo", u"&Archivo", None))
        self.menuEditar.setTitle(QCoreApplication.translate("EditorLumo", u"&Editar", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("EditorLumo", u"A&yuda", None))
        self.barraHerramientas.setWindowTitle(QCoreApplication.translate("EditorLumo", u"Barra de herramientas", None))
    # retranslateUi

