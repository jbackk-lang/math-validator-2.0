"""
algebra_filter.py — wykrywa błędy algebraiczne: dzielenie przez zero,
wyrażenia nieokreślone, zespolone pierwiastki.
"""
from core import ParsedExpr
from sympy import zoo, oo, nan, I, im, Symbol


def run(p: ParsedExpr) -> dict:
    if p.error:
        return {"status": "error", "message": p.error}

    notes = []

    # Dzielenie przez zero — SymPy uprościł do zoo
    if p.is_zoo:
        return {
            "status": "error",
            "message": "dzielenie przez zero (zoo)",
            "notes": ["wyrażenie stale nieokreślone — mianownik zawsze 0"]
        }

    # Wyrażenie zawiera zoo jako podelement
    if p.sym is not None and p.sym.has(zoo):
        return {
            "status": "error",
            "message": "wyrażenie zawiera dzielenie przez zero",
            "notes": ["zoo wykryte jako podelement wyrażenia"]
        }

    # Wartość urojona (np. sqrt(-1))
    if p.sym is not None and p.sym.is_number:
        try:
            if im(p.sym) != 0:
                notes.append(f"wyrażenie ma część urojoną: {p.sym}")
                return {"status": "warning", "message": "wartość zespolona", "notes": notes}
        except Exception:
            pass

    return {"status": "ok", "message": "brak błędów algebraicznych", "notes": notes}
