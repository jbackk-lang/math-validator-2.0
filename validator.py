"""
validator.py — jedyny publiczny entry point.

Naprawki względem oryginalnego repo:
1. Jedna definicja validate() (oryginał miał dwie — Python brał ostatnią)
2. parse() wywoływane RAZ — ParsedExpr współdzielony przez wszystkie filtry
3. Wszystkie filtry Λ–τ–ρ wywoływane przez słownik
4. Dodany filtr 'misleading' — wykrywa problemy mylne
5. [NOWE] Dodany filtr 'millennium' — wykrywa powiązania z 7 Problemami Milenijnymi
   Clay Mathematics Institute (P vs NP, Riemann, BSD, Yang–Mills,
   Navier–Stokes, Poincaré [SOLVED], Hodge).
   Filtr ostrzega, gdy wyrażenie zakłada lub implikuje nieudowodnione tezy.
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

# ── [NOWE] Import filtra Problemów Milenijnych ───────────────────────────────
# Umieść plik millennium_filter.py w katalogu filters/
from filters.millennium_filter import run as millennium_run
# ─────────────────────────────────────────────────────────────────────────────

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
    # ── [NOWE] ────────────────────────────────────────────────────────────────
    "millennium":     millennium_run,
    # ─────────────────────────────────────────────────────────────────────────
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
            orientation = "CLOSED"    # M²-closure

        return {
            "cycle":       self.loop_index,
            "angle":       angle,
            "phase":       phase,
            "orientation": orientation,
        }


stability = StabilityLayer()


def validate(equation: str) -> dict:
    """
    Parsuje wyrażenie raz, uruchamia wszystkie filtry Λ–τ–ρ + warstwę stabilności.
    Zwraca pełny słownik wyników filtrów oraz stan stabilności.

    Nowe pole 'millennium' w 'filters':
      {
        "triggered": bool,          # True jeśli wykryto powiązanie
        "matches": [...],           # lista dopasowanych problemów
        "summary": str,             # czytelne podsumowanie
        "open_problems": int,       # liczba OTWARTYCH problemów
        "solved_problems": int,     # liczba ROZWIĄZANYCH problemów (Poincaré)
      }

    Uwaga dot. Problemów Milenijnych:
      Filtr NIE rozwiązuje problemów — jedynie wykrywa, że wyrażenie może
      zakładać twierdzenia, które są wciąż nieudowodnione (lub błędnie
      zakładać, że Hipoteza Poincarégo jest otwarta, gdy jest już SOLVED).
      Każde wyrażenie powiązane z otwartym problemem milenijnym powinno być
      traktowane z najwyższą ostrożnością matematyczną.
    """
    p = parse(equation)

    filter_results = {name: fn(p) for name, fn in FILTERS.items()}

    # ── [NOWE] Post-processing: podnieś flagę globalną jeśli millennium triggered ──
    millennium_result = filter_results.get("millennium", {})
    millennium_triggered = millennium_result.get("triggered", False)
    open_count = millennium_result.get("open_problems", 0)

    stability_state = stability.step()

    return {
        "filters":               filter_results,
        "stability":             stability_state,
        # ── [NOWE] skrót na najwyższym poziomie dla łatwego dostępu ──────────
        "millennium_warning":    millennium_triggered,
        "millennium_open_count": open_count,
        # ─────────────────────────────────────────────────────────────────────
    }
