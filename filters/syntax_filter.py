"""
syntax_filter.py — sprawdza poprawność składni wyrażenia.
Wynik parse() dostarcza informację o błędzie jeśli sympify() rzucił wyjątek.
"""
from core import ParsedExpr


def run(p: ParsedExpr) -> dict:
    if p.error:
        return {
            "status": "error",
            "message": p.error,
            "notes": ["wyrażenie nie mogło być sparsowane przez SymPy"]
        }

    return {
        "status": "ok",
        "message": "składnia poprawna"
    }
