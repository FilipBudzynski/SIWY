# Experiment Results: Prompt Stability in LLM Personality Tests

## Methodology

| Parameter | Value |
|----------|-------|
| Models | Mistral 7B Instruct, Llama 3.1 8B Instruct (Ollama) |
| Questionnaire | BFI-10 (Big Five Inventory, 10 items) |
| Prompt types | baseline, few-shot, format_constrained |
| Repetitions | 10 per configuration |
| Temperature | 0.3, 0.5, 0.7, 1.0 |
| Seeds | 42-51 per repetition |

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

## Wnioski (Conclusions)

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

See result files:
- `results.json` (temp=0.7)
- `results_tmptr_5.json` (temp=0.5)
- `results_tmptr_3.json` (temp=0.3)
- `results_tmptr_10.json` (temp=1.0)
