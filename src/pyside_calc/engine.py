"""Safe expression evaluator for calculator input."""

from __future__ import annotations

import ast
import operator
import re
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 50

_ALLOWED_RE = re.compile(r"^[0-9+\-*/().^%\s]+$")
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def normalize_expr(expr: str) -> str:
    s = expr.strip().replace(" ", "")
    # caret power → Python **
    s = s.replace("^", "**")
    return s


def _eval_node(node: ast.AST) -> Decimal:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Decimal(str(node.value))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = _OPS[type(node.op)]
        if isinstance(node.op, ast.Pow):
            # Decimal ** float can be awkward; use float for exponent when needed
            if right == right.to_integral_value() and abs(int(right)) < 10_000:
                return left ** int(right)
            return Decimal(str(float(left) ** float(right)))
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("division by zero")
        return Decimal(str(op(left, right)))
    raise ValueError("unsupported expression")


def format_result(value: Decimal) -> str:
    try:
        normalized = value.normalize()
    except InvalidOperation:
        normalized = value
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def try_evaluate(expr: str) -> str | None:
    """Return formatted result, or None if input is incomplete/invalid."""
    raw = expr.strip()
    if not raw:
        return None
    if not _ALLOWED_RE.match(raw):
        return None
    # Plain number alone: no result row (match Rofi calc behavior)
    if re.fullmatch(r"[0-9]+(\.[0-9]+)?", raw.replace(" ", "")):
        return None
    # Need an operator (or unary minus pattern like 1-2)
    compact = raw.replace(" ", "")
    if not re.search(r"[+*/^%()]", compact):
        if not re.search(r"[0-9]-[0-9]", compact):
            return None

    normalized = normalize_expr(raw)
    try:
        tree = ast.parse(normalized, mode="eval")
        for n in ast.walk(tree):
            if isinstance(n, ast.Call | ast.Name | ast.Attribute | ast.Subscript):
                return None
        result = _eval_node(tree)
        return format_result(result)
    except (SyntaxError, ValueError, ZeroDivisionError, InvalidOperation, OverflowError, ArithmeticError):
        return None
