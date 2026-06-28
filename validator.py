"""
validator.py — jedyny publiczny entry point.
"""

from core import parse

from filters.information_filter import run as information_run
from filters.syntax_filter     import run as syntax_run
from filters.algebra_filter    import run as algebra_run
from filters.logic_filter      import run as logic_run
from filters.numeric_filter    import run as numeric_run
from filters.harmonic_filter   import run as harmonic_run
from filters.moebius_filter    import run as moebius_run
from filters.topology_filter   import run as topology_run
from filters.singularity_filter import run as singularity_run
from filters.prime_spectrum_filter import run as prime_spectrum_run
from filters.misleading_filter import run as misleading_run
from filters.millennium_filter import run as millennium_run

# ── [NOWE] tourosomobius Λ–τ–ρ ───────────────────────────────
from filters.tourosomobius_filter import run as tourosomobius_run
# ─────────────────────────────────────────────────────────────


FILTERS = {
    "information":    information_run,
    "syntax":         syntax_run,
    "algebra":        algebra_run,
    "logic":          logic_run,
    "numeric":        numeric_run,
    "harmonic":       harmonic_run,
    "moebius":        moebius_run,
    "topology":       topology_run,
    "singularity":    singularity_run,
    "prime_spectrum": prime_spectrum_run,
    "misleading":     misleading_run,
    "millennium":     millennium_run,
    "tourosomobius":  tourosomobius_run,
}


class StabilityLayer:
    def __init__(self):
        self.loop_index = 0

    def step(self):
        self.loop_index += 1
        angle = 72 * self.loop_index

        if self.loop_index <= 5:
            phase = "UNDEFINED"
        else:
            phase = "FORCED"

        if angle < 720:
            orientation = "RETURNING" if phase == "FORCED" else "M_PRIME"
        else:
            orientation = "CLOSED"

        return {
            "cycle":       self.loop_index,
            "angle":       angle,
            "phase":       phase,
            "orientation": orientation,
        }


stability = StabilityLayer()


def validate(equation: str) -> dict:
    p = parse(equation)

    filter_results = {name: fn(p) for name, fn in FILTERS.items()}

    millennium_result = filter_results.get("millennium", {})
    millennium_triggered = millennium_result.get("triggered", False)
    open_count = millennium_result.get("open_problems", 0)

    stability_state = stability.step()

    return {
        "filters":               filter_results,
        "stability":             stability_state,
        "millennium_warning":    millennium_triggered,
        "millennium_open_count": open_count,
    }
# filters/millennium_boundaries.py
# Warunki brzegowe dla 7 Problemów Milenijnych Clay Institute

BOUNDARIES = {
    "P_vs_NP": {
        "forbidden": [
            "P=NP", "NP=coNP", "SAT solved in polytime",
            "all NP problems reducible in P"
        ],
        "rule": "Nie wolno zakładać równoważności P i NP."
    },

    "Riemann": {
        "forbidden": [
            "all nontrivial zeros lie on 1/2",
            "RH true", "RH proven", "critical line theorem"
        ],
        "rule": "Nie wolno zakładać, że wszystkie zera nietrywialne leżą na Re(s)=1/2."
    },

    "Birch_Swinnerton_Dyer": {
        "forbidden": [
            "rank(E) equals order of zero",
            "BSD proven", "L(E,1)=0 implies infinite rational points"
        ],
        "rule": "Nie wolno zakładać pełnej zgodności rzędu krzywej z zerem funkcji L."
    },

    "Yang_Mills": {
        "forbidden": [
            "mass gap proven", "YM gap exists",
            "nonperturbative gauge mass"
        ],
        "rule": "Nie wolno zakładać istnienia masy w Yang–Mills bez dowodu."
    },

    "Navier_Stokes": {
        "forbidden": [
            "global regularity", "no blow-up",
            "smooth solution for all time"
        ],
        "rule": "Nie wolno zakładać globalnej regularności Navier–Stokes."
    },

    "Poincare": {
        "forbidden": [
            "Poincare open", "Poincare unsolved"
        ],
        "rule": "Nie wolno twierdzić, że Poincaré jest OTWARTY — jest ROZWIĄZANY."
    },

    "Hodge": {
        "forbidden": [
            "all cohomology classes are harmonic",
            "Hodge proven"
        ],
        "rule": "Nie wolno zakładać pełnej zgodności klas kohomologii z formami harmonicznymi."
    }
}


def run(parsed):
    expr = str(parsed.expr).lower()
    violations = []

    for name, data in BOUNDARIES.items():
        for forbidden in data["forbidden"]:
            if forbidden.lower() in expr:
                violations.append({
                    "problem": name,
                    "violation": forbidden,
                    "rule": data["rule"]
                })

    return {
        "violated": len(violations) > 0,
        "violations": violations,
        "count": len(violations)
    }
