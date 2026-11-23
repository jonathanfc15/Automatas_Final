"""Analizador sintáctico de Lumo, construido con PLY (``ply.yacc``).

Aquí están las producciones (la gramática) del lenguaje. Cada función ``p_...``
tiene como docstring la regla de la gramática y su cuerpo construye el nodo
del árbol (AST) definido en ``compiler/ast.py``.

Gramática de Lumo (resumen):

    program          : declaration*
    declaration      : var_declaration | function_declaration | statement
    var_declaration  : TYPE IDENTIFIER '=' expression ';'
    function_decl    : 'funchion' TYPE IDENTIFIER '(' parameters? ')' block
    statement        : print | if | while | return | assignment | expression ';'
    block            : '{' declaration* '}'
"""

import sys

import ply.lex as lex
import ply.yacc as yacc

from compiler import ast
from compiler.lexer import tokens  # noqa: F401  (PLY necesita `tokens` en este módulo)
from compiler.tokens import Token, TokenType


class ParserError(Exception):
    """Error sintáctico con ubicación en el código fuente.

    ``errors`` contiene todos los errores sintácticos encontrados (el primero
    es el propio objeto), para poder mostrarlos juntos.
    """

    def __init__(self, message: str, token: Token):
        super().__init__(f"Línea {token.line}, columna {token.column}: {message}")
        self.message = message
        self.line = token.line
        self.column = token.column
        self.errors: list["ParserError"] = [self]


# --------------------------------------------------------------------------
# Precedencia y asociatividad (de menor a mayor prioridad)
# --------------------------------------------------------------------------
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "EQUAL_EQUAL", "NOT_EQUAL"),
    ("left", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "STAR", "SLASH", "PERCENT"),
    ("right", "UNARY"),
)

start = "program"


# --------------------------------------------------------------------------
# Programa y declaraciones
# --------------------------------------------------------------------------
def p_program(p):
    "program : declaration_list"
    p[0] = ast.Program(p[1])


def p_declaration_list_many(p):
    "declaration_list : declaration_list declaration"
    if p[2] is not None:  # None = instrucción descartada por recuperación de errores
        p[1].append(p[2])
    p[0] = p[1]


def p_declaration_list_empty(p):
    "declaration_list : empty"
    p[0] = []


def p_empty(p):
    "empty :"


def p_declaration(p):
    """declaration : var_declaration
                   | function_declaration
                   | statement"""
    p[0] = p[1]


def p_declaration_error(p):
    "declaration : error SEMICOLON"
    # Recuperación de errores: se descarta hasta el siguiente ';' y se sigue
    # analizando, para poder reportar más de un error sintáctico.
    p[0] = None


def p_var_declaration(p):
    "var_declaration : TYPE IDENTIFIER EQUAL expression SEMICOLON"
    p[0] = ast.VarDeclaration(p[1].lexeme, p[2].lexeme, p[4], p[2].line, p[2].column)


def p_function_declaration(p):
    "function_declaration : FUNCTION TYPE IDENTIFIER LEFT_PAREN parameters RIGHT_PAREN block"
    p[0] = ast.FunctionDeclaration(p[2].lexeme, p[3].lexeme, p[5], p[7], p[3].line, p[3].column)


def p_parameters_empty(p):
    "parameters : empty"
    p[0] = []


def p_parameters_list(p):
    "parameters : parameter_list"
    p[0] = p[1]


def p_parameter_list_many(p):
    "parameter_list : parameter_list COMMA parameter"
    p[1].append(p[3])
    p[0] = p[1]


def p_parameter_list_one(p):
    "parameter_list : parameter"
    p[0] = [p[1]]


def p_parameter(p):
    "parameter : TYPE IDENTIFIER"
    p[0] = ast.Parameter(p[1].lexeme, p[2].lexeme, p[2].line, p[2].column)


# --------------------------------------------------------------------------
# Instrucciones
# --------------------------------------------------------------------------
def p_statement(p):
    """statement : print_statement
                 | if_statement
                 | while_statement
                 | return_statement
                 | assignment
                 | expression_statement"""
    p[0] = p[1]


def p_print_statement(p):
    "print_statement : PRINT LEFT_PAREN expression RIGHT_PAREN SEMICOLON"
    p[0] = ast.PrintStatement(p[3], p[1].line, p[1].column)


def p_if_statement(p):
    "if_statement : IF expression block"
    p[0] = ast.IfStatement(p[2], p[3], None, p[1].line, p[1].column)


def p_if_else_statement(p):
    "if_statement : IF expression block ELSE block"
    p[0] = ast.IfStatement(p[2], p[3], p[5], p[1].line, p[1].column)


def p_while_statement(p):
    "while_statement : WHILE expression block"
    p[0] = ast.WhileStatement(p[2], p[3], p[1].line, p[1].column)


def p_return_statement(p):
    "return_statement : RETURN SEMICOLON"
    p[0] = ast.ReturnStatement(None, p[1].line, p[1].column)


def p_return_value_statement(p):
    "return_statement : RETURN expression SEMICOLON"
    p[0] = ast.ReturnStatement(p[2], p[1].line, p[1].column)


def p_assignment(p):
    "assignment : IDENTIFIER EQUAL expression SEMICOLON"
    p[0] = ast.Assignment(p[1].lexeme, p[3], p[1].line, p[1].column)


def p_expression_statement(p):
    "expression_statement : expression SEMICOLON"
    p[0] = ast.ExpressionStatement(p[1], p[1].line, p[1].column)


def p_block(p):
    "block : LEFT_BRACE declaration_list RIGHT_BRACE"
    p[0] = ast.Block(p[2])


# --------------------------------------------------------------------------
# Expresiones
# --------------------------------------------------------------------------
def p_expression_binary(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression STAR expression
                  | expression SLASH expression
                  | expression PERCENT expression
                  | expression LESS expression
                  | expression LESS_EQUAL expression
                  | expression GREATER expression
                  | expression GREATER_EQUAL expression
                  | expression EQUAL_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression AND expression
                  | expression OR expression"""
    p[0] = ast.Binary(p[1], p[2].lexeme, p[3], p[2].line, p[2].column)


def p_expression_unary(p):
    """expression : MINUS expression %prec UNARY
                  | NOT expression %prec UNARY"""
    p[0] = ast.Unary(p[1].lexeme, p[2], p[1].line, p[1].column)


def p_expression_group(p):
    "expression : LEFT_PAREN expression RIGHT_PAREN"
    p[0] = p[2]


def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = ast.Literal(int(p[1].lexeme), p[1].line, p[1].column)


def p_expression_decimal(p):
    "expression : DECIMAL"
    p[0] = ast.Literal(float(p[1].lexeme), p[1].line, p[1].column)


def p_expression_string(p):
    "expression : STRING"
    p[0] = ast.Literal(p[1].lexeme, p[1].line, p[1].column)


def p_expression_true(p):
    "expression : TRUE"
    p[0] = ast.Literal(True, p[1].line, p[1].column)


def p_expression_false(p):
    "expression : FALSE"
    p[0] = ast.Literal(False, p[1].line, p[1].column)


def p_expression_variable(p):
    "expression : IDENTIFIER"
    p[0] = ast.Variable(p[1].lexeme, p[1].line, p[1].column)


def p_expression_call(p):
    "expression : IDENTIFIER LEFT_PAREN arguments RIGHT_PAREN"
    p[0] = ast.Call(p[1].lexeme, p[3], p[1].line, p[1].column)


def p_arguments_empty(p):
    "arguments : empty"
    p[0] = []


def p_arguments_list(p):
    "arguments : argument_list"
    p[0] = p[1]


def p_argument_list_many(p):
    "argument_list : argument_list COMMA expression"
    p[1].append(p[3])
    p[0] = p[1]


def p_argument_list_one(p):
    "argument_list : expression"
    p[0] = [p[1]]


# --------------------------------------------------------------------------
# Manejo de errores sintácticos
# --------------------------------------------------------------------------
_EXPRESSION_START = {
    "INTEGER", "DECIMAL", "STRING", "IDENTIFIER", "TRUE", "FALSE",
    "LEFT_PAREN", "MINUS", "NOT",
}

_FRIENDLY_NAMES = {
    "INTEGER": "un número entero", "DECIMAL": "un número decimal",
    "STRING": "una cadena", "IDENTIFIER": "un identificador",
    "TYPE": "un tipo (ent, dec, txt, bool)", "IF": "'simon'", "ELSE": "'nosimon'",
    "WHILE": "'mientras'", "FUNCTION": "'funchion'", "RETURN": "'retorno'",
    "PRINT": "'muestrame'", "TRUE": "'verdad'", "FALSE": "'falso'",
    "AND": "'Y'", "OR": "'O'", "NOT": "'NONES'",
    "PLUS": "'+'", "MINUS": "'-'", "STAR": "'*'", "SLASH": "'/'", "PERCENT": "'%'",
    "EQUAL": "'='", "EQUAL_EQUAL": "'=='", "NOT_EQUAL": "'!='",
    "LESS": "'<'", "LESS_EQUAL": "'<='", "GREATER": "'>'", "GREATER_EQUAL": "'>='",
    "LEFT_PAREN": "'('", "RIGHT_PAREN": "')'", "LEFT_BRACE": "'{'", "RIGHT_BRACE": "'}'",
    "COMMA": "','", "SEMICOLON": "';'",
}


class _TokenStream:
    """Entrega a PLY los tokens ya generados por el lexer.

    PLY pide los tokens uno por uno con ``token()`` y espera ``None`` al llegar
    al final del programa. También recuerda los últimos tokens leídos y los
    errores, para armar mensajes claros.
    """

    def __init__(self, token_list: list[Token]):
        self.tokens = token_list
        self.index = 0
        self.current: Token | None = None
        self.previous: Token | None = None
        self.errors: list[ParserError] = []
        if token_list and token_list[-1].type == TokenType.EOF:
            self.eof = token_list[-1]
        else:
            self.eof = Token(TokenType.EOF, "", 1, 1)

    def token(self):
        if self.index >= len(self.tokens):
            return None
        token = self.tokens[self.index]
        self.index += 1
        if token.type == TokenType.EOF:
            return None
        self.previous, self.current = self.current, token
        ply_token = lex.LexToken()
        ply_token.type = token.type.name
        ply_token.value = token  # las reglas leen lexema, línea y columna de aquí
        ply_token.lineno = token.line
        ply_token.lexpos = 0
        return ply_token


_stream: _TokenStream | None = None


def _end_of(token: Token) -> Token:
    """Posición justo después de ``token`` (donde habría que escribir algo)."""
    length = len(token.lexeme) + (2 if token.type == TokenType.STRING else 0)
    return Token(token.type, token.lexeme, token.line, token.column + length)


def _describe(token: Token | None) -> str:
    if token is None:
        return "el fin del programa"
    if token.type == TokenType.STRING:
        return f'"{token.lexeme}"'
    return f"'{token.lexeme}'"


def _would_shift(stack: list[int], token_name: str) -> bool:
    """Simula la tabla LALR para saber si ``token_name`` sería aceptado.

    Una misma celda de la tabla puede traer tokens que solo son válidos
    "después de reducir"; al simular las reducciones se obtiene la lista real
    de lo que el parser esperaba en ese punto.
    """
    stack = list(stack)
    while True:
        state = stack[-1]
        action = parser.defaulted_states.get(state)
        if action is None:
            action = parser.action[state].get(token_name)
        if action is None:
            return False
        if action >= 0:  # desplazar (o aceptar)
            return True
        production = parser.productions[-action]
        if production.len:
            del stack[-production.len:]
        stack.append(parser.goto[stack[-1]][production.name])


def _expected_tokens() -> set[str]:
    state = parser.statestack[-1]
    candidates = set(parser.action.get(state, {})) - {"error"}
    return {name for name in candidates if _would_shift(parser.statestack, name)}


def _build_error(token, expected: set[str]) -> ParserError:
    stream = _stream
    found = token.value if token is not None else None
    at_found = found or stream.eof

    if (
        found is not None
        and found.type == TokenType.RIGHT_BRACE
        and not {"RIGHT_BRACE", "SEMICOLON", "RIGHT_PAREN"} & expected
    ):
        message = "'}' sin su '{' correspondiente"
        location = at_found
    elif found is not None and found.type == TokenType.ELSE and "ELSE" not in expected:
        message = "'nosimon' sin un 'simon' antes"
        location = at_found
    elif found is None and "RIGHT_BRACE" in expected:
        message = "se esperaba '}' para cerrar el bloque, pero el programa terminó"
        location = stream.eof
    elif {"TYPE", "PRINT"} <= expected:
        message = f"se esperaba una declaración o instrucción, pero se encontró {_describe(found)}"
        location = at_found
    elif _EXPRESSION_START <= expected:
        message = f"se esperaba una expresión, pero se encontró {_describe(found)}"
        location = at_found
    elif "SEMICOLON" in expected:
        before = stream.current if found is None else stream.previous
        message = "se esperaba ';' al final de la instrucción"
        if found is not None:
            message += f" (se encontró {_describe(found)})"
        location = _end_of(before) if before is not None else at_found
    elif "RIGHT_PAREN" in expected:
        message = f"se esperaba ')', pero se encontró {_describe(found)}"
        location = at_found
    elif "LEFT_BRACE" in expected:
        message = f"se esperaba '{{' para abrir el bloque, pero se encontró {_describe(found)}"
        location = at_found
    elif 0 < len(expected) <= 4:
        options = [_FRIENDLY_NAMES.get(name, name) for name in sorted(expected - {"$end"})] or [
            "el fin del programa"
        ]
        wanted = options[0] if len(options) == 1 else ", ".join(options[:-1]) + " o " + options[-1]
        message = f"se esperaba {wanted}, pero se encontró {_describe(found)}"
        location = at_found
    else:
        message = f"{_describe(found)} no es válido en este lugar"
        location = at_found
    return ParserError(message, location)


def p_error(token):
    # Lo que el parser aceptaba en el punto donde falló el análisis: con eso
    # el mensaje puede decir exactamente qué se esperaba.
    _stream.errors.append(_build_error(token, _expected_tokens()))


# Construye el parser a partir de las producciones de este módulo.
parser = yacc.yacc(
    module=sys.modules[__name__],
    write_tables=False,
    debug=False,
    errorlog=yacc.NullLogger(),
)


# --------------------------------------------------------------------------
# Interfaz que usa el resto del proyecto
# --------------------------------------------------------------------------
class Parser:
    """Convierte una secuencia de tokens en un AST usando el parser de PLY."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.errors: list[ParserError] = []

    def parse_all(self) -> tuple[ast.Program | None, list[ParserError]]:
        """Analiza sin detenerse en el primer error.

        Regresa ``(programa, errores)``. Si hay errores el programa no es
        confiable y debe ignorarse.
        """
        global _stream
        _stream = _TokenStream(self.tokens)
        program = parser.parse(lexer=_stream)
        self.errors = _stream.errors
        _stream = None
        return program, self.errors

    def parse(self) -> ast.Program:
        """Analiza el programa; si hay errores lanza ``ParserError``.

        La excepción es el primer error y su atributo ``errors`` trae todos.
        """
        program, errors = self.parse_all()
        if errors:
            first = errors[0]
            first.errors = list(errors)
            raise first
        return program
