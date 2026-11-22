
from dataclasses import dataclass, field
from typing import Union


@dataclass
class Program:
    declarations: list["Declaration"] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class Block:
    statements: list["Statement"] = field(default_factory=list)


@dataclass
class Parameter:
    type_name: str
    name: str
    line: int = 1
    column: int = 1


@dataclass
class VarDeclaration:
    type_name: str
    name: str
    initializer: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class FunctionDeclaration:
    return_type: str
    name: str
    parameters: list[Parameter]
    body: Block
    line: int = 1
    column: int = 1


@dataclass
class Assignment:
    name: str
    value: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class PrintStatement:
    expression: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class IfStatement:
    condition: "Expression"
    then_branch: Block
    else_branch: Block | None = None
    line: int = 1
    column: int = 1


@dataclass
class WhileStatement:
    condition: "Expression"
    body: Block
    line: int = 1
    column: int = 1


@dataclass
class ReturnStatement:
    value: "Expression | None" = None
    line: int = 1
    column: int = 1


@dataclass
class ExpressionStatement:
    expression: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class Literal:
    value: object
    line: int = 1
    column: int = 1


@dataclass
class Variable:
    name: str
    line: int = 1
    column: int = 1


@dataclass
class Unary:
    operator: str
    operand: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class Binary:
    left: "Expression"
    operator: str
    right: "Expression"
    line: int = 1
    column: int = 1


@dataclass
class Call:
    name: str
    arguments: list["Expression"] = field(default_factory=list)
    line: int = 1
    column: int = 1


Statement = Union[
    VarDeclaration,
    Assignment,
    PrintStatement,
    IfStatement,
    WhileStatement,
    ReturnStatement,
    ExpressionStatement,
]
Declaration = Union[VarDeclaration, FunctionDeclaration, Statement]
Expression = Union[Literal, Variable, Unary, Binary, Call]
