# Experiment Results: Prompt Stability in LLM Personality Tests

## Methodology

| Parameter | Value |
|----------|-------|
| Models | Mistral 7B Instruct (Ollama), Llama 3.1 8B Instruct (Ollama), gpt-oss-20b (OpenRouter, free tier) |
| Questionnaire | BFI-10 (Big Five Inventory, 10 items) |
| Prompt types | baseline, few-shot, format_constrained |
| Repetitions | 10 per configuration |
| Temperature | 0.3, 0.5, 0.7, 1.0 (główna analiza poniżej: temp=0.7) |
| Seeds | 42-51 per repetition (gpt-oss: upstream JAX provider ignoruje seed, stąd wariancja czysto stochastyczna) |

## Results

### Combined Metrics Table

| Temp | Model   | Prompt              | N   | Fleiss κ | Kripp α | Shannon H | Mean Std | Cosine | Levensht. |
|------|---------|---------------------|-----|----------|----------|-----------|----------|--------|------------|
| 0.3 | llama3.1 | baseline           | 10  | 0.803    | 0.990    | 0.336     | 0.194    | 0.988  | 0.156      |
| 0.3 | llama3.1 | few_shot           | 10  | **1.000**| 0.990    | -0.000    | 0.000    | 1.000  | **0.000**  |
| 0.3 | llama3.1 | format_constrained | 10  | 0.486    | 0.990    | 0.809     | 0.642    | 0.952  | 0.369      |
| 0.3 | mistral  | baseline           | 10  | 0.751    | 0.990    | 0.377     | 0.215    | 0.996  | 0.164      |
| 0.3 | mistral  | few_shot           | 10  | **1.000**| 0.990    | -0.000    | 0.000    | 1.000  | **0.000**  |
| 0.3 | mistral  | format_constrained | 0   | N/A      | N/A      | N/A       | N/A      | N/A    | N/A        |
| 0.5 | llama3.1 | baseline           | 10  | 0.770    | 0.990    | 0.392     | 0.216    | 0.989  | 0.182      |
| 0.5 | llama3.1 | few_shot           | 10  | 0.839    | 0.990    | 0.282     | 0.166    | 0.993  | 0.127      |
| 0.5 | llama3.1 | format_constrained | 10  | 0.455    | 0.990    | 0.915     | 0.679    | 0.954  | 0.400      |
| 0.5 | mistral  | baseline           | 10  | 0.601    | 0.990    | 0.605     | 0.336    | 0.991  | 0.280      |
| 0.5 | mistral  | few_shot           | 10  | **1.000**| 0.990    | -0.000    | 0.000    | 1.000  | **0.000**  |
| 0.5 | mistral  | format_constrained | 0   | N/A      | N/A      | N/A       | N/A      | N/A    | N/A        |
| 0.7 | llama3.1 | baseline           | 10  | 0.537    | 0.990    | 0.822     | 0.561    | 0.959  | 0.293      |
| 0.7 | llama3.1 | few_shot           | 10  | 0.467    | 0.990    | 0.883     | 0.739    | 0.946  | 0.307      |
| 0.7 | llama3.1 | format_constrained | 10  | 0.474    | 0.990    | 0.846     | 0.528    | 0.964  | 0.387      |
| 0.7 | mistral  | baseline           | 10  | 0.512    | 0.990    | 0.695     | 0.366    | 0.989  | 0.342      |
| 0.7 | mistral  | few_shot           | 10  | **1.000**| 0.990    | -0.000    | 0.000    | 1.000  | **0.000**  |
| 0.7 | mistral  | format_constrained | 0   | N/A      | N/A      | N/A       | N/A      | N/A    | N/A        |
| 1.0 | llama3.1 | baseline           | 10  | 0.477    | 0.990    | 0.943     | 0.728    | 0.938  | 0.402      |
| 1.0 | llama3.1 | few_shot           | 10  | 0.374    | 0.990    | 1.057     | 0.815    | 0.933  | 0.433      |
| 1.0 | llama3.1 | format_constrained | 10  | 0.356    | 0.990    | 1.075     | 0.669    | 0.957  | 0.469      |
| 1.0 | mistral  | baseline           | 10  | 0.403    | 0.990    | 0.824     | 0.428    | 0.989  | 0.411      |
| 1.0 | mistral  | few_shot           | 10  | **1.000**| 0.990    | -0.000    | 0.000    | 1.000  | **0.000**  |
| 1.0 | mistral  | format_constrained | 0   | N/A      | N/A      | N/A       | N/A      | N/A    | N/A        |

### Cross-model comparison @ temp=0.7 (with gpt-oss)

| Model    | Prompt              | N   | Fleiss κ | Kripp α | Shannon H | Mean σ | Cosine | Lev    |
|----------|---------------------|-----|----------|---------|-----------|--------|--------|--------|
| mistral  | baseline            | 10  | 0.512    | 0.990   | 0.695     | 0.366  | 0.989  | 0.342  |
| mistral  | few_shot            | 10  | **1.000**| 0.990   | -0.000    | 0.000  | 1.000  | **0.000** |
| mistral  | format_constrained* | 9   | 0.383    | 0.990   | 0.755     | 0.452  | —      | —      |
| llama3.1 | baseline            | 10  | 0.537    | 0.990   | 0.822     | 0.561  | 0.959  | 0.293  |
| llama3.1 | few_shot            | 10  | 0.467    | 0.990   | 0.883     | 0.739  | 0.946  | 0.307  |
| llama3.1 | format_constrained* | 9   | 0.372    | 0.990   | 0.806     | 0.524  | —      | —      |
| gpt-oss  | baseline            | 10  | 0.509    | 0.990   | 0.702     | 0.352  | 0.988  | 0.356  |
| gpt-oss  | few_shot            | 10  | **0.798**| 0.990   | 0.288     | 0.159  | 0.995  | 0.144  |
| gpt-oss  | format_constrained* | 10  | 0.715    | 0.990   | 0.456     | 0.241  | —      | —      |

\* `format_constrained` używa nowej wersji promptu (lista pytań bez numerów); patrz `docs/final_report.md` sekcja 9.

### Ranking konfiguracji (Fleiss κ, temp=0.7, im wyżej tym stabilniej)

1. **mistral + few_shot** — κ = 1.000
2. **gpt-oss + few_shot** — κ = 0.798
3. **gpt-oss + format_constrained** — κ = 0.715
4. llama3.1 + baseline — κ = 0.537
5. mistral + baseline — κ = 0.512
6. gpt-oss + baseline — κ = 0.509
7. llama3.1 + few_shot — κ = 0.467
8. mistral + format_constrained — κ = 0.383
9. llama3.1 + format_constrained — κ = 0.372

### Średnia Fleiss κ per typ promptu (uśredniona po modelach × temperaturach)

| Prompt | Mean κ | n konfiguracji |
|--------|-------:|-------:|
| **few_shot** | **0.803** | 12 |
| baseline | 0.563 | 12 |
| format_constrained | 0.489 | 12 |

## Wnioski (Conclusions)

### 🏆 Który prompt wygrywa?

**Few-shot** jest jednoznacznie najbardziej stabilną strategią — średnia Fleiss κ = **0.803** vs 0.563 (baseline) i 0.489 (format-constrained). Spośród 9 udanych konfiguracji, dwa pierwsze miejsca w rankingu zajmuje few-shot (mistral κ=1.0, gpt-oss κ=0.798). Mechanizm: kotwiczenie odpowiedzi przykładami (`"outgoing" → 4`, `"cold" → 2`, `"reliable" → 5`) drastycznie ogranicza przestrzeń możliwych interpretacji skali Likerta i wymusza powtarzalność.

**Wyjątek — Llama 3.1:** few-shot pogarsza stabilność (0.537 → 0.467). Hipoteza: większa pojemność modelu pozwala na bardziej "kreatywną" interpretację przykładów, podczas gdy mniejszy Mistral po prostu kopiuje wzorzec. Wniosek praktyczny: **few-shot warto zwalidować empirycznie dla każdego modelu — nie jest to bezwarunkowo lepsza strategia**.

### Hipoteza główna: potwierdzona

Wariancja w sformułowaniu promptu **istotnie wpływa** na stabilność. Różnica κ między najlepszym (1.000) a najgorszym (0.467) promptem dla tego samego modelu (Mistral baseline vs few_shot) to **0.488** — zmiana z "umiarkowanej zgodności" na "perfekcyjną". Rekomendacja produkcyjna: w aplikacjach wymagających spójności (rekrutacja, ocena osobowości, mental health) używać few-shot z walidacją per model.

### 1. Wpływ few-shot na stabilność

- **Mistral + few-shot**: Perfekcyjna stabilność (κ=1.0) niezależnie od temperatury
- **Llama3.1 + few-shot**: Wysoka stabilność przy niskiej temperaturze (κ=1.0 przy temp=0.3), ale spada przy wyższej (κ=0.374 przy temp=1.0)

### 2. Wpływ temperatury na stabilność (baseline)

| Model   | temp=0.3 | temp=0.5 | temp=0.7 | temp=1.0 |
|---------|----------|----------|----------|----------|
| mistral | 0.751   | 0.601    | 0.512    | 0.403    |
| llama3.1| 0.803   | 0.770    | 0.537    | 0.477    |

- **Niższa temperatura = wyższa stabilność** - wniosek potwierdzony dla obu modeli
- Llama3.1 jest bardziej wrażliwy na zmiany temperatury niż Mistral

### 3. Format-constrained

- **Mistral**: Całkowita porażka (0% sukcesu) - model zwraca liczby spoza zakresu 1-5 (np. "5,2,4,4,5,6,7,8,9,3")
- **Llama3.1**: 100% sukces w parsowaniu, ale niska stabilność (κ=0.356-0.486)

### 4. Metryki Krippendorff α

- Wszystkie konfiguracje z ≥1 poprawną odpowiedzią osiągają α≈0.99
- Wskazuje to na wysoką "zgodność wewnętrzną" między powtórzeniami, ale niekoniecznie na poprawność odpowiedzi

### 5. Rekomendacje praktyczne

| Cel | Model | Prompt | Temperature |
|-----|-------|--------|-------------|
| Maksymalna powtarzalność | Mistral | few-shot | dowolna (0.3-1.0) |
| Wysoka powtarzalność + bezpieczne | Llama3.1 | few-shot | 0.3 |
| Minimalna zmienność | dowolny | few-shot | 0.3 |

## Metric Definitions

| Metric | Range | Interpretation |
|--------|-------|----------------|
| Fleiss κ | -1 to 1 | 1 = perfect agreement |
| Krippendorff α | 0 to 1 | 1 = perfect reliability |
| Mean Std | 0 to ~1.5 | 0 = no variance |
| Levenshtein | 0 to 1 | 0 = identical strings |
| Cosine Sim | -1 to 1 | 1 = identical vectors |

## Raw Data

See result files (in `results/`):
- `results/results.json` (mistral + llama3.1, temp=0.7)
- `results/results_gpt_oss.json` (gpt-oss-20b, temp=0.7)
- `results/results_tmptr_5.json` (temp=0.5)
- `results/results_tmptr_3.json` (temp=0.3)
- `results/results_tmptr_10.json` (temp=1.0)
