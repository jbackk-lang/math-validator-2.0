import numpy as np
from math import gcd

def calculate_geometric_resonance(omega_input, omega_pivot, max_harmonic=8, tolerance=1e-3):
    """
    Rygorystyczny test walidacyjny dla homogeniczności geometrii pól.
    Sprawdza, czy stosunek częstotliwości wejściowej do punktu zwrotnego (pivot)
    odpowiada czystym, wymiernym proporcjom topologicznym (m/n).
    
    Terminologia oficjalna: Analiza spektralna rezonansu fali stojącej.
    Terminologia ukryta (muzyczna): Detekcja konsonansu/dysonansu układu.
    """
    # 1. Obliczenie surowego stosunku częstotliwości układu
    raw_ratio = omega_input / omega_pivot
    
    best_m = 1
    best_n = 1
    min_delta = float('inf')
    
    # 2. Szukanie najbliższego węzła topologicznego (liczby całkowite m, n)
    for n in range(1, max_harmonic + 1):
        # Znajdź najbliższe m dla danego n
        m = round(raw_ratio * n)
        if m == 0 or m > max_harmonic * 2:
            continue
            
        delta = abs(raw_ratio - (m / n))
        if delta < min_delta:
            min_delta = delta
            best_m = m
            best_n = n

    # Skrócenie ułamka do formy podstawowej
    common_divisor = gcd(best_m, best_n)
    m_prime = best_m // common_divisor
    n_prime = best_n // common_divisor

    # 3. Kryterium 1: Indeks Spójności Geometrycznej (GRI) 
    # Odpowiednik "czystości interwału". Im niższe m*n, tym stabilniejszy stan geometryczny.
    geometric_resonance_index = 1.0 / (m_prime * n_prime)
    
    # 4. Kryterium 2: Napięcie Pola (Field Tension)
    # Odchylenie od idealnego węzła. Jeśli delta < tolerance, układ jest w stanie czystego rezonansu.
    # Jeśli delta jest mierzalna, układ posiada asymetryczne naprężenie.
    is_resonant = min_delta <= tolerance
    
    return {
        "ratio_string": f"{m_prime}:{n_prime}",
        "raw_ratio": round(raw_ratio, 4),
        "geometric_resonance_index": round(geometric_resonance_index, 4),
        "field_tension_delta": round(min_delta, 6),
        "is_perfect_resonance": is_resonant
    }

# --- TEST WALIDATORA DLA TRZECH SKAL ---

# 1. Skala Atomowa: Stabilność Żelaza (Idealny stan podstawowy - Oktawa 2:1)
print("--- SKALA ATOMOWA (Helium/Fe) ---")
print(calculate_geometric_resonance(omega_input=500.0, omega_pivot=250.0))

# 2. Skala Makro: Dysk akrecyjny Sgr A* (Wzmocnienie dżetu - Kwinta 3:2)
print("\n--- SKALA MAKRO (Astro-Map) ---")
print(calculate_geometric_resonance(omega_input=300.1, omega_pivot=200.0))

# 3. Skala Kwantowa: Photon Engine (Szukana asymetria - wysokie naprężenie pola, np. 8:5)
print("\n--- SKALA KWANTOWA (Photon Engine) ---")
print(calculate_geometric_resonance(omega_input=800.0, omega_pivot=500.0, tolerance=1e-5))
