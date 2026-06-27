## 🔗 Wszystkie modele i repozytoria
Pełna lista projektów znajduje się na stronie:
https://jbackk-lang.github.io
---
# math-validator-2.0

`math-validator-2.0` to druga generacja walidatora struktur matematycznych.  
Został zaprojektowany tak, aby wykrywać nie tylko błędy składniowe, ale również
tzw. **problemy mylne** — wyrażenia pozornie poprawne, które są niespójne
w szerszym kontekście logicznym.

---

## 🔧 Funkcje

- analiza składniowa wyrażeń matematycznych,
- wykrywanie sprzeczności,
- klasyfikacja błędów:
  - `OK` — poprawne,
  - `ERROR` — błąd składni lub sprzeczność,
  - `MISLEADING` — problem mylny (pozorna poprawność),
- modułowa architektura (parser → walidator → raport),
- przygotowany pod integrację z TRM / TIMDR (Λ–Τ–Ρ).

---

## 🆚 Różnice względem `math-validator` (1.0)

- przebudowany parser,
- rozszerzona logika błędów,
- dodany typ `MISLEADING`,
- możliwość eksportu wyników do CSV / JSONL,
- przygotowane miejsce na integrację z TRM i TIMDR.

---

## ▶️ Jak używać

Plik wejściowy `input.txt`:


---

# math-validator-2.0

py -3.14 -m pip install uvicorn fastapi

py -3.14 -m uvicorn api:app --reload

uvicorn app:app --reload

http://127.0.0.1:8000/validate?expr=1/(x-1)
