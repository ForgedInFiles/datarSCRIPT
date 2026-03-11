"""Parser for DatarScript: converts tokens into an AST."""

from __future__ import annotations

from typing import Optional

import re
from .lexer import Token, TokenType
from .errors import DatarSyntaxError
from .ast import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None

    # ── Utility ───────────────────────────────────────────────────────────

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = Token(
                TokenType.EOF, "", self.tokens[-1].lineno if self.tokens else 0
            )

    # Use string token types for compatibility
    # TokenType constants are now strings like "IDENT", "EOF", etc.
    def match(self, *types: str) -> bool:
        if self.current is None:
            return False
        token_type = self.current.type
        for t in types:
            if token_type == t:
                return True
        return False

    def expect(self, *types: str) -> Token:
        if self.current is None:
            raise DatarSyntaxError("Unexpected end of file", lineno=0)
        if not self.match(*types):
            expected = ", ".join(str(t) for t in types)
            raise DatarSyntaxError(
                f"Expected {expected}, got {self.current.type}",
                lineno=self.current.lineno,
            )
        tok = self.current
        self.advance()
        return tok

    def peek(self) -> Optional[Token]:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    # ── Parsing entry ─────────────────────────────────────────────────────

    def parse_program(self) -> Program:
        stmts = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                stmts.append(stmt)
        return Program(body=stmts)

    def parse_statement(self) -> Optional[Stmt]:
        if self.match(TokenType.EOF):
            return None

        tok = self.current
        if tok is None:
            return None
        val = tok.value.lower() if hasattr(tok, "value") else ""

        # Statement type dispatcher based on first few tokens (natural language)
        # We'll look at sequences of IDENT tokens and punctuation to identify constructs.
        # Since we allow multi-word keywords (e.g., "end if", "for each"),
        # we'll use a lookahead approach.

        # Save position for rollback if needed
        start_pos = self.pos

        # Try compound statements (if, while, for, function, try)
        try:
            if val in (
                "if",
                "show",
                "set",
                "create",
                "make",
                "define",
                "ask",
                "call",
                "while",
                "for",
                "create",
                "return",
                "try",
                "break",
                "continue",
            ):
                return self._parse_compound_or_simple()
            else:
                # Might be expression statement or assignment?
                # Look for pattern: SET VAR TO expr, or ASK FOR ... STORE IN, or SHOW expr,
                # or ADD expr TO var, etc.
                return self._parse_simple_statement()
        except DatarSyntaxError:
            # Reset and re-raise after cleaning up? For now, just reset to start and raise
            self.pos = start_pos
            self.current = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
            raise

    def _parse_compound_or_simple(self) -> Stmt:
        """Parse either a compound statement (with block) or a simple statement."""
        # Peek to decide
        if self.match(TokenType.IDENT):
            val = self.current.value.lower()
            if val == "if":
                return self.parse_if()
            elif val == "while":
                return self.parse_while()
            elif val == "for":
                return self.parse_for()
            elif val == "create":
                # Could be "create function" or "create a function" or "create name as"
                # Look ahead: if next few tokens include "function"
                saved = self.pos
                self.advance()  # consume 'create'
                # Skip optional "a"
                if self.match(TokenType.IDENT) and self.current.value.lower() == "a":
                    self.advance()
                if (
                    self.match(TokenType.IDENT)
                    and self.current.value.lower() == "function"
                ):
                    self.pos = saved
                    return self.parse_function_def()
                else:
                    self.pos = saved
                    return self._parse_simple_statement()
            elif val == "try":
                return self.parse_try()
            elif val in ("set", "make", "define"):
                return self._parse_simple_statement()
            elif val == "show":
                return self._parse_simple_statement()
            elif val == "ask":
                return self._parse_simple_statement()
            elif val == "add":
                return self._parse_simple_statement()
            elif val == "call":
                return self._parse_simple_statement()
            elif val == "return":
                return self.parse_return()
            elif val == "break":
                self.advance()
                self._consume_dot()
                return Break()
            elif val == "continue":
                self.advance()
                self._consume_dot()
                return Continue()
            elif val == "end":
                # Should be handled by parse_block, not here
                raise DatarSyntaxError(
                    "Unexpected 'end' without matching block",
                    lineno=self.current.lineno,
                )
            else:
                return self._parse_simple_statement()
        else:
            # Not an IDENT; could be unknown
            raise DatarSyntaxError(
                f"Unexpected token: {self.current.value}", lineno=self.current.lineno
            )

    def _parse_simple_statement(self) -> Stmt:
        # Simple statements are: assignments, expressions (show, call, post, fetch, etc.),
        # add to list, subtract from, multiply, divide, read/write file, etc.
        # We'll handle high-level patterns and convert to Expr nodes.

        # We need to parse natural language patterns using token sequence.
        # For now, we'll use a hybrid approach: reconstruct a natural string from tokens
        # until a DOT, then parse that string using the legacy parsing approach.
        # This keeps compatibility while using the new lexer/parser infrastructure.

        start_lineno = self.current.lineno if self.current else 0
        tokens_buffer = []
        while not self.match(TokenType.DOT) and not self.match(TokenType.EOF):
            tokens_buffer.append(
                self.current.value if hasattr(self.current, "value") else ""
            )
            self.advance()
        if not self.match(TokenType.DOT):
            raise DatarSyntaxError("Missing terminating period", lineno=start_lineno)
        self.advance()  # consume DOT

        # Reconstruct natural language statement string
        stmt_str = " ".join(tokens_buffer).strip()

        # Delegate to legacy statement parser (will move later)
        # We'll create a temporary parser for the statement only
        # Instead, we'll call a parsing function that replicates the old logic just for stmt_str
        # But we want AST nodes. We'll directly call a helper that builds AST from the string.
        return self._parse_simple_statement_from_string(stmt_str, start_lineno)

    def _parse_simple_statement_from_string(self, stmt: str, lineno: int) -> Stmt:
        # This uses the old regex parsing logic to construct AST nodes from a single line.
        # We'll convert each statement type into appropriate AST classes.
        s = stmt.strip()

        # ═══════════════════════════════════════════════════════════════════════════════
        # TUPLE PATTERNS - Must be checked FIRST before general patterns
        # ═══════════════════════════════════════════════════════════════════════════════

        # Pattern: Set <var> to a tuple of <items>
        m = re.match(r"^set\s+(\w+)\s+to\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Create <var> as a tuple of <items>
        m = re.match(r"^create\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Make <var> equal to a tuple of <items>
        m = re.match(r"^make\s+(\w+)\s+equal\s+to\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Define <var> as a tuple of <items>
        m = re.match(r"^define\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # ═══════════════════════════════════════════════════════════════════════════════
        # NATURAL LANGUAGE RANDOM SYNTAX PATTERNS
        # ═══════════════════════════════════════════════════════════════════════════════

        # Pattern: Set <var> to generate a random number between <min> and <max>
        m = re.match(
            r"^set\s+(\w+)\s+to\s+generate\s+a\s+random\s+number\s+between\s+(.+)\s+and\s+(.+)$",
            s,
            re.I,
        )
        if m:
            var = m.group(1).lower()
            min_str = m.group(2).strip()
            max_str = m.group(3).strip()
            min_expr = self._parse_expression(min_str)
            max_expr = self._parse_expression(max_str)
            return Assign(
                target=var,
                value=Call(func=Variable(name="randint"), args=[min_expr, max_expr]),
            )

        # Pattern: Set <var> to roll a random number from <min> to <max>
        m = re.match(
            r"^set\s+(\w+)\s+to\s+roll\s+a\s+random\s+number\s+from\s+(.+)\s+to\s+(.+)$",
            s,
            re.I,
        )
        if m:
            var = m.group(1).lower()
            min_str = m.group(2).strip()
            max_str = m.group(3).strip()
            min_expr = self._parse_expression(min_str)
            max_expr = self._parse_expression(max_str)
            return Assign(
                target=var,
                value=Call(func=Variable(name="randint"), args=[min_expr, max_expr]),
            )

        # Pattern: Set <var> to generate a random value between <min> and <max>
        m = re.match(
            r"^set\s+(\w+)\s+to\s+generate\s+a\s+random\s+value\s+between\s+(.+)\s+and\s+(.+)$",
            s,
            re.I,
        )
        if m:
            var = m.group(1).lower()
            min_str = m.group(2).strip()
            max_str = m.group(3).strip()
            min_expr = self._parse_expression(min_str)
            max_expr = self._parse_expression(max_str)
            return Assign(
                target=var,
                value=Call(func=Variable(name="randint"), args=[min_expr, max_expr]),
            )

        # Pattern: Set <var> to pick a random integer between <min> and <max>
        m = re.match(
            r"^set\s+(\w+)\s+to\s+pick\s+a\s+random\s+integer\s+between\s+(.+)\s+and\s+(.+)$",
            s,
            re.I,
        )
        if m:
            var = m.group(1).lower()
            min_str = m.group(2).strip()
            max_str = m.group(3).strip()
            min_expr = self._parse_expression(min_str)
            max_expr = self._parse_expression(max_str)
            return Assign(
                target=var,
                value=Call(func=Variable(name="randint"), args=[min_expr, max_expr]),
            )

        # ═══════════════════════════════════════════════════════════════════════════════
        # GENERAL PATTERNS (checked after natural language patterns to avoid conflicts)
        # ═══════════════════════════════════════════════════════════════════════════════

        # Pattern: Set <var> to <expr>
        m = re.match(r"^set\s+(\w+)\s+to\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            # Check if it's a trim expression
            trim_m = re.match(r"^trim\s+whitespace\s+from\s+(\w+)$", expr_str, re.I)
            if trim_m:
                trim_var = trim_m.group(1).lower()
                return Assign(
                    target=var,
                    value=Call(
                        func=Variable(name="trim"), args=[Variable(name=trim_var)]
                    ),
                )
            # NOT a tuple, parse as normal expression
            return Assign(target=var, value=self._parse_expression(expr_str))

        # First check for tuple patterns BEFORE general set pattern!
        # Pattern: Create <var> as a tuple of <items>
        m = re.match(r"^create\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # IF not tuple, then regular set <var> to <expr> processing (trim check above already passed)
        # ... continue with normal expression parsing

        # Note: Other tuple patterns moved to after their general counterparts
        # ... (rest of the Pattern: Set <var> to <expr> block remains but after tuple checks)

        # Pattern: Create <var> as a tuple of <items>
        m = re.match(r"^create\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Create <var> as <expr>
        m = re.match(r"^create\s+(\w+)\s+as\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            return Assign(target=var, value=self._parse_expression(expr_str))

        # Pattern: Make <var> equal to <expr>
        m = re.match(r"^make\s+(\w+)\s+equal\s+to\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            return Assign(target=var, value=self._parse_expression(expr_str))

        # Pattern: Define <var> as <expr>
        m = re.match(r"^define\s+(\w+)\s+as\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            return Assign(target=var, value=self._parse_expression(expr_str))

        # Pattern: Create <var> as a tuple of <items>
        m = re.match(r"^create\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Make <var> equal to a tuple of <items>
        m = re.match(r"^make\s+(\w+)\s+equal\s+to\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Define <var> as a tuple of <items>
        m = re.match(r"^define\s+(\w+)\s+as\s+a\s+tuple\s+of\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            items_str = m.group(2)
            items = self._parse_expression_list(items_str)
            return Assign(target=var, value=TupleExpr(elements=items))

        # Pattern: Show <expr>
        m = re.match(r"^show\s+(.+)$", s, re.I)
        if m:
            expr_str = m.group(1)
            # Show is like a print statement; we'll model as Call(builtin "print", [expr])
            return ExprStmt(
                expr=Call(
                    func=Variable(name="print"), args=[self._parse_expression(expr_str)]
                )
            )

        # Pattern: Ask for <prompt> and store in <var>
        m = re.match(r"^ask\s+for\s+\"([^\"]+)\"\s+and\s+store\s+in\s+(\w+)$", s, re.I)
        if m:
            prompt = m.group(1)
            var = m.group(2).lower()
            # Model as assignment: var = input(prompt)
            return Assign(
                target=var,
                value=Call(func=Variable(name="input"), args=[Literal(prompt)]),
            )

        # Pattern: Add <expr> to <var>
        m = re.match(r"^add\s+(.+?)\s+to\s+(\w+)$", s, re.I)
        if m:
            expr_str = m.group(1)
            var = m.group(2).lower()
            # In AST: equivalent to var = var + expr (but need special handling for list append)
            # We'll create a special node: AddTo(var, expr) – but for now use Assign with Binary
            # We'll handle list append at evaluation; detect type?
            # For AST: just a Binary plus assignment: var = var plus expr
            return Assign(
                target=var,
                value=Binary(
                    left=Variable(name=var),
                    op="plus",
                    right=self._parse_expression(expr_str),
                ),
            )

        # Pattern: Subtract <expr> from <var>
        m = re.match(r"^subtract\s+(.+?)\s+from\s+(\w+)$", s, re.I)
        if m:
            expr_str = m.group(1)
            var = m.group(2).lower()
            return Assign(
                target=var,
                value=Binary(
                    left=Variable(name=var),
                    op="minus",
                    right=self._parse_expression(expr_str),
                ),
            )

        # Pattern: Multiply <var> by <expr>
        m = re.match(r"^multiply\s+(\w+)\s+by\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            return Assign(
                target=var,
                value=Binary(
                    left=Variable(name=var),
                    op="times",
                    right=self._parse_expression(expr_str),
                ),
            )

        # Pattern: Divide <var> by <expr>
        m = re.match(r"^divide\s+(\w+)\s+by\s+(.+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            expr_str = m.group(2)
            return Assign(
                target=var,
                value=Binary(
                    left=Variable(name=var),
                    op="divided by",
                    right=self._parse_expression(expr_str),
                ),
            )

        # Pattern: Increment <var>
        m = re.match(r"^increment\s+(\w+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            return Assign(
                target=var,
                value=Binary(left=Variable(name=var), op="plus", right=Literal(1)),
            )

        # Pattern: Decrement <var>
        m = re.match(r"^decrement\s+(\w+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            return Assign(
                target=var,
                value=Binary(left=Variable(name=var), op="minus", right=Literal(1)),
            )

        # Pattern: Remove last item from <var>
        m = re.match(r"^remove\s+the\s+last\s+item\s+from\s+(\w+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            # In Python: var = var[:-1]
            return ExprStmt(
                expr=Call(
                    func=Variable(name="builtin_remove_last"), args=[Variable(name=var)]
                )
            )

        # Pattern: Remove <expr> from <var>
        m = re.match(r"^remove\s+(.+?)\s+from\s+(\w+)$", s, re.I)
        if m:
            expr_str = m.group(1)
            var = m.group(2).lower()
            return ExprStmt(
                expr=Call(
                    func=Variable(name="builtin_remove_value"),
                    args=[Variable(name=var), self._parse_expression(expr_str)],
                )
            )

        # Pattern: Trim whitespace from <var>
        m = re.match(r"^trim\s+whitespace\s+from\s+(\w+)$", s, re.I)
        if m:
            var = m.group(1).lower()
            return Call(func=Variable(name="trim"), args=[Variable(name=var)])

        # Pattern: Raise <error type> error with message <msg>
        m = re.match(
            r"^raise\s+(.+?)\s+error\s+with\s+message\s+\"([^\"]+)\"$", s, re.I
        )
        if m:
            error_type = m.group(1).strip()
            message = m.group(2)
            return ExprStmt(
                expr=Call(
                    func=Variable(name="builtin_raise"),
                    args=[Literal(error_type), Literal(message)],
                )
            )

        # Pattern: <var> equals? -> expression statement (function call)
        # Fallback: treat as expression statement
        return ExprStmt(expr=self._parse_expression(s))

    def _parse_expression(self, expr_str: str) -> Expr:
        """Parse an expression string into an AST Expr."""
        s = expr_str.strip()

        # Parenthesized expression
        if s.startswith("(") and s.endswith(")"):
            return self._parse_expression(s[1:-1])

        # Boolean / null literals
        ls = s.lower()
        if ls == "true":
            return Literal(True)
        if ls == "false":
            return Literal(False)
        if ls in ("null", "none", "nothing"):
            return Literal(None)
        if ls == "empty":
            # empty means empty string or empty list depending on context? We'll treat as empty string for now.
            return Literal("")

        # Number literal (could be int or float)
        try:
            if "." in s:
                return Literal(float(s))
            else:
                return Literal(int(s))
        except ValueError:
            pass

        # String literal - only if it's a single quoted string (not dict/list with quotes)
        if s.startswith('"') and s.endswith('"'):
            quote_count = s.count('"')
            if quote_count == 2:
                return Literal(s[1:-1])

        # Call function: call <func> with <args> OR just call <func>
        m = re.match(r"^call\s+(\w+)\s+with\s+(.+)$", s, re.I)
        if m:
            func_name = m.group(1).lower()
            args_str = m.group(2)
            args = self._parse_call_args(args_str)
            return Call(func=Variable(name=func_name), args=args)
        m = re.match(r"^call\s+(\w+)$", s, re.I)
        if m:
            func_name = m.group(1).lower()
            return Call(func=Variable(name=func_name), args=[])

        # List/Dict literal - only for explicit list syntax
        # DatarScript uses "a", "b", "c" syntax for lists
        # Only trigger if it looks like a real list/dict literal
        if "," in s and not s.startswith('"'):
            # Check if this looks like a simple list (no operators like 'and', 'plus', etc.)
            # Simple heuristic: if it contains common operators, it's not a list
            has_operator = any(
                op in s.lower()
                for op in [
                    " and ",
                    " or ",
                    " plus ",
                    " minus ",
                    " times ",
                    " divided ",
                    " is ",
                    " equals ",
                    "+",
                    "-",
                    "*",
                    "/",
                ]
            )
            # Also check if it looks like a dict (has "key": pattern with quoted keys)
            is_dict_like = False
            if ":" in s:
                # Check if it has quoted key pattern
                is_dict_like = '"' in s.split(":")[0]

            if not has_operator:
                # Might be a list or a dict; check for colons too
                if ":" in s:
                    # Dict: key: val, key: val - but respect strings
                    # Use safe split
                    parts = self._safe_split_on(s, ",")
                    parts = [p for p in parts if p.strip() and p.strip() != ","]
                    keys = []
                    values = []
                    for part in parts:
                        if ":" not in part:
                            raise DatarSyntaxError(
                                f"Invalid dict entry: {part}", lineno=0
                            )
                        k, v = part.split(":", 1)
                        key_str = k.strip()
                        # Strip quotes from string keys
                        if key_str.startswith('"') and key_str.endswith('"'):
                            key_str = key_str[1:-1]
                        keys.append(key_str.lower())
                        values.append(self._parse_expression(v.strip()))
                    return DictExpr(keys=keys, values=values)
                else:
                    # List
                    parts = self._safe_split_on(s, ",")
                    parts = [p for p in parts if p.strip() and p.strip() != ","]
                    elems = [
                        self._parse_expression(p.strip()) for p in parts if p.strip()
                    ]
                    return ListExpr(elements=elems)

        # Variables (must not have spaces)
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", s):
            return Variable(name=s.lower())

        # Binary operations with natural operators
        # We'll use safe splitting; note this could be nested, so we need precedence.
        # Use simple precedence: plus/minus lowest, then times/divided by/modulo, then power, then comparisons.
        # We'll first try comparisons, then arithmetic.
        # We'll reuse the old safe_split_on logic but need to be careful.

        # For now, use a simple operator list with precedence.
        # We'll call _parse_binary_expr(s) which handles precedence parsing.

        return self._parse_binary_expr(s)

    def _parse_binary_expr(self, s: str) -> Expr:
        # Precedence climbing or Pratt parsing. Simpler: split on lowest-precedence operators first.
        # Operators by precedence (low to high):
        # or, and, comparisons (== != > >= < <=), plus/minus, times/divided by/modulo, power/unary

        # Or
        parts = self._safe_split_on(s, "or")
        if len(parts) > 1:
            # Build left-associative chain: OR(OR(a,b),c) or flatten? We'll do flat list then fold left
            exprs = [
                self._parse_binary_expr(p) for p in parts if p.strip().lower() != "or"
            ]
            expr = exprs[0]
            for e in exprs[1:]:
                expr = Binary(left=expr, op="or", right=e)
            return expr

        # And
        parts = self._safe_split_on(s, "and")
        if len(parts) > 1:
            exprs = [
                self._parse_binary_expr(p) for p in parts if p.strip().lower() != "and"
            ]
            expr = exprs[0]
            for e in exprs[1:]:
                expr = Binary(left=expr, op="and", right=e)
            return expr

        # Comparisons
        comparison_ops = [
            "is not equal to",
            "is equal to",
            "is different from",
            "is greater than or equal to",
            "is at least",
            "is greater than",
            "is less than or equal to",
            "is at most",
            "is less than",
            "equals",
            "is not",
        ]
        for op in comparison_ops:
            parts = self._safe_split_on(s, op)
            if len(parts) > 1:
                # Filter out the operator itself from parts (re.split includes captured groups)
                filtered_parts = [p for p in parts if p.strip().lower() != op.lower()]
                if len(filtered_parts) != 2:
                    raise DatarSyntaxError(
                        f"Invalid comparison expression: {s}", lineno=0
                    )
                left = self._parse_arithmetic_expr(filtered_parts[0])
                right = self._parse_arithmetic_expr(filtered_parts[1])
                return Compare(left=left, op=op, right=right)

        # Equality as fallback?
        # Arithmetic
        return self._parse_arithmetic_expr(s)

    def _parse_arithmetic_expr(self, s: str) -> Expr:
        # Precedence: plus/minus (lowest), times/divided by/modulo, power (higher), unary minus/not
        # We'll use recursive descent: split on 'plus'/'minus', then each part evaluated for higher ops.
        # Also support '+' and '-' as operators

        # First handle '+' character operator
        # Split on '+' but only if it's not inside a quoted string
        if "+" in s:
            # Simple split on '+' respecting strings by tracking quote state
            parts = []
            current = []
            in_string = False
            for char in s:
                if char == '"':
                    in_string = not in_string
                    current.append(char)
                elif char == "+" and not in_string:
                    parts.append("".join(current).strip())
                    current = []
                else:
                    current.append(char)
            if current:
                parts.append("".join(current).strip())

            # Filter out empty parts
            parts = [p for p in parts if p]
            if len(parts) > 1:
                expr = self._parse_arithmetic_expr(parts[0])
                for part in parts[1:]:
                    rhs = self._parse_arithmetic_expr(part)
                    expr = Binary(left=expr, op="plus", right=rhs)
                return expr

        # Handle '-' character operator (but not negative numbers)
        # Only split if '-' is surrounded by spaces or at word boundary
        if " - " in s:
            # Simple split on ' - ' respecting strings
            parts = []
            current = []
            in_string = False
            i = 0
            chars = list(s)
            while i < len(chars):
                if chars[i] == '"':
                    in_string = not in_string
                    current.append(chars[i])
                    i += 1
                elif (
                    i < len(chars) - 2
                    and chars[i : i + 3] == [" ", "-", " "]
                    and not in_string
                ):
                    parts.append("".join(current).strip())
                    current = []
                    i += 3
                else:
                    current.append(chars[i])
                    i += 1
            if current:
                parts.append("".join(current).strip())

            parts = [p for p in parts if p]
            if len(parts) > 1:
                expr = self._parse_arithmetic_expr(parts[0])
                for part in parts[1:]:
                    rhs = self._parse_arithmetic_expr(part)
                    expr = Binary(left=expr, op="minus", right=rhs)
                return expr

        parts = self._safe_split_on(s, "plus", "minus")
        if len(parts) > 1:
            expr = self._parse_arithmetic_expr(parts[0])
            i = 1
            while i < len(parts):
                op = parts[i].lower()
                rhs = self._parse_arithmetic_expr(parts[i + 1])
                if op == "plus":
                    expr = Binary(left=expr, op="plus", right=rhs)
                elif op == "minus":
                    expr = Binary(left=expr, op="minus", right=rhs)
                i += 2
            return expr

        parts = self._safe_split_on(s, "times", "divided by", "modulo")
        if len(parts) > 1:
            expr = self._parse_arithmetic_expr(parts[0])
            i = 1
            while i < len(parts):
                op = parts[i].lower()
                rhs = self._parse_arithmetic_expr(parts[i + 1])
                if op == "times":
                    expr = Binary(left=expr, op="times", right=rhs)
                elif op == "divided by":
                    expr = Binary(left=expr, op="divided by", right=rhs)
                elif op == "modulo":
                    expr = Binary(left=expr, op="modulo", right=rhs)
                i += 2
            return expr

        # Power
        # Only check for "raised to" if not inside a string (simple check: if entire string is quoted, skip)
        if not (s.startswith('"') and s.endswith('"') and s.count('"') == 2):
            m = re.search(r"\braised\s+to\b", s, re.I)
            if m:
                # split only on first occurrence (right-associative-ish)
                base_str = s[: m.start()].strip()
                exp_str = s[m.end() :].strip()
                base = self._parse_arithmetic_expr(base_str)
                exp = self._parse_arithmetic_expr(exp_str)
                return Binary(left=base, op="raised to", right=exp)

        # Unary: not, and maybe negative numbers?
        # Not: "not X" or "not (X)"
        m = re.match(r"^not\s+(.+)$", s, re.I)
        if m:
            inner = m.group(1)
            # strip optional parens
            if inner.startswith("(") and inner.endswith(")"):
                inner = inner[1:-1]
            return Unary(op="not", expr=self._parse_arithmetic_expr(inner))

        # If nothing matches, maybe it's a simple atom (variable, number, string, list, dict, call)
        return self._parse_atom(s)

    def _parse_atom(self, s: str) -> Expr:
        s = s.strip()
        # Variable reference
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", s):
            return Variable(name=s.lower())

        # Number
        try:
            if "." in s:
                return Literal(float(s))
            else:
                return Literal(int(s))
        except ValueError:
            pass

        # String - only match if it's a single quoted string (not multiple strings with operators)
        if s.startswith('"') and s.endswith('"'):
            # Count quotes - should be exactly 2 (one pair)
            quote_count = s.count('"')
            if quote_count == 2:
                return Literal(s[1:-1])

        # Boolean / null
        ls = s.lower()
        if ls == "true":
            return Literal(True)
        if ls == "false":
            return Literal(False)
        if ls in ("null", "none", "nothing"):
            return Literal(None)

        # Call: call X with Y
        m = re.match(r"^call\s+(\w+)\s+with\s+(.+)$", s, re.I)
        if m:
            return Call(
                func=Variable(name=m.group(1).lower()),
                args=self._parse_call_args(m.group(2)),
            )
        m = re.match(r"^call\s+(\w+)$", s, re.I)
        if m:
            return Call(func=Variable(name=m.group(1).lower()), args=[])

        # List literal: a, b, c - only if comma is not inside a string
        if "," in s:
            # Check if this looks like a list literal (not a string with commas)
            # Simple heuristic: if the string starts with a quote, it's probably not a list
            if not s.startswith('"'):
                # Use safe split to respect strings
                parts = self._safe_split_on(s, ",")
                # Filter out the commas themselves
                parts = [p for p in parts if p.strip() and p.strip() != ","]
                if len(parts) > 1:
                    elems = [
                        self._parse_expression(p.strip()) for p in parts if p.strip()
                    ]
                    return ListExpr(elements=elems)

        # Dict literal: key: val, key: val
        if ":" in s:
            parts = re.split(r",\s*", s)
            keys = []
            values = []
            for part in parts:
                if ":" not in part:
                    raise DatarSyntaxError(f"Invalid dict entry: {part}", lineno=0)
                k, v = part.split(":", 1)
                key_str = k.strip()
                # Strip quotes from string keys
                if key_str.startswith('"') and key_str.endswith('"'):
                    key_str = key_str[1:-1]
                keys.append(key_str.lower())
                values.append(self._parse_expression(v.strip()))
            return DictExpr(keys=keys, values=values)

        # Parenthesized expression
        if s.startswith("(") and s.endswith(")"):
            return self._parse_expression(s[1:-1])

        # value of key in dict
        m = re.match(r"^value\s+of\s+(\w+)\s+in\s+(\w+)$", s, re.I)
        if m:
            key = m.group(1).lower()
            container = Variable(name=m.group(2).lower())
            return GetDictValue(key=Variable(name=key), container=container)

        # item at N in list
        m = re.match(r"^item\s+at\s+(\d+)\s+in\s+(\w+)$", s, re.I)
        if m:
            idx = int(m.group(1)) - 1  # DatarScript uses 1-based?
            # Actually original is 1-based indexing; we'll keep that
            container = Variable(name=m.group(2).lower())
            return ItemAt(index=Literal(idx), container=container)
        m = re.match(r"^item\s+at\s+(\w+)\s+in\s+(\w+)$", s, re.I)
        if m:
            idx_var = Variable(name=m.group(1).lower())
            container = Variable(name=m.group(2).lower())
            return ItemAt(index=idx_var, container=container)

        raise DatarSyntaxError(f"Cannot parse expression: '{s}'", lineno=0)

    def _parse_call_args(self, args_raw: str) -> list[Expr]:
        """Parse 'arg1, arg2, and arg3' or 'arg1 and arg2' into Expr list."""
        # Replace " and " with ", "
        clean = re.sub(r",?\s+and\s+", ", ", args_raw, flags=re.I)
        # Split on commas
        parts = [p.strip() for p in re.split(r",\s*", clean) if p.strip()]
        return [self._parse_expression(p) for p in parts]

    def _parse_expression_list(self, items_str: str) -> list[Expr]:
        """Parse comma-separated expression list (no 'and' conversion)."""
        parts = self._safe_split_on(items_str, ",")
        # Filter out empty/whitespace parts
        parts = [p.strip() for p in parts if p.strip() and p.strip() != ","]
        return [self._parse_expression(p) for p in parts]

    def _safe_split_on(self, text: str, *kw_list):
        """Split on any of the keywords, respecting quoted strings."""
        protected, strings = self._extract_strings(text)
        # Build regex patterns for each keyword, with special handling for comma
        pat_with_len = []
        for kw in kw_list:
            kw_clean = kw.strip()
            if kw_clean == ",":
                # Match comma with optional surrounding whitespace
                pat = r"\s*,\s*"
            else:
                pat = r"\b" + re.escape(kw_clean) + r"\b"
            pat_with_len.append((len(kw_clean), pat))
        # Sort by length descending to avoid partial matches of shorter keywords
        pat_with_len.sort(key=lambda x: x[0], reverse=True)
        sorted_patterns = [p[1] for p in pat_with_len]
        pattern = "|".join(sorted_patterns)
        parts = re.split(f"({pattern})", protected, flags=re.IGNORECASE)
        return [self._restore_strings(p.strip(), strings) for p in parts]

    def _extract_strings(self, text: str):
        parts = []
        result = []
        i = 0
        while i < len(text):
            if text[i] == '"':
                j = i + 1
                while j < len(text) and text[j] != '"':
                    if text[j] == "\\":
                        j += 2
                    else:
                        j += 1
                literal = text[i : j + 1]
                parts.append(literal)
                result.append(f"__S{len(parts) - 1}__")
                i = j + 1
            else:
                result.append(text[i])
                i += 1
        return "".join(result), parts

    def _restore_strings(self, text: str, parts: list[str]):
        for i, orig in enumerate(parts):
            text = text.replace(f"__S{i}__", orig)
        return text

    def _consume_dot(self) -> None:
        if self.match(TokenType.DOT):
            self.advance()
        else:
            raise DatarSyntaxError(
                "Missing terminating period", lineno=self.current.lineno
            )

    # ── Compound statements ───────────────────────────────────────────────

    def parse_if(self) -> If:
        # Format: If <condition> then: ... Else if ... Else ... End if.
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'if'
        # collect 'if' token and then next ident 'then'?
        # Actually tokens are just words. We'll read condition until we hit 'then' or ':'?
        # In DatarScript: "If condition then:" or "If condition:"
        # We'll gather tokens until we see a COLON or the word 'then'
        condition_tokens = []
        while (
            not self.match(TokenType.COLON)
            and not (
                self.match(TokenType.IDENT) and self.current.value.lower() == "then"
            )
            and not self.match(TokenType.COMMA)
        ):
            if self.match(TokenType.EOF):
                raise DatarSyntaxError("Unterminated if statement", lineno=lineno)
            condition_tokens.append(
                self.current.value if hasattr(self.current, "value") else ""
            )
            self.advance()
        # Check for then (may come after comma)
        if self.match(TokenType.IDENT) and self.current.value.lower() == "then":
            self.advance()
        # Consume optional comma (may come before or instead of then)
        if self.match(TokenType.COMMA):
            self.advance()
        # Check for then again (in case comma was first)
        if self.match(TokenType.IDENT) and self.current.value.lower() == "then":
            self.advance()
        self.expect(TokenType.COLON)
        condition_str = " ".join(condition_tokens).strip()
        condition = self._parse_expression(condition_str)
        then_body, else_branches, else_body = self._parse_block_body()
        return If(
            condition=condition,
            then_body=then_body,
            elif_branches=else_branches,
            else_body=else_body,
        )

    def _parse_block_body(
        self,
    ) -> tuple[list[Stmt], list[tuple[Expr, list[Stmt]]], list[Stmt] | None]:
        """Parse body of block, collecting elif and else."""
        body = []
        elif_branches = []
        else_body = None
        while not self.match(TokenType.EOF):
            # Check for block end keywords BEFORE calling parse_statement
            if self.match(TokenType.IDENT) and self.current.value.lower() == "end":
                # handle end of block - consume the 'end' keyword and any following keyword (like 'if')
                self.advance()  # consume 'end'
                # Consume optional block type word (e.g., 'if', 'while', 'for')
                if self.match(TokenType.IDENT):
                    self.advance()
                # Consume the DOT if present
                if self.match(TokenType.DOT):
                    self.advance()
                break
            # Check for else/else if - don't consume here, let the code after the loop handle it
            if self.match(TokenType.IDENT) and self.current.value.lower() == "else":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        # Check for else/elif
        if self.match(TokenType.IDENT) and self.current.value.lower() == "else":
            self.advance()  # consume 'else'
            if self.match(TokenType.IDENT) and self.current.value.lower() == "if":
                # else if
                self.advance()  # consume 'if'
                # parse condition similar to if
                condition_tokens = []
                while not self.match(TokenType.COLON):
                    if self.match(TokenType.EOF):
                        raise DatarSyntaxError(
                            "Unterminated else if", lineno=self.current.lineno
                        )
                    condition_tokens.append(
                        self.current.value if hasattr(self.current, "value") else ""
                    )
                    self.advance()
                self.expect(TokenType.COLON)
                condition_str = " ".join(condition_tokens).strip()
                condition = self._parse_expression(condition_str)
                # Recursively parse the rest to get elif_then_body, more elif branches, and else
                elif_then_body, more_elifs, else_body = self._parse_block_body()
                elif_branches.append((condition, elif_then_body))
                # Add any additional elif branches
                elif_branches.extend(more_elifs)
            else:
                # else: - consume the colon
                self.expect(TokenType.COLON)
                else_body, _, _ = self._parse_block_body()  # body until end
        return body, elif_branches, else_body

    def parse_while(self) -> While:
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'while'
        # condition until colon, but handle optional "do"
        condition_tokens = []
        while not self.match(TokenType.COLON) and not self.match(TokenType.COMMA):
            # Handle optional "do" keyword before colon
            if self.match(TokenType.IDENT) and self.current.value.lower() == "do":
                break
            if self.match(TokenType.EOF):
                raise DatarSyntaxError("Unterminated while", lineno=lineno)
            condition_tokens.append(
                self.current.value if hasattr(self.current, "value") else ""
            )
            self.advance()
        # Skip the "do" if present
        if self.match(TokenType.IDENT) and self.current.value.lower() == "do":
            self.advance()
        # Consume optional comma (may come before or after do)
        if self.match(TokenType.COMMA):
            self.advance()
        # Check for "do" again (in case comma was first)
        if self.match(TokenType.IDENT) and self.current.value.lower() == "do":
            self.advance()
        self.expect(TokenType.COLON)
        condition_str = " ".join(condition_tokens).strip()
        condition = self._parse_expression(condition_str)
        body = []
        while not self._is_block_end():
            body.append(self.parse_statement())
        # Expect 'end while'
        self._expect_end("while")
        return While(condition=condition, body=body)

    def _is_block_end(self) -> bool:
        if self.match(TokenType.IDENT) and self.current.value.lower() == "end":
            # peek ahead for block type?
            next_tok = self.peek()
            if next_tok and next_tok.type == TokenType.IDENT:
                return True
        return False

    def _expect_end(self, block_type: str):
        if not self.match(TokenType.IDENT) or self.current.value.lower() != "end":
            raise DatarSyntaxError(
                f"Expected 'end {block_type}'",
                lineno=self.current.lineno if self.current else 0,
            )
        self.advance()
        # Expect optional block type word
        if self.match(TokenType.IDENT) and self.current.value.lower() == block_type:
            self.advance()
        self._consume_dot()

    def parse_for(self) -> For:
        # Two forms: "For i from 1 to 10 do:" or "For each item in list do:"
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'for'
        if not self.match(TokenType.IDENT):
            raise DatarSyntaxError("Expected variable name after for", lineno=lineno)
        # Check 'each'? optional - "For each item in list" vs "For item from 1 to 10"
        if self.match(TokenType.IDENT) and self.current.value.lower() == "each":
            self.advance()  # consume 'each'
            # variable
            if not self.match(TokenType.IDENT):
                raise DatarSyntaxError("Expected variable after 'each'", lineno=lineno)
            target = self.current.value.lower()
            self.advance()
            # Expect 'in'
            if not self.match(TokenType.IDENT) or self.current.value.lower() != "in":
                raise DatarSyntaxError("Expected 'in'", lineno=lineno)
            self.advance()
            # iterable expression
            iterable_tokens = []
            while (
                not self.match(TokenType.COLON)
                and not (
                    self.match(TokenType.IDENT) and self.current.value.lower() == "do"
                )
                and not self.match(TokenType.COMMA)
            ):
                iterable_tokens.append(
                    self.current.value if hasattr(self.current, "value") else ""
                )
                self.advance()
            # Consume optional comma
            if self.match(TokenType.COMMA):
                self.advance()
            if self.match(TokenType.IDENT) and self.current.value.lower() == "do":
                self.advance()
            self.expect(TokenType.COLON)
            iterable_str = " ".join(iterable_tokens).strip()
            iterable = self._parse_expression(iterable_str)
        else:
            # Numeric for: "For i from 1 to 10 do:"
            target = self.current.value.lower()
            self.advance()
            self.expect(TokenType.IDENT)  # 'from'
            from_tokens = []
            while not self.match(TokenType.IDENT) or self.current.value.lower() != "to":
                from_tokens.append(
                    self.current.value if hasattr(self.current, "value") else ""
                )
                self.advance()
            self.expect(TokenType.IDENT)  # 'to'
            from_str = " ".join(from_tokens).strip()
            start = self._parse_expression(from_str)
            to_tokens = []
            while (
                not self.match(TokenType.COLON)
                and not (
                    self.match(TokenType.IDENT) and self.current.value.lower() == "do"
                )
                and not self.match(TokenType.COMMA)
            ):
                to_tokens.append(
                    self.current.value if hasattr(self.current, "value") else ""
                )
                self.advance()
            # Consume optional comma
            if self.match(TokenType.COMMA):
                self.advance()
            if self.match(TokenType.IDENT) and self.current.value.lower() == "do":
                self.advance()
            self.expect(TokenType.COLON)
            to_str = " ".join(to_tokens).strip()
            end = self._parse_expression(to_str)
            # Build iterable as range(start, end+1) inclusive
            # We'll represent as a Call to builtin_range(start, end)
            iterable = Call(func=Variable(name="range_inclusive"), args=[start, end])
        body = []
        while not self._is_block_end():
            body.append(self.parse_statement())
        self._expect_end("for")
        return For(target=target, iterable=iterable, body=body)

    def parse_function_def(self) -> FunctionDef:
        # "Create a function called <name> that takes <params>:" OR
        # "Create function <name> with parameters <params>:" etc.
        # We'll support "create function <name> that takes a, b:" style
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'create'
        # Skip optional "a"
        if self.match(TokenType.IDENT) and self.current.value.lower() == "a":
            self.advance()
        self.expect(TokenType.IDENT)  # 'function'
        # Skip optional "called"
        if self.match(TokenType.IDENT) and self.current.value.lower() == "called":
            self.advance()
        # function name
        if not self.match(TokenType.IDENT):
            raise DatarSyntaxError("Expected function name", lineno=lineno)
        name = self.current.value.lower()
        self.advance()
        # Params
        params = []
        defaults = {}
        # Look for "that takes" or "with parameters"
        if self.match(TokenType.IDENT) and self.current.value.lower() == "that":
            self.advance()
            # Expect 'takes'
            if not self.match(TokenType.IDENT) or self.current.value.lower() != "takes":
                raise DatarSyntaxError("Expected 'takes'", lineno=self.current.lineno)
            self.advance()
            # parse params: a, b, c with optionally = default
            while not self.match(TokenType.COLON):
                if self.match(TokenType.EOF):
                    raise DatarSyntaxError(
                        "Unterminated function definition", lineno=lineno
                    )
                if self.match(TokenType.IDENT):
                    param_name = self.current.value.lower()
                    self.advance()
                    # check for default '= expr'
                    if (
                        self.match(TokenType.IDENT)
                        and self.current.value.lower() == "="
                    ):
                        self.advance()
                        # parse default expression until comma or colon
                        default_tokens = []
                        while not self.match(TokenType.COMMA) and not self.match(
                            TokenType.COLON
                        ):
                            default_tokens.append(
                                self.current.value
                                if hasattr(self.current, "value")
                                else ""
                            )
                            self.advance()
                        default_str = " ".join(default_tokens).strip()
                        defaults[param_name] = self._parse_expression(default_str)
                    params.append(param_name)
                if self.match(TokenType.COMMA):
                    self.advance()
        self.expect(TokenType.COLON)
        body = []
        while not self._is_block_end():
            body.append(self.parse_statement())
        self._expect_end("function")
        return FunctionDef(name=name, params=params, defaults=defaults, body=body)

    def parse_return(self) -> Return:
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'return'
        value = None
        # If next token not DOT, parse expression
        if not self.match(TokenType.DOT):
            value_tokens = []
            while not self.match(TokenType.DOT) and not self.match(TokenType.EOF):
                value_tokens.append(
                    self.current.value if hasattr(self.current, "value") else ""
                )
                self.advance()
            value = self._parse_expression(" ".join(value_tokens))
        self._consume_dot()
        return Return(value=value)

    def parse_try(self) -> Try:
        lineno = self.current.lineno if self.current else 0
        self.expect(TokenType.IDENT)  # 'try'
        self.expect(TokenType.COLON)
        body = []
        while not self._is_block_end() and not (
            self.match(TokenType.IDENT)
            and self.current.value.lower() in ("catch", "finally")
        ):
            body.append(self.parse_statement())
        # catches
        catches = []
        if self.match(TokenType.IDENT) and self.current.value.lower() == "catch":
            while self.match(TokenType.IDENT) and self.current.value.lower() == "catch":
                self.advance()
                # Syntax options:
                # 1. "Catch <type> as <var>:" - catch specific error type
                # 2. "Catch <var>:" - catch any error, store message in var
                # 3. "Catch:" - catch any error without storing
                exc_type = None
                var = None

                # Collect tokens until ':'
                type_tokens = []
                while not self.match(TokenType.COLON):
                    if self.match(TokenType.EOF):
                        raise DatarSyntaxError(
                            "Unterminated catch clause", lineno=self.current.lineno
                        )
                    type_tokens.append(
                        self.current.value if hasattr(self.current, "value") else ""
                    )
                    self.advance()

                # Check if we have "type as var" pattern or just "var" pattern
                if type_tokens:
                    # Check for "as" keyword
                    as_idx = None
                    for i, tok in enumerate(type_tokens):
                        if tok.lower() == "as":
                            as_idx = i
                            break

                    if as_idx is not None:
                        # "type as var" pattern
                        exc_type = " ".join(type_tokens[:as_idx]).strip()
                        if as_idx + 1 < len(type_tokens):
                            var = type_tokens[as_idx + 1].lower()
                    else:
                        # Just "var" pattern - treat as variable name for error message
                        var = " ".join(type_tokens).strip().lower()

                self.expect(TokenType.COLON)
                catch_body = []
                while not self._is_block_end() and not (
                    self.match(TokenType.IDENT)
                    and self.current.value.lower() in ("catch", "finally", "end")
                ):
                    catch_body.append(self.parse_statement())
                catches.append(Catch(exception_type=exc_type, var=var, body=catch_body))
                # After catch, may have another catch or finally or end
                if (
                    self.match(TokenType.IDENT)
                    and self.current.value.lower() == "finally"
                ):
                    break
        finally_body = None
        if self.match(TokenType.IDENT) and self.current.value.lower() == "finally":
            self.advance()
            self.expect(TokenType.COLON)
            finally_body = []
            while not self._is_block_end():
                finally_body.append(self.parse_statement())
        self._expect_end("try")
        return Try(body=body, catches=catches, finally_body=finally_body)

    # ── Helpers ─────────────────────────────────────────────────────────────

    # (All the same _parse_* methods from earlier version: _safe_split_on, _extract_strings, _restore_strings, etc. remain)
