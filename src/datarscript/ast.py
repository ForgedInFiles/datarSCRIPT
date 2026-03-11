"""Abstract Syntax Tree node classes for DatarScript."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar


T = TypeVar("T")


# Statement nodes
class Stmt:
    pass


@dataclass
class Program(Stmt):
    body: list[Stmt]


@dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclass
class Assign(Stmt):
    target: str
    value: Expr


@dataclass
class If(Stmt):
    condition: Expr
    then_body: list[Stmt]
    elif_branches: list[tuple[Expr, list[Stmt]]] = field(default_factory=list)
    else_body: list[Stmt] | None = None


@dataclass
class While(Stmt):
    condition: Expr
    body: list[Stmt]


@dataclass
class For(Stmt):
    target: str
    iterable: Expr
    body: list[Stmt]


@dataclass
class FunctionDef(Stmt):
    name: str
    params: list[str]
    defaults: dict[str, Expr] = field(default_factory=dict)
    body: list[Stmt] = field(default_factory=list)


@dataclass
class Return(Stmt):
    value: Expr | None = None


@dataclass
class Try(Stmt):
    body: list[Stmt]
    catches: list[Catch] = field(default_factory=list)
    finally_body: list[Stmt] | None = None


@dataclass
class Catch(Stmt):
    exception_type: str | None  # e.g., "division by zero error"
    var: str | None  # variable to store error message
    body: list[Stmt]


@dataclass
class Break(Stmt):
    pass


@dataclass
class Continue(Stmt):
    pass


# Expression nodes
class Expr:
    pass


@dataclass
class Literal(Expr, Generic[T]):
    value: T


@dataclass
class Variable(Expr):
    name: str


@dataclass
class Binary(Expr):
    left: Expr
    op: str  # 'plus', 'minus', 'times', 'divided by', 'modulo', 'raised to', etc.
    right: Expr


@dataclass
class Compare(Expr):
    left: Expr
    op: str  # 'is equal to', 'is not equal to', etc.
    right: Expr


@dataclass
class Call(Expr):
    func: Expr
    args: list[Expr]


@dataclass
class GetDictValue(Expr):
    key: Expr
    container: Expr


@dataclass
class ItemAt(Expr):
    index: Expr
    container: Expr


@dataclass
class Attribute(Expr):
    obj: Expr
    attr: str


@dataclass
class Unary(Expr):
    op: str  # 'not'
    expr: Expr


# Utility nodes
@dataclass
class ListExpr(Expr):
    elements: list[Expr]


@dataclass
class TupleExpr(Expr):
    elements: list[Expr]


@dataclass
class DictExpr(Expr):
    keys: list[str]
    values: list[Expr]
