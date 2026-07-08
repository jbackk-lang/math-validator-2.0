"""
closed_loop_pipeline.py — Silnik integracyjny dla math-validator-2.0 i TRM-Geometry-Core.
Weryfikuje niezmienniki topologiczne dla wszystkich operatorów przejściowych.
"""
import math
import sys
# Zakładamy, że moduły z TRM-Geometry-Core/src są dostępne w ścieżce
# Jeśli pliki są w tym samym katalogu, import zadziała bezpośrednio:
try:
    import transitions
    import quadrature
    import triangle
    import cube
    import sphere
    import circle
except ImportError:
    print("⚠️  [BŁĄD] Brak plików źródłowych z TRM-Geometry-Core w PYTHONPATH.")
    print("Upewnij się, że pliki geometryczne znajdują się w tym samym folderze lub zostały zainstalowane.")
    sys.exit(1)

def verify_geometric_closures(r: float = 1.0) -> bool:
    print(f"=== URUCHAMIANIE WALIDACJI TOPOLOGICZNEJ DLA PROMIENIA r = {r} ===")
    
    # 1. Walidacja operatora kwadratury koła
    op_square = transitions.circle_to_square_operator()
    calc_square = quadrature.square_side_from_circle(r)
    expected_square = r * op_square
    
    if not math.isclose(calc_square, expected_square):
        print("🔴 ANOMALIA: Błąd transformacji kwadratury koła!")
        return False
    print("🟢 Operator kwadratury koła: ZGODNY")

    # 2. Walidacja operatora trygonalnego (Triangle)
    op_triangle = transitions.circle_to_triangle_operator()
    calc_triangle = triangle.side_from_radius(r)
    expected_triangle = r * op_triangle
    
    if not math.isclose(calc_triangle, expected_triangle):
        print("🔴 ANOMALIA: Błąd symetrii trygonalnej pętli!")
        return False
    print("🟢 Operator trygonalny pętli: ZGODNY")

    # 3. Walidacja operatora sferyczno-ortogonalnego (Cube)
    op_cube = transitions.sphere_to_cube_operator()
    calc_cube = cube.side_from_sphere(r)
    expected_cube = 2 * r / math.sqrt(3) # Sprawdzenie ze wzorem bazowym
    
    if not math.isclose(calc_cube, expected_cube) or not math.isclose(calc_cube, r * op_cube):
        print("🔴 ANOMALIA: Przerwanie ciągłości na rzucie sferycznym!")
        return False
    print("🟢 Operator rzutu sferycznego: ZGODNY")

    print("\n🚀 [M²-CLOSURE SUCCESSFUL] Wszystkie operatory geometrii zachowują ciągłość fluksu.")
    return True

if __name__ == "__main__":
    success = verify_geometric_closures(1.0)
    if not success:
        sys.exit(1)
