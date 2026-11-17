"""Nodos del árbol de sintaxis abstracta de Lumo."""

from dataclasses import dataclass, field
from typing import Union


@dataclass
class Program:
    declarations: list["Declaration"] = field(default_factory=list)


@dataclass
class Block:
    statements: list["Statement"] = field(default_factory=list)


@dataclass
class Parameter:
    type_name: str
    name: str


@dataclass
class VarDeclaration:
    type_name: str
    name: str
    initializer: "Expression"


@dataclass
class FunctionDeclaration:
    return_type: str
    name: str
    parameters: list[Parameter]
    body: Block


@dataclass
class Assignment:
    name: str
    value: "Expression"


@dataclass
class PrintStatement:
    expression: "Expression"


@dataclass
class IfStatement:
    condition: "Expression"
    then_branch: Block
    else_branch: Block | None = None


@dataclass
class WhileStatement:
    condition: "Expression"
    body: Block


@dataclass
class ReturnStatement:
    value: "Expression | None" = None


@dataclass
class ExpressionStatement:
    expression: "Expression"


@dataclass
class Literal:
    value: object


@dataclass
class Variable:
    name: str


@dataclass
class Unary:
    operator: str
    operand: "Expression"


@dataclass
class Binary:
    left: "Expression"
    operator: str
    right: "Expression"


@dataclass
class Call:
    name: str
    arguments: list["Expression"] = field(default_factory=list)


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
