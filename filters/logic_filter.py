"""
logic_filter.py — wykrywa tautologie, sprzeczności i ukryte osobliwości
w wyrażeniach uproszczonych do stałej.
"""
from core import ParsedExpr


def run(p: ParsedExpr) -> dict:
    if p.error:
        return {"status": "error", "message": p.error}

    notes = []

    # Tautologia: wyrażenie zawsze prawdziwe
    if p.sym is True:
        return {
            "status": "ok",
            "verdict": "tautology",
            "notes": ["wyrażenie jest zawsze prawdziwe"]
        }

    # Sprzeczność: wyrażenie zawsze fałszywe
    if p.sym is False:
        return {
            "status": "ok",
            "verdict": "contradiction",
            "notes": ["wyrażenie jest zawsze fałszywe — sprzeczność logiczna"]
        }

    # Uproszczone do stałej nietrywialnej (np. (x+1)/(x+1) → 1)
    # ale zawiera dzielenie — możliwa ukryta osobliwość
    if p.is_const and p.has_division:
        notes.append(
            "wyrażenie uproszczone do stałej, ale zawiera dzielenie "
            "— możliwa ukryta osobliwość w mianowniku (np. x=-1 dla (x+1)/(x+1))"
        )
        return {
            "status": "warning",
            "verdict": "simplified_with_hidden_singularity",
            "notes": notes
        }

    return {"status": "ok", "verdict": "ok", "notes": notes}
