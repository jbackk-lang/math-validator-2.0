"""
validator.py — jedyny publiczny entry point.

Poprawki v2:
  1. StabilityLayer przeniesiony do scope'u per-request (był globalnym singletonem
     — w FastAPI / wielowątkach współdzielił loop_index między requestami)
  2. Jedna definicja validate() — oryginał miał dwie (Python brał ostatnią)
  3. parse() wywoływane RAZ — ParsedExpr współdzielony przez wszystkie filtry
  4. Wszystkie filtry Λ–τ–ρ wywoływane przez słownik
"""

from core import parse
from filters.information_filter  import run as information_run
from filters.syntax_filter       import run as syntax_run
from filters.algebra_filter      import run as algebra_run
from filters.logic_filter        import run as logic_run
from filters.numeric_filter      import run as numeric_run
from filters.harmonic_filter     import run as harmonic_run
from filters.moebius_filter      import run as moebius_run
from filters.topology_filter     import run as topology_run
from filters.singularity_filter  import run as singularity_run
from filters.prime_spectrum_filter import run as prime_spectrum_run
from filters.misleading_filter   import run as misleading_run

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
}


# ── StabilityLayer Λ–τ–ρ ─────────────────────────────────────────────────────
# POPRAWKA: klasa bez stanu globalnego — instancja tworzona per-wywołanie
# validate() lub per-sesję przez klienta (np. API).
# Oryginał: `stability = StabilityLayer()` na poziomie modułu — niebezpieczne
# w środowiskach wielowątkowych (FastAPI, Gunicorn).

class StabilityLayer:
    """
    Warstwa stabilności Λ→τ→ρ — 10 pętli, bifurkacja po 5.

    Użycie per-sesję (bezpieczne wielowątkowo):
        session = StabilityLayer()
        result  = validate("x**2", stability=session)
    """

    def __init__(self):
        self.loop_index = 0

    def step(self) -> dict:
        self.loop_index += 1
        angle = 72 * self.loop_index

        if self.loop_index <= 5:
            phase = "UNDEFINED"       # stan nieoznaczony
        else:
            phase = "FORCED"          # system dąży do domknięcia

        if phase == "FORCED" and angle < 720:
            orientation = "RETURNING"
        elif angle >= 720:
            orientation = "CLOSED"    # M²-closure
        else:
            orientation = "M_PRIME"

        return {
            "cycle":       self.loop_index,
            "angle":       angle,
            "phase":       phase,
            "orientation": orientation,
        }


def validate(equation: str, stability: StabilityLayer | None = None) -> dict:
    """
    Parsuje wyrażenie raz, uruchamia wszystkie filtry Λ–τ–ρ.

    Parametry:
        equation  : wyrażenie matematyczne jako string
        stability : opcjonalna instancja StabilityLayer (per-sesja).
                    Jeśli None — tworzona lokalnie (stateless, bezpieczne).

    Zwraca:
        {
          "filters":   { nazwa_filtru: wynik, ... },
          "stability": { cycle, angle, phase, orientation },
        }
    """
    if stability is None:
        stability = StabilityLayer()

    p              = parse(equation)
    filter_results = {name: fn(p) for name, fn in FILTERS.items()}
    stability_state = stability.step()

    return {
        "filters":   filter_results,
        "stability": stability_state,
    }
