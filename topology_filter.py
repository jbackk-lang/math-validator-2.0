"""
topology_filter.py — warstwa Λ–τ–ρ.
Λ: struktura wyrażenia (z ParsedExpr, bez sympify).
τ: score transformacji.
ρ: delegowane do singularity_filter (z cache).
"""
from core import ParsedExpr
from filters.singularity_filter import run as singularity_run


def run(p: ParsedExpr) -> dict:
    if p.error:
        return {"status": "error", "message": p.error}

    # Λ — struktura (już obliczona w core.parse, zero kosztu)
    lam = {
        "cycles":    p.cycles,
        "fractions": p.fractions,
        "powers":    p.powers,
    }

    # τ — score transformacji
    tau = 0
    if "/" in p.raw:      tau += 1
    if "**-1" in p.raw:  tau += 1
    if "sqrt" in p.raw:  tau += 1
    if "^" in p.raw:     tau += 1

    # ρ — z singularity_filter (cached)
    rho = singularity_run(p)

    return {
        "status":        rho["status"],
        "Λ_structure":   lam,
        "τ_transforms":  tau,
        "ρ_defects":     rho["ρ_defects"],
        "twists":        rho["twists"],
        "singularities": rho["singularities"],
        "notes":         rho["notes"],
    }
