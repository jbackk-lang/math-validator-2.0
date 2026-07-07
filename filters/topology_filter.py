"""
Topology Filter — wersja z logowaniem topologii
Model: Λ–τ–ρ + M²-closure + inwarianty topologiczne + pełne logowanie

Logowanie:
  • log_topology() — centralny logger
  • logi globalnych inwariantów
  • logi lokalnej analizy
  • logi operatorów (z cache)
  • logi early-exit zależnego od StabilityLayer
"""

from typing import Any, Dict


# ─────────────────────────────────────────────────────────────────────────────
#  LOGOWANIE
# ─────────────────────────────────────────────────────────────────────────────

def log_topology(event: str, data: Dict[str, Any]) -> None:
    """
    Minimalistyczny logger topologiczny.
    Nie używa print(), nie używa globalnego stanu.
    Zapisuje logi w strukturze zwracanej przez filtr.
    """
    if "_log" not in data:
        data["_log"] = []
    data["_log"].append(event)


# Cache operatorów
TOPO_CACHE: Dict[str, Dict[str, Any]] = {}


# ─────────────────────────────────────────────────────────────────────────────
# 1. GLOBALNE INWARIANTY
# ─────────────────────────────────────────────────────────────────────────────

def compute_invariants(ast: Any, log: Dict[str, Any]) -> Dict[str, Any]:
    stack = [ast]
    cycles = 0
    closures = 0
    singularities = 0
    depth = 0
    mobius_loops = 0

    while stack:
        node = stack.pop()
        depth += 1

        op = getattr(node, "op", None)

        if op in ("**", "/", "sin", "cos"):
            cycles += 1

        if hasattr(node, "children") and len(node.children) == 1:
            closures += 1

        if op in ("log", "/") and getattr(node, "value", None) == 0:
            singularities += 1

        if op in ("sin", "cos", "tan"):
            mobius_loops += 1

        if hasattr(node, "children"):
            stack.extend(node.children)

    invariants = {
        "cycles": cycles,
        "closures": closures,
        "singularities": singularities,
        "depth": depth,
        "mobius_loops": mobius_loops,
    }

    log_topology("invariants_computed", log)
    return invariants


# ─────────────────────────────────────────────────────────────────────────────
# 2. ANALIZA LOKALNA
# ─────────────────────────────────────────────────────────────────────────────

def analyze_local(ast: Any, invariants: Dict[str, Any], log: Dict[str, Any]) -> Dict[str, Any]:
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

    local = {
        "local_nodes": local_nodes,
        "operators": list(operators),
        "complexity": local_nodes + invariants["depth"],
    }

    log_topology("local_analysis_done", log)
    return local


# ─────────────────────────────────────────────────────────────────────────────
# 3. ANALIZA OPERATORÓW (z cache)
# ─────────────────────────────────────────────────────────────────────────────

def analyze_operator(node: Any, log: Dict[str, Any]) -> Dict[str, Any]:
    op = getattr(node, "op", None)
    if not op:
        return {"type": "literal"}

    if op in TOPO_CACHE:
        log_topology(f"operator_cached:{op}", log)
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
    log_topology(f"operator_analyzed:{op}", log)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 4. GŁÓWNY FILTR — z logowaniem
# ─────────────────────────────────────────────────────────────────────────────

def run(ast: Any, stability: Dict[str, Any]) -> Dict[str, Any]:
    log: Dict[str, Any] = {}

    # Early exit — UNDEFINED
    if stability["phase"] == "UNDEFINED":
        log_topology("early_exit_phase_undefined", log)
        return {
            "status": "SKIPPED",
            "reason": "Phase UNDEFINED — early exit",
            "orientation": stability["orientation"],
            "_log": log["_log"],
        }

    # Early exit — CLOSED
    if stability["orientation"] == "CLOSED":
        log_topology("early_exit_orientation_closed", log)
        return {
            "status": "TRIVIAL",
            "reason": "Orientation CLOSED — trivial topology",
            "invariants": {"closures": 1},
            "_log": log["_log"],
        }

    # 1. Globalne inwarianty
    invariants = compute_invariants(ast, log)

    # 2. Analiza lokalna
    local = analyze_local(ast, invariants, log)

    # 3. Analiza operatorów
    op_analysis = []
    stack = [ast]
    while stack:
        node = stack.pop()
        op_analysis.append(analyze_operator(node, log))
        if hasattr(node, "children"):
            stack.extend(node.children)

    log_topology("operator_analysis_complete", log)

    # 4. Wynik końcowy
    return {
        "status": "OK",
        "phase": stability["phase"],
        "orientation": stability["orientation"],
        "invariants": invariants,
        "local": local,
        "operators": op_analysis,
        "_log": log["_log"],
    }
