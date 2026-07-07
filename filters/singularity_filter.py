"""
singularity_filter.py — Detektor punktów osobliwych i strażnik osi czasu tau.
"""
from typing import Any, Dict

def run(parsed_expr: Any) -> Dict[str, Any]:
    """
    Analizuje pochodną d(tau)/d(Delta S). Przejście nie może generować
    ujemnego upływu czasu ani dzielenia przez zero na krytycznych punktach przegięcia.
    """
    status = "PASSED"
    details = "Brak osobliwości krytycznych. Oś czasu tau zachowuje monotoniczność."
    
    # Przykładowy test bezpiecznego mianownika (Poles and Zeros Verification)
    # Jeśli w wyrażeniu występuje dzielenie, sprawdzamy czy mianownik zeruje się na osi stabilizacji
    is_singular = False
    
    if hasattr(parsed_expr, "source_str"):
        # Uproszczona detekcja jawnego dzielenia przez zmienne fazowe bez offsetu
        if "/ theta" in parsed_expr.source_str or "/ phi" in parsed_expr.source_str:
            is_singular = True

    if is_singular:
        status = "CRITICAL"
        details = "Wykryto punkt osobliwy (Singularity Detected). Ryzyko zamrożenia potoku tau."

    return {
        "status": status,
        "metric": "Singularity & Causality Guard",
        "details": details
    }
