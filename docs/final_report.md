# Raport końcowy: Wpływ promptu i temperatury na stabilność LLM w teście BFI-10

**Autorzy:** Filip Budzyński (319021), Dawid Budzyński (319020)
**Kurs:** Wyjaśnialna sztuczna inteligencja

## 1. Co badaliśmy

Hipoteza: **wariancja w sformułowaniu promptu istotnie wpływa na zmienność odpowiedzi LLM w teście osobowości BFI-10**.

Sprawdziliśmy ją na **3 modelach** × **3 typach promptu** × **4 temperaturach** × **10 powtórzeniach** = do 360 wywołań.

| Wymiar | Wartości |
|---|---|
| Modele | `mistral:7b` (Ollama), `llama3.1:8b` (Ollama), `openai/gpt-oss-20b:free` (OpenRouter) |
| Prompty | `baseline` (zero-shot), `few_shot` (3 przykłady), `format_constrained` (CSV-only) |
| Temperatury | 0.3, 0.5, 0.7, 1.0 |
| Powtórzenia | 10 per kombinacja |
| Metryka główna | Fleiss κ (zgodność powtórzeń, 1.0 = perfekcyjna) |

## 2. Wynik 1 — Wpływ temperatury

![Wpływ temperatury](../results/plots/01_temperature_effect.png)

| Temperatura | Średnia κ (po wszystkich model×prompt) |
|:---:|:---:|
| **0.3** | **0.742** |
| 0.5 | 0.715 |
| 0.7 | 0.604 |
| 1.0 | 0.504 |

**Trend:** im niższa temperatura, tym wyższa stabilność — zgodnie z intuicją (niska T = mniej losowości w samplingu).

**Wyjątki widoczne na wykresie:**
- **Mistral + few_shot** osiąga κ = 1.0 na *każdej* temperaturze — przykłady w prompcie tak silnie kotwiczą odpowiedź, że temperatura nie ma znaczenia.
- **gpt-oss + baseline @ T=0.3** spada nieoczekiwanie do 0.38. Hipoteza: upstream provider (OpenInference) routuje T=0.3 inaczej niż standardowa Ollama, plus seed jest tam ignorowany — więc wariancja może być artefaktem providera, nie samego modelu.

## 3. Wynik 2 — Wpływ typu promptu

![Wpływ promptu](../results/plots/02_prompt_effect.png)

| Prompt | Średnia κ | Zakres | n konfiguracji |
|---|:---:|:---:|:---:|
| **few_shot** | **0.803** | 0.374 – 1.000 | 12 |
| baseline | 0.563 | 0.361 – 0.803 | 12 |
| format_constrained | 0.517 | 0.356 – 0.751 | 8 (Mistral nie parsuje 0/40) |

**Wniosek:** few-shot jest średnio **+43% lepszy** od baseline (0.803 vs 0.563) i **+55% lepszy** od format_constrained. Trzy linijki przykładów w prompcie kotwiczą model do konkretnego rozumienia skali Likerta i drastycznie tną wariancję.

**Caveat (ważny dla XAI):** few-shot **nie jest uniwersalny**. Dla Llamy 3.1 ten sam few-shot prompt *pogarsza* stabilność (κ=0.467 vs 0.537 dla baseline) — większy model wydaje się generalizować z przykładów twórczo, zamiast je kopiować. Wniosek praktyczny: **każdy model trzeba zwalidować empirycznie**.

## 4. Wynik 3 — Ranking finalny (T=0.7, „standardowa" temperatura z proposala)

![Ranking](../results/plots/03_ranking.png)

| # | Konfiguracja | Fleiss κ | Interpretacja |
|---|---|:---:|---|
| 🥇 1 | mistral + few_shot | **1.000** | perfekcyjna zgodność |
| 🥈 2 | gpt-oss + few_shot | **0.798** | substantial agreement |
| 3 | gpt-oss + format_constrained | 0.537 | moderate |
| 4 | llama3.1 + baseline | 0.537 | moderate |
| 5 | mistral + baseline | 0.512 | moderate |
| 6 | gpt-oss + baseline | 0.509 | moderate |
| 7 | llama3.1 + format_constrained | 0.474 | low-moderate |
| 8 | llama3.1 + few_shot | 0.467 | low-moderate |

(`mistral + format_constrained` pominięty — 0/10 udanych parsowań; Mistral zwraca cyfry spoza 1–5 dla tego promptu.)

## 5. Najlepsza konfiguracja w całym eksperymencie

> **`mistral:7b` + few-shot prompt + T = 0.3** → Fleiss κ = **1.000**, Shannon H = 0.0, Levenshtein = 0.0 (idealnie powtarzalne 10 razy z rzędu)

Jeśli **interesuje nas konkretnie ChatGPT-klasa**: **`gpt-oss-20b` + few-shot** przy T=0.5 lub 0.7 daje κ ≈ 0.79 → solidne „substantial agreement" przy zachowaniu pewnej zmienności wartościowej dla realistycznej osobowości.

## 6. Hipoteza główna: potwierdzona

Różnica κ między najlepszym a najgorszym promptem dla **tego samego modelu i temperatury** wynosi do **0.488** (Mistral baseline 0.512 → few_shot 1.000 @ T=0.7). Wybór promptu zmienia więc zgodność z „moderate" na „perfect" — efekt jest **istotny i praktycznie wymierny**, nie statystyczny artefakt.

## 7. Rekomendacje produkcyjne

Dla aplikacji wymagających powtarzalnych odpowiedzi LLM (rekrutacja, oceny psychologiczne, mental-health AI):

1. **Zawsze few-shot, nigdy zero-shot baseline.** Średnio +0.24 κ.
2. **Niska temperatura (0.3–0.5).** Każde +0.2 do T to ~−0.08 κ.
3. **Format-constrained tylko z robust parserem** — małe modele (7B) potrafią zwracać wartości spoza skali (Mistral: 0% sukcesu).
4. **Waliduj empirycznie per model.** Sam fakt że few-shot działa świetnie dla Mistrala i gpt-oss nie oznacza że zadziała dla Llamy — u nas pogorszył wynik o 0.07 κ.

## 8. Surowe dane i kod

- Wyniki JSON: `results/results_tmptr_{3,5,10}.json`, `results/results.json`, `results/results_gpt_oss*.json`
- Skrypt wykresów: `siwy/experiments/visualize.py` (`python -m siwy.experiments.visualize`)
- Pełna metodologia: [`design_proposal.md`](../design_proposal.md)
- Szczegóły eksperymentalne: [`experiment_results.md`](experiment_results.md)
