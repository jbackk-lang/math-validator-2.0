"""
Topology Filter — wersja zoptymalizowana dla math-validator-2.0
Autor: jbackk-lang
Model: Λ–τ–ρ + M²-closure + inwarianty topologiczne liczone jednokrotnie

Założenia:
  • Pracujemy wyłącznie na AST (parsed_expression).
  • Inwarianty globalne liczone raz, przekazywane do analizy lokalnej.
  • Early-exit zależny od StabilityLayer (phase/orientation).
  • Iteracyjne przejście po AST (bez rekursji).
  • Cache operatorów topologicznych.
"""

from typing import Any, Dict

# Cache operatorów (stałe topologiczne)
TOPO_CACHE: Dict[str, Dict[str, Any]] = {}


# ─────────────────────────────────────────────────────────────────────────────
# 1. GLOBALNE INWARIANTY TOPOLOGICZNE — liczone raz
# ─────────────────────────────────────────────────────────────────────────────

def compute_invariants(ast: Any) -> Dict[str, Any]:
    """
    Liczy globalne inwarianty topologiczne:
      • liczba cykli
      • liczba domknięć
      • liczba osobliwości
      • głębokość drzewa
      • liczba pętli Möbiusa
    """

    stack = [ast]
    cycles = 0
    closures = 0
    singularities = 0
    depth = 0
    mobius_lo
