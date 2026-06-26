"""
validator.py — jedyny publiczny entry point.

Naprawki względem oryginalnego repo:
1. Jedna definicja validate() (oryginał miał dwie — Python brał ostatnią)
2. parse() wywoływane RAZ — ParsedExpr współdzielony przez wszystkie filtry
3. Wszystkie 8 filtrów wywoływane (oryginał wywoływał tylko 2)
4. Routing przez słownik — łatwe dodawanie nowych filtrów
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

FILTERS = {
    "syntax":        syntax_run,
    "algebra":       algebra_run,
    "logic":         logic_run,
    "numeric":       numeric_run,
    "harmonic":      harmonic_run,
    "moebius":       moebius_run,
    "topology":      topology_run,
    "singularity":   singularity_run,
    "prime_spectrum": prime_spectrum_run,
}

# --- Warstwa stabilności λ→τ→ρ (10 pętli, bifurkacja po 5) ---

class StabilityLayer:
    def __init__(self):
        self.loop_index = 0

    def step(self):
        self.loop_index += 1
        angle = 72 * self.loop_index

        if self.loop_index <= 5:
            phase = "UNDEFINED"   # stan nieoznaczony materii
        else:
            phase = "FORCED"      # system musi dążyć do domknięcia albo cofnięcia

        if angle < 720:
            orientation = "RETURNING" if phase == "FORCED" else "M_PRIME"
        else:
            orientation = "CLOSED"  # M²-closure

        return {
            "cycle": self.loop_index,
            "angle": angle,
            "phase": phase,
            "orientation": orientation
        }

stability = StabilityLayer()

def validate(equation: str) -> dict:
    """Parsuje wyrażenie raz, uruchamia wszystkie filtry Λ–τ–ρ + warstwę stabilności."""
    p = parse(equation)

    filter_results = {name: fn(p) for name, fn in FILTERS.items()}
    stability_state = stability.step()

    return {
        "filters":   filter_results,
        "stability": stability_state,
    }
