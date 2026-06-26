"""
core.py — jedyne miejsce gdzie sympify() jest wywoływane.
Parsuje wyrażenie raz i zwraca ParsedExpr przekazywany do wszystkich filtrów.
"""

from sympy import sympify, symbols, zoo, oo, nan
from dataclasses import dataclass
from typing import Any
import re

# globalny symbol
x = symbols('x')


@dataclass
class ParsedExpr:
    raw: str
    sym: Any = None
    sym_raw: Any = None
    x: Any = None

    # cechy strukturalne
    is_zoo: bool = False
    is_const: bool = False
    has_division: bool = False
    cycles: int = 0
    fractions: int = 0
    powers: int = 0

    # cechy harmoniczne
    has_trig: bool = False
    trig_count: int = 0
    has_pi: bool = False

    # błąd parsowania
    error: str = ""

    def __post_init__(self):
        self.x = x

    @property
    def ok(self) -> bool:
        return not self.error and self.sym is not None


def parse(expr: str) -> "ParsedExpr":
    """Parsuje wyrażenie RAZ. Wynik przekazywany do wszystkich filtrów."""
    expr = expr.strip()

    try:
        # surowa forma (bez evaluate)
        sym_raw = sympify(expr, evaluate=False)

        # pełna forma (z evaluate)
        sym = sympify(expr)

        # trig detection (szybkie, syntaktyczne)
        trig_fns = sum(1 for fn in ("sin", "cos", "tan") if fn in expr)

        # stała liczba (ale nie zoo/oo/nan)
        is_const = bool(sym.is_number and sym not in (oo, -oo, zoo, nan))

        return ParsedExpr(
            raw          = expr,
            sym          = sym,
            sym_raw      = sym_raw,

            is_zoo       = (sym == zoo),
            is_const     = is_const,
            has_division = ("/" in expr or "**-1" in expr),

            cycles       = expr.count("(") + expr.count(")"),
            fractions    = expr.count("/"),
            powers       = len(re.findall(r"\*\*", expr)),

            has_trig     = trig_fns > 0,
            trig_count   = trig_fns,
            has_pi       = ("pi" in expr),
        )

    except Exception as e:
        return ParsedExpr(raw=expr, error=str(e))
