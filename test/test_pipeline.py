"""
test_pipeline.py — Integracyjny potok testowy: PC Model -> Math Validator -> Dashboard Output.
"""
from validator import validate, StabilityLayer
from pc_model_simulator import PCModelSimulator
import json

def run_integration_test():
    simulator = PCModelSimulator()
    
    # Inicjalizacja sesji/warstwy stabilności (symulacja potoku Gia dla 3 różnych requestów)
    print("=" * 70)
    print("Uruchamianie Topologicznego Potoku Testowego (Pętla M²)")
    print("=" * 70)

    scenarios = [
        ("STABILNY TRZON", simulator.generate_stable_state()),
        ("ANOMALIA TOPOLOGICZNA", simulator.generate_moebius_anomaly()),
        ("PUNKT OSOBLIWY", simulator.generate_critical_singularity())
    ]

    for name, data in scenarios:
        print(f"\n[TEST] Testowanie scenariusza: {name}")
        print(f"  Równanie z PC Model: {data['equation']}")
        print(f"  Opis fizyczny: {data['description']}")
        
        # Tworzymy osobną, czystą warstwę stabilności per-request (Poprawka v2 z validator.py)
        session_stability = StabilityLayer()
        
        # Wykonujemy krok ewolucji (wymuszamy przejście w pętli dla testu)
        # Symulujemy, że system wykonał już kilka obrotów i wchodzi w fazę FORCED
        for _ in range(5):
            session_stability.step()
            
        # Główna walidacja topologiczna
        result = validate(data["equation"], stability=session_stability)
        
        # Renderowanie wyników w formacie czytelnym dla Dashboardu
        print(f"  Status Warstwy Stabilności:")
        print(f"    Cykl: {result['stability']['cycle']} | Faza: {result['stability']['phase']} | Orientacja: {result['stability']['orientation']}")
        print(f"  Wyniki Filtrów Topologicznych:")
        
        # Wyciągamy interesujące nas filtry z potoku
        for filter_name in ["moebius", "topology", "singularity"]:
            f_res = result["filters"].get(filter_name, {"status": "UNKNOWN", "details": "Brak filtra"})
            color = "🟢" if f_res["status"] == "PASSED" else "🔴"
            print(f"    {color} [{filter_name.upper()}]: Status: {f_res['status']} | {f_res['details']}")
            
    print("\n" + "=" * 70)
    print("Test integracyjny zakończony.")
    print("=" * 70)

if __name__ == "__main__":
    # Mockowanie funkcji parse na potrzeby testu izolowanego (jeśli core nie jest w pełni spięty)
    import sys
    import types
    
    # Tworzymy atrapę modułu core, jeśli nie istnieje w lokalnej ścieżce
    try:
        import core
    except ImportError:
        core_mock = types.ModuleType('core')
        def parse_mock(eq):
            # Atrapa obiektu ParsedExpr posiadającego atrybut source_str
            class ParsedExpr:
                def __init__(self, s): self.source_str = s
            return ParsedExpr(eq)
        core_mock.parse = parse_mock
        sys.modules['core'] = core_mock
        
    # Atrapy pozostałych filtrów, aby słownik FILTERS w validator.py się nie wyłożył
    import validator
    for filter_key in validator.FILTERS.keys():
        if filter_key not in ["moebius", "topology", "singularity"]:
            validator.FILTERS[filter_key] = lambda p: {"status": "PASSED", "details": "Ignorowany w tym teście polowym."}

    run_integration_test()
