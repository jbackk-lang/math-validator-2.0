"""
millennium_filter.py — filtr wykrywający powiązania z Problemami Milenijnymi Clay Mathematics Institute.

Problemy Milenijne (7 problemów, nagroda $1 000 000 każdy):
  1. P vs NP
  2. Hipoteza Riemanna
  3. Hipoteza Bircha i Swinnertona-Dyera
  4. Yang–Mills i luka masowa
  5. Równania Naviera–Stokesa
  6. Hipoteza Poincarégo (ROZWIĄZANA przez Perelmana 2003)
  7. Hipoteza Hodge'a

Filtr działa na obiekcie ParsedExpr z core.py.
Wykrywa słowa kluczowe i struktury symboliczne wskazujące na dany problem,
nadaje poziom pewności (confidence) i zwraca ostrzeżenie.
"""

import re
from sympy import (
    Symbol, Function, oo, zoo, nan,
    zeta, I, pi, exp, sin, cos, log,
    symbols, Rational
)
from dataclasses import dataclass, field
from typing import List, Optional


# ─────────────────────────────────────────────
# Dane każdego Problemu Milenijnego
# ─────────────────────────────────────────────

MILLENNIUM_PROBLEMS = {
    "P_vs_NP": {
        "id": "MP-1",
        "name": "P vs NP",
        "status": "OPEN",
        "keywords": ["NP", "SAT", "polynomial", "complexity", "decidable", "NP-hard", "NP-complete"],
        "description": "Czy każdy problem, którego rozwiązanie można szybko zweryfikować, można też szybko rozwiązać?",
        "risk": "Wyrażenie sugeruje strukturę związaną z teorią złożoności obliczeniowej.",
    },
    "Riemann": {
        "id": "MP-2",
        "name": "Hipoteza Riemanna",
        "status": "OPEN",
        "keywords": ["zeta", "riemann", "zeros", "critical line", "Re(s)=1/2", "L-function", "ζ"],
        "description": "Wszystkie nietrywiane zera funkcji ζ(s) mają część rzeczywistą 1/2.",
        "risk": "Wyrażenie zawiera funkcję zeta lub strukturę związaną z zerami Riemanna.",
    },
    "Birch_Swinnerton_Dyer": {
        "id": "MP-3",
        "name": "Hipoteza Bircha i Swinnertona-Dyera",
        "status": "OPEN",
        "keywords": ["elliptic curve", "rank", "L(E,1)", "torsion", "Mordell", "BSD", "abelian variety"],
        "description": "Rząd grupy punktów wymiernych krzywej eliptycznej = rząd zera L(E,s) w s=1.",
        "risk": "Wyrażenie sugeruje strukturę krzywej eliptycznej lub funkcji L.",
    },
    "Yang_Mills": {
        "id": "MP-4",
        "name": "Yang–Mills i luka masowa",
        "status": "OPEN",
        "keywords": ["Yang-Mills", "gauge", "mass gap", "quantum field", "QFT", "SU(N)", "SU(2)", "SU(3)", "lagrangian"],
        "description": "Teoria Yang–Millsa istnieje i ma dodatnią lukę masową.",
        "risk": "Wyrażenie zawiera struktury teorii pola lub grupy cechowania.",
    },
    "Navier_Stokes": {
        "id": "MP-5",
        "name": "Równania Naviera–Stokesa",
        "status": "OPEN",
        "keywords": ["navier", "stokes", "fluid", "velocity", "pressure", "turbulence", "viscosity", "∇", "div", "curl"],
        "description": "Istnienie i gładkość rozwiązań równań Naviera–Stokesa w R³.",
        "risk": "Wyrażenie zawiera struktury charakterystyczne dla mechaniki płynów.",
    },
    "Poincare": {
        "id": "MP-6",
        "name": "Hipoteza Poincarégo",
        "status": "SOLVED",
        "solved_by": "Grigorij Perelman (2003)",
        "keywords": ["poincare", "3-sphere", "simply connected", "3-manifold", "Ricci flow"],
        "description": "Każda prosta spójnie 3-rozmaitość jest homeomorficzna z S³.",
        "risk": "UWAGA: Ten problem jest już ROZWIĄZANY (Perelman, 2003). Weryfikuj, czy twoje wyrażenie nie zakłada jego otwartości.",
    },
    "Hodge": {
        "id": "MP-7",
        "name": "Hipoteza Hodge'a",
        "status": "OPEN",
        "keywords": ["hodge", "algebraic cycle", "cohomology", "de Rham", "Dolbeault", "H^{p,p}", "Lefschetz"],
        "description": "Pewne klasy de Rhama na rozmaitości algebraicznej są kombinacjami liniowymi klas algebraicznych.",
        "risk": "Wyrażenie sugeruje strukturę kohomologiczną lub cykl algebraiczny.",
    },
}

# ─────────────────────────────────────────────
# Detekcja symboliczna (sympy)
# ─────────────────────────────────────────────

def _detect_symbolic(sym) -> List[str]:
    """Zwraca listę ID problemów wykrytych na podstawie struktury symbolicznej."""
    hits = []
    if sym is None:
        return hits

    sym_str = str(sym)

    # Riemann — obecność funkcji zeta
    if "zeta" in sym_str.lower():
        hits.append("Riemann")

    # Navier–Stokes — wyrażenia wektorowe / gradient
    if any(k in sym_str for k in ["nabla", "div", "curl", "laplacian"]):
        hits.append("Navier_Stokes")

    # Yang–Mills — grupy SU / lagrangiany pól
    if re.search(r"SU\s*\(\s*\d+\s*\)", sym_str):
        hits.append("Yang_Mills")

    return hits


def _detect_keywords(raw: str) -> List[str]:
    """Zwraca listę ID problemów wykrytych na podstawie słów kluczowych w surowym wyrażeniu."""
    raw_lower = raw.lower()
    hits = []
    for problem_id, info in MILLENNIUM_PROBLEMS.items():
        for kw in info["keywords"]:
            if kw.lower() in raw_lower:
                hits.append(problem_id)
                break
    return hits


# ─────────────────────────────────────────────
# Wynik filtra
# ─────────────────────────────────────────────

@dataclass
class MillenniumMatch:
    problem_id: str
    name: str
    status: str          # "OPEN" | "SOLVED"
    confidence: str      # "HIGH" | "MEDIUM" | "LOW"
    source: str          # "keyword" | "symbolic" | "both"
    risk_message: str
    description: str
    solved_by: Optional[str] = None


def _confidence(keyword_hit: bool, symbolic_hit: bool) -> str:
    if keyword_hit and symbolic_hit:
        return "HIGH"
    if symbolic_hit:
        return "MEDIUM"
    return "LOW"


# ─────────────────────────────────────────────
# Publiczny entry point (zgodny z konwencją filtrów)
# ─────────────────────────────────────────────

def run(parsed) -> dict:
    """
    Przyjmuje ParsedExpr z core.py.
    Zwraca:
      {
        "triggered": bool,
        "matches": [MillenniumMatch, ...],
        "summary": str,
        "open_problems": int,
        "solved_problems": int,
      }
    """
    raw = parsed.raw
    sym = getattr(parsed, "sym", None)

    keyword_hits = set(_detect_keywords(raw))
    symbolic_hits = set(_detect_symbolic(sym))
    all_hits = keyword_hits | symbolic_hits

    matches: List[MillenniumMatch] = []
    for pid in all_hits:
        info = MILLENNIUM_PROBLEMS[pid]
        kw_hit = pid in keyword_hits
        sym_hit = pid in symbolic_hits
        source = (
            "both" if (kw_hit and sym_hit)
            else "symbolic" if sym_hit
            else "keyword"
        )
        matches.append(MillenniumMatch(
            problem_id=info["id"],
            name=info["name"],
            status=info["status"],
            confidence=_confidence(kw_hit, sym_hit),
            source=source,
            risk_message=info["risk"],
            description=info["description"],
            solved_by=info.get("solved_by"),
        ))

    # Osobne liczniki
    open_count = sum(1 for m in matches if m.status == "OPEN")
    solved_count = sum(1 for m in matches if m.status == "SOLVED")

    # Podsumowanie tekstowe
    if not matches:
        summary = "Brak powiązań z Problemami Milenijnymi."
    else:
        names = ", ".join(m.name for m in matches)
        warnings = []
        if open_count:
            warnings.append(f"{open_count} OTWARTYCH problemu(-ów)")
        if solved_count:
            warnings.append(f"{solved_count} ROZWIĄZANEGO(-ch) problemu(-ów) — sprawdź aktualny status")
        summary = (
            f"Wykryto powiązania z: {names}. "
            + " | ".join(warnings)
            + ". Wyrażenie może zakładać lub implikować tezy nieudowodnione."
        )

    return {
        "triggered": bool(matches),
        "matches": [
            {
                "problem_id": m.problem_id,
                "name": m.name,
                "status": m.status,
                "confidence": m.confidence,
                "source": m.source,
                "risk": m.risk_message,
                "description": m.description,
                **({"solved_by": m.solved_by} if m.solved_by else {}),
            }
            for m in matches
        ],
        "summary": summary,
        "open_problems": open_count,
        "solved_problems": solved_count,
    }
