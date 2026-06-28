# filters/millennium_filter.py
# Wykrywanie powiązań z Problemami Milenijnymi Clay Institute

PROBLEMS = {
    "P_vs_NP": {
        "keywords": ["P=NP", "NP=coNP", "SAT", "NP-hard", "NP-complete"],
        "open": True
    },
    "Riemann": {
        "keywords": ["ζ(s)", "zeta", "nontrivial zeros", "critical line", "Riemann"],
        "open": True
    },
    "Birch_Swinnerton_Dyer": {
        "keywords": ["elliptic curve", "rank", "BSD", "L-function"],
        "open": True
    },
    "Yang_Mills": {
        "keywords": ["Yang-Mills", "mass gap", "gauge theory", "QFT"],
        "open": True
    },
    "Navier_Stokes": {
        "keywords": ["Navier-Stokes", "fluid", "blow-up", "regularity"],
        "open": True
    },
    "Poincare": {
        "keywords": ["3-manifold", "simply connected", "Poincaré"],
        "open": False  # solved by Perelman
    },
    "Hodge": {
        "keywords": ["Hodge", "harmonic form", "cohomology"],
        "open": True
    }
}


def run(parsed):
    expr = str(parsed.expr).lower()

    matches = []
    open_count = 0
    solved_count = 0

    for name, data in PROBLEMS.items():
        for kw in data["keywords"]:
            if kw.lower() in expr:
                matches.append(name)
                if data["open"]:
                    open_count += 1
                else:
                    solved_count += 1
                break

    return {
        "triggered": len(matches) > 0,
        "matches": matches,
        "summary": f"Powiązania: {', '.join(matches)}" if matches else "Brak powiązań",
        "open_problems": open_count,
        "solved_problems": solved_count
    }
