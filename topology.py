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
    mobius_loops = 0

    while stack:
        node = stack.pop()
        depth += 1

        # Detekcja cykli (np. powtarzające się struktury operatorów)
        if getattr(node, "op", None) in ("**", "/", "sin", "cos"):
            cycles += 1

        # Domknięcia topologiczne (np. struktury typu f(f(x)))
        if hasattr(node, "children") and len(node.children) == 1:
            closures += 1

        # Osobliwości (np. dzielenie przez zero, log(0), pow(x, -1))
        if getattr(node, "op", None) in ("log", "/") and getattr(node, "value", None) == 0:
            singularities += 1

        # Pętle Möbiusa — heurystyka: operator o niezmiennej orientacji
        if getattr(node, "op", None) in ("sin", "cos", "tan"):
            mobius_loops += 1

        # Iteracyjne przejście
        if hasattr(node, "children"):
            stack.extend(node.children)

    return {
        "cycles": cycles,
        "closures": closures,
        "singularities": singularities,
        "depth": depth,
        "mobius_loops": mobius_loops,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 2. ANALIZA LOKALNA — lekka, zależna od inwariantów
# ─────────────────────────────────────────────────────────────────────────────

def analyze_local(ast: Any, invariants: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lekka analiza lokalna — nie powtarza globalnych obliczeń.
    """

    stack = [ast]
    local_nodes = 0
    operators = set()

    while stack:
        node = stack.pop()
        local_nodes += 1

        op = getattr(node, "op", None)
        if op:
            operators.add(op)

        if hasattr(node, "children"):
            stack.extend(node.children)

    return {
        "local_nodes": local_nodes,
        "operators": list(operators),
        "complexity": local_nodes + invariants["depth"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3. ANALIZA OPERATORÓW — z cache
# ─────────────────────────────────────────────────────────────────────────────

def analyze_operator(node: Any) -> Dict[str, Any]:
    op = getattr(node, "op", None)
    if not op:
        return {"type": "literal"}

    if op in TOPO_CACHE:
        return TOPO_CACHE[op]

    if op in ("+", "-"):
        result = {"type": "linear", "orientation": "M_PRIME"}
    elif op in ("*", "/"):
        result = {"type": "multiplicative", "orientation": "RETURNING"}
    elif op == "**":
        result = {"type": "exponential", "orientation": "CLOSED"}
    else:
        result = {"type": "function", "orientation": "RETURNING"}

    TOPO_CACHE[op] = result
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 4. GŁÓWNA FUNKCJA FILTRA — z early-exit Λ–τ–ρ
# ─────────────────────────────────────────────────────────────────────────────

def run(ast: Any, stability: Dict[str, Any]) -> Dict[str, Any]:
    """
    Główny filtr topologiczny:
      • early-exit zależny od StabilityLayer
      • globalne inwarianty liczone raz
      • lokalna analiza lekka
      • cache operatorów
    """

    # Early exit — faza UNDEFINED → nie analizujemy głębokiej topologii
    if stability["phase"] == "UNDEFINED":
        return {
            "status": "SKIPPED",
            "reason": "Phase UNDEFINED — early exit",
            "orientation": stability["orientation"],
        }

    # Early exit — CLOSED → struktura domknięta
    if stability["orientation"] == "CLOSED":
        return {
            "status": "TRIVIAL",
            "reason": "Orientation CLOSED — trivial topology",
            "invariants": {"closures": 1},
        }

    # 1. Globalne inwarianty
    invariants = compute_invariants(ast)

    # 2. Analiza lokalna
    local = analyze_local(ast, invariants)

    # 3. Analiza operatorów
    op_analysis = []
    stack = [ast]
    while stack:
        node = stack.pop()
        op_analysis.append(analyze_operator(node))
        if hasattr(node, "children"):
            stack.extend(node.children)

    # 4. Wynik końcowy
    return {
        "status": "OK",
        "phase": stability["phase"],
        "orientation": stability["orientation"],
        "invariants": invariants,
        "local": local,
        "operators": op_analysis,
    }
