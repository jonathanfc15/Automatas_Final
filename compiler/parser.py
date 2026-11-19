"""Analizador sintáctico descendente recursivo para Lumo."""

from compiler import ast
from compiler.tokens import Token, TokenType


class ParserError(Exception):
    """Error sintáctico con ubicación en el código fuente."""

    def __init__(self, message: str, token: Token):
        super().__init__(f"Línea {token.line}, columna {token.column}: {message}")
        self.message = message
        self.line = token.line
        self.column = token.column


class Parser:
    """Convierte una secuencia de tokens en un AST."""

    TYPE_NAMES = {"ent", "dec", "txt", "bool"}

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> ast.Program:
        declarations = []
        while not self._check(TokenType.EOF):
            declarations.append(self._declaration())
        return ast.Program(declarations)

    def _declaration(self):
        if self._check(TokenType.TYPE):
            return self._variable_declaration()
        if self._match(TokenType.FUNCTION):
            return self._function_declaration()
        return self._statement()

    def _variable_declaration(self) -> ast.VarDeclaration:
        type_token = self._advance()
        if type_token.lexeme not in self.TYPE_NAMES:
            raise ParserError(f"tipo no válido: {type_token.lexeme}", type_token)
        name = self._consume(TokenType.IDENTIFIER, "se esperaba el nombre de la variable")
        self._consume(TokenType.EQUAL, "se esperaba '=' en la declaración")
        initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "se esperaba ';' al final de la declaración")
        return ast.VarDeclaration(type_token.lexeme, name.lexeme, initializer)

    def _function_declaration(self) -> ast.FunctionDeclaration:
        return_type = self._consume(TokenType.TYPE, "se esperaba el tipo de retorno")
        name = self._consume(TokenType.IDENTIFIER, "se esperaba el nombre de la función")
        self._consume(TokenType.LEFT_PAREN, "se esperaba '(' después del nombre")
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                parameter_type = self._consume(TokenType.TYPE, "se esperaba el tipo del parámetro")
                parameter_name = self._consume(TokenType.IDENTIFIER, "se esperaba el nombre del parámetro")
                parameters.append(ast.Parameter(parameter_type.lexeme, parameter_name.lexeme))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_PAREN, "se esperaba ')' después de los parámetros")
        return ast.FunctionDeclaration(return_type.lexeme, name.lexeme, parameters, self._block())

    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()
        if self._check(TokenType.IDENTIFIER) and self._check_next(TokenType.EQUAL):
            return self._assignment()
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "se esperaba ';' después de la expresión")
        return ast.ExpressionStatement(expression)

    def _print_statement(self) -> ast.PrintStatement:
        self._consume(TokenType.LEFT_PAREN, "se esperaba '(' después de muestrame")
        expression = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "se esperaba ')' después de la expresión")
        self._consume(TokenType.SEMICOLON, "se esperaba ';' después de muestrame")
        return ast.PrintStatement(expression)

    def _if_statement(self) -> ast.IfStatement:
        condition = self._expression()
        then_branch = self._block()
        else_branch = self._block() if self._match(TokenType.ELSE) else None
        return ast.IfStatement(condition, then_branch, else_branch)

    def _while_statement(self) -> ast.WhileStatement:
        condition = self._expression()
        return ast.WhileStatement(condition, self._block())

    def _return_statement(self) -> ast.ReturnStatement:
        value = None if self._check(TokenType.SEMICOLON) else self._expression()
        self._consume(TokenType.SEMICOLON, "se esperaba ';' después de retorno")
        return ast.ReturnStatement(value)

    def _assignment(self) -> ast.Assignment:
        name = self._advance()
        self._consume(TokenType.EQUAL, "se esperaba '=' en la asignación")
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "se esperaba ';' después de la asignación")
        return ast.Assignment(name.lexeme, value)

    def _block(self) -> ast.Block:
        self._consume(TokenType.LEFT_BRACE, "se esperaba '{'")
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._check(TokenType.EOF):
            statements.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "se esperaba '}' al cerrar el bloque")
        return ast.Block(statements)

    def _expression(self):
        return self._logical_or()

    def _logical_or(self):
        expression = self._logical_and()
        while self._match(TokenType.OR):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._logical_and())
        return expression

    def _logical_and(self):
        expression = self._equality()
        while self._match(TokenType.AND):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._equality())
        return expression

    def _equality(self):
        expression = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._comparison())
        return expression

    def _comparison(self):
        expression = self._term()
        while self._match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._term())
        return expression

    def _term(self):
        expression = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._factor())
        return expression

    def _factor(self):
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self._previous()
            expression = ast.Binary(expression, operator.lexeme, self._unary())
        return expression

    def _unary(self):
        if self._match(TokenType.MINUS, TokenType.NOT):
            operator = self._previous()
            return ast.Unary(operator.lexeme, self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.INTEGER):
            return ast.Literal(int(self._previous().lexeme))
        if self._match(TokenType.DECIMAL):
            return ast.Literal(float(self._previous().lexeme))
        if self._match(TokenType.STRING):
            return ast.Literal(self._previous().lexeme)
        if self._match(TokenType.TRUE):
            return ast.Literal(True)
        if self._match(TokenType.FALSE):
            return ast.Literal(False)
        if self._match(TokenType.IDENTIFIER):
            name = self._previous().lexeme
            if self._match(TokenType.LEFT_PAREN):
                arguments = []
                if not self._check(TokenType.RIGHT_PAREN):
                    while True:
                        arguments.append(self._expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RIGHT_PAREN, "se esperaba ')' después de los argumentos")
                return ast.Call(name, arguments)
            return ast.Variable(name)
        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "se esperaba ')'")
            return expression
        raise ParserError("se esperaba una expresión", self._peek())

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(message, self._peek())

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type

    def _check_next(self, token_type: TokenType) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def _advance(self) -> Token:
        if not self._check(TokenType.EOF):
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]
