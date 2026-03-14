"""Interpreter: evaluates AST nodes to execute DatarScript programs."""

from __future__ import annotations

from typing import Any
from .errors import (
    DatarError,
    DatarNameError,
    DatarTypeError,
    DatarRuntimeError,
    BreakSignal,
    ContinueSignal,
    ReturnSignal,
)
from .ast import *
from .builtins.base import BuiltinRegistry


class Environment:
    """Lexical scoping environment for variables."""

    def __init__(self, parent: Environment | None = None):
        self._store: dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        key = name.lower()
        if key in self._store:
            return self._store[key]
        if self.parent:
            return self.parent.get(key)
        raise DatarNameError(f"Undefined variable: '{name}'")

    def set(self, name: str, value: Any) -> None:
        self._store[name.lower()] = value

    def assign(self, name: str, value: Any) -> None:
        key = name.lower()
        if key in self._store:
            self._store[key] = value
            return
        if self.parent and self.parent._has(key):
            self.parent.assign(key, value)
            return
        self._store[key] = value

    def _has(self, name: str) -> bool:
        key = name.lower()
        return key in self._store or (self.parent is not None and self.parent._has(key))


KEY_CONSTANTS = {
    # Basic keys
    "space": " ",
    "enter": "\r",
    "newline": "\n",       # some terminals send \n for Enter
    "escape": "\x1b",
    "tab": "\t",
    "backspace": "\x7f",   # DEL — standard on modern terminals
    "backspace2": "\x08",  # BS  — older terminals / some configs
    # Arrow keys (standard ANSI CSI sequences)
    "uparrow": "\x1b[A",
    "downarrow": "\x1b[B",
    "rightarrow": "\x1b[C",
    "leftarrow": "\x1b[D",
    # Navigation keys
    "home": "\x1b[H",
    "end": "\x1b[F",
    "pageup": "\x1b[5~",
    "pagedown": "\x1b[6~",
    "delete": "\x1b[3~",
    "insert": "\x1b[2~",
    # Function keys (xterm / most modern terminals)
    "f1": "\x1bOP",
    "f2": "\x1bOQ",
    "f3": "\x1bOR",
    "f4": "\x1bOS",
    "f5": "\x1b[15~",
    "f6": "\x1b[17~",
    "f7": "\x1b[18~",
    "f8": "\x1b[19~",
    "f9": "\x1b[20~",
    "f10": "\x1b[21~",
    "f11": "\x1b[23~",
    "f12": "\x1b[24~",
}


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.builtins = BuiltinRegistry.get_all()
        # Register builtins as global variables with special call handling
        # We'll store them separately; call node checks builtins first
        self._builtin_functions = self.builtins
        # Named key constants available as variables in every script
        for name, value in KEY_CONSTANTS.items():
            self.global_env.set(name, value)

    def run(self, source: str) -> None:
        from .lexer import Lexer
        from .parser import Parser

        tokens = Lexer(source).tokens
        self.program = Parser(tokens).parse_program()
        self._exec(self.program.body, self.global_env)

    # ── Execution ─────────────────────────────────────────────────────────────

    def _exec(self, stmts: list[Stmt], env: Environment) -> None:
        for stmt in stmts:
            self._exec_stmt(stmt, env)

    def _exec_stmt(self, stmt: Stmt, env: Environment) -> None:
        if isinstance(stmt, ExprStmt):
            self._eval(stmt.expr, env)
        elif isinstance(stmt, Assign):
            value = self._eval(stmt.value, env)
            env.assign(stmt.target, value)
        elif isinstance(stmt, If):
            cond = self._eval_boolean(stmt.condition, env)
            if cond:
                self._exec(stmt.then_body, env)
            elif stmt.elif_branches:
                for elif_cond, elif_body in stmt.elif_branches:
                    if self._eval_boolean(elif_cond, env):
                        self._exec(elif_body, env)
                        break
            elif stmt.else_body:
                self._exec(stmt.else_body, env)
        elif isinstance(stmt, While):
            while self._eval_boolean(stmt.condition, env):
                try:
                    self._exec(stmt.body, env)
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        elif isinstance(stmt, For):
            # For numeric range (Call to range_inclusive) build range
            if (
                isinstance(stmt.iterable, Call)
                and isinstance(stmt.iterable.func, Variable)
                and stmt.iterable.func.name == "range_inclusive"
            ):
                args = [self._eval(arg, env) for arg in stmt.iterable.args]
                start = args[0]
                end = args[1]
                iterable = list(range(start, end + 1))
            else:
                iterable = self._eval(stmt.iterable, env)
            for item in iterable:
                loop_env = Environment(parent=env)
                loop_env.set(stmt.target, item)
                try:
                    self._exec(stmt.body, loop_env)
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        elif isinstance(stmt, FunctionDef):
            # Store function as closure
            closure_env = env
            env.set(
                stmt.name,
                {
                    "type": "function",
                    "params": stmt.params,
                    "defaults": stmt.defaults,
                    "body": stmt.body,
                    "closure_env": closure_env,
                },
            )
        elif isinstance(stmt, Return):
            if stmt.value is not None:
                raise ReturnSignal(self._eval(stmt.value, env))
            else:
                raise ReturnSignal(None)
        elif isinstance(stmt, Try):
            try:
                self._exec(stmt.body, env)
            except DatarError as e:
                caught = False
                for catch in stmt.catches:
                    if catch.exception_type is None:
                        caught = True
                    else:
                        # Simple substring match for error types
                        if catch.exception_type.lower() in e.msg.lower():
                            caught = True
                    if caught:
                        catch_env = Environment(parent=env)
                        if catch.var:
                            catch_env.set(catch.var, e.msg)
                        self._exec(catch.body, catch_env)
                        break
                if not caught:
                    raise
            finally:
                if stmt.finally_body:
                    self._exec(stmt.finally_body, env)
        elif isinstance(stmt, Match):
            subject_val = self._eval(stmt.subject, env)
            matched = False
            for case_expr, case_body in stmt.cases:
                case_val = self._eval(case_expr, env)
                if subject_val == case_val:
                    self._exec(case_body, env)
                    matched = True
                    break
            if not matched and stmt.otherwise_body:
                self._exec(stmt.otherwise_body, env)
        elif isinstance(stmt, Break):
            raise BreakSignal()
        elif isinstance(stmt, Continue):
            raise ContinueSignal()
        else:
            raise DatarRuntimeError(f"Unknown statement type: {type(stmt).__name__}")

    def _eval(self, expr: Expr, env: Environment) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Variable):
            name = expr.name
            if name in self._builtin_functions:
                # For builtins, we need to return a callable wrapper that will
                # be called when the Call node evaluates it
                return self._builtin_functions[name]
            return env.get(name)
        if isinstance(expr, Binary):
            left = self._eval(expr.left, env)
            right = self._eval(expr.right, env)
            return self._apply_binary(
                op=expr.op,
                left=left,
                right=right,
                lineno=expr.lineno if hasattr(expr, "lineno") else None,
            )
        if isinstance(expr, Compare):
            left = self._eval(expr.left, env)
            right = self._eval(expr.right, env)
            return self._apply_compare(
                op=expr.op,
                left=left,
                right=right,
                lineno=expr.lineno if hasattr(expr, "lineno") else None,
            )
        if isinstance(expr, Call):
            func = self._eval(expr.func, env)
            args = [self._eval(arg, env) for arg in expr.args]
            return self._call(
                func, args, expr.lineno if hasattr(expr, "lineno") else None
            )
        if isinstance(expr, GetDictValue):
            container = self._eval(expr.container, env)
            if not isinstance(container, dict):
                raise DatarTypeError(
                    "Cannot get value from non-dictionary",
                    lineno=expr.lineno if hasattr(expr, "lineno") else None,
                )
            key = self._eval(expr.key, env)
            return container.get(str(key))
        if isinstance(expr, ItemAt):
            container = self._eval(expr.container, env)
            if not isinstance(container, (list, tuple, str)):
                raise DatarTypeError(
                    "Cannot index into non-sequence",
                    lineno=expr.lineno if hasattr(expr, "lineno") else None,
                )
            idx = self._eval(expr.index, env)
            if not isinstance(idx, int):
                raise DatarTypeError(
                    "Index must be an integer",
                    lineno=expr.lineno if hasattr(expr, "lineno") else None,
                )
            # DatarScript traditionally 1-based for human readability? We'll use 0-based internally but ItemAt parsing may offset.
            # The parser for "item at N in LIST" already adjusted N-1.
            return container[idx]
        if isinstance(expr, ListExpr):
            return [self._eval(e, env) for e in expr.elements]
        if isinstance(expr, TupleExpr):
            return tuple(self._eval(e, env) for e in expr.elements)
        if isinstance(expr, DictExpr):
            d = {}
            for k, v in zip(expr.keys, expr.values):
                d[k] = self._eval(v, env)
            return d
        if isinstance(expr, Unary):
            val = self._eval(expr.expr, env)
            if expr.op == "not":
                return not self._truthy(val)
            else:
                raise DatarRuntimeError(f"Unknown unary operator: {expr.op}")
        raise DatarRuntimeError(
            f"Cannot evaluate expression of type {type(expr).__name__}"
        )

    def _eval_boolean(self, expr: Expr, env: Environment) -> bool:
        val = self._eval(expr, env)
        return self._truthy(val)

    def _truthy(self, val: Any) -> bool:
        if val is None or val is False:
            return False
        if isinstance(val, (int, float)) and val == 0:
            return False
        if isinstance(val, str) and val == "":
            return False
        if isinstance(val, (list, dict)) and len(val) == 0:
            return False
        return True

    def _apply_binary(self, op: str, left: Any, right: Any, lineno: int | None) -> Any:
        # Arithmetic
        if op == "plus":
            if isinstance(left, tuple) or isinstance(right, tuple):
                if not (isinstance(left, tuple) and isinstance(right, tuple)):
                    raise DatarTypeError(
                        "Cannot concatenate tuple with non-tuple", lineno=lineno
                    )
                return left + right
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == "minus":
            return left - right
        if op == "times":
            return left * right
        if op == "divided by":
            if right == 0:
                raise DatarError("Division by zero", lineno=lineno)
            return left / right
        if op == "modulo":
            return left % right
        if op == "raised to":
            return left**right
        # Logical
        if op == "and":
            return self._truthy(left) and self._truthy(right)
        if op == "or":
            return self._truthy(left) or self._truthy(right)
        # Pipe: left |> right  =>  right(left)
        if op == "pipegt":
            if not callable(right):
                raise DatarError("Right side of pipe must be a function", lineno=lineno)
            return right(left)
        raise DatarRuntimeError(f"Unknown binary operator: {op}")

    def _apply_compare(
        self, op: str, left: Any, right: Any, lineno: int | None
    ) -> bool:
        ops = {
            "is equal to": lambda a, b: a == b,
            "is not equal to": lambda a, b: a != b,
            "is different from": lambda a, b: a != b,
            "is greater than": lambda a, b: a > b,
            "is less than": lambda a, b: a < b,
            "is greater than or equal to": lambda a, b: a >= b,
            "is less than or equal to": lambda a, b: a <= b,
            "is at least": lambda a, b: a >= b,
            "is at most": lambda a, b: a <= b,
            "equals": lambda a, b: a == b,
            "is not": lambda a, b: a != b,
        }
        if op in ops:
            return ops[op](left, right)
        raise DatarRuntimeError(f"Unknown comparison: {op}")

    def _call(self, func: Any, args: list[Any], lineno: int | None) -> Any:
        # Builtin: callable (Builtin instance)
        if callable(func) and not isinstance(func, dict):
            try:
                return func(*args)
            except TypeError as e:
                raise DatarTypeError(
                    f"Builtin argument error: {e}", lineno=lineno
                ) from e
            except DatarError:
                raise
            except Exception as e:
                raise DatarRuntimeError(f"Builtin error: {e}", lineno=lineno) from e

        # User-defined function (stored as dict)
        if isinstance(func, dict) and func.get("type") == "function":
            fn = func
            params = fn["params"]
            closure = fn["closure_env"]
            body = fn["body"]
            defaults = fn.get("defaults", {})
            call_env = Environment(parent=closure)
            for i, p in enumerate(params):
                if i < len(args):
                    call_env.set(p, args[i])
                elif p in defaults:
                    default_val = self._eval(defaults[p], closure)
                    call_env.set(p, default_val)
                else:
                    call_env.set(p, None)
            try:
                self._exec(body, call_env)
                return None
            except ReturnSignal as r:
                return r.val

        raise DatarNameError(f"Undefined function: {getattr(func, 'name', str(func))}")
