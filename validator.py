"""
validator.py — jedyny publiczny entry point.

Naprawki względem oryginalnego repo:
1. Jedna definicja validate() (oryginał miał dwie — Python brał ostatnią)
2. parse() wywoływane RAZ — ParsedExpr współdzielony przez wszystkie filtry
3. Wszystkie 8 filtrów wywoływane (oryginał wywoływał tylko 2)
4. Routing przez słownik — łatwe dodawanie nowych filtrów
"""
from core import parse
from filters.syntax_filter     import run as syntax_run
from filters.algebra_filter    import run as algebra_run
from filters.logic_filter      import run as logic_run
from filters.numeric_filter    import run as numeric_run
from filters.harmonic_filter   import run as harmonic_run
from filters.moebius_filter    import run as moebius_run
from filters.topology_filter   import run as topology_run
from filters.singularity_filter import run as singularity_run

FILTERS = {
    "syntax":      syntax_run,
    "algebra":     algebra_run,
    "logic":       logic_run,
    "numeric":     numeric_run,
    "harmonic":    harmonic_run,
    "moebius":     moebius_run,
    "topology":    topology_run,
    "singularity": singularity_run,
}


def validate(equation: str) -> dict:
    """Parsuje wyrażenie raz, uruchamia wszystkie filtry Λ–τ–ρ."""
    p = parse(equation)
    return {name: fn(p) for name, fn in FILTERS.items()}
