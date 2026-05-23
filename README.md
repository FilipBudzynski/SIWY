# SIWY - Wpływ promptów na stabilność cech zachowania w LLM

## Struktura projektu

```
siwy/
├── prompts/         # Kwestionariusz BFI-10 i szablony promptów
├── models/          # Ładowanie modeli (ChatGPT, Mistral, Llama)
├── inference/       # Parsowanie odpowiedzi modelu
├── experiments/     # Runner eksperymentów i agregacja metryk
├── metrics/         # Metryki stabilności i semantyczne
├── data/            # Schematy danych
tests/               # Testy jednostkowe
results/             # Surowe wyniki eksperymentów (JSON)
docs/                # Dokumentacja i raport z eksperymentów
pyproject.toml
```

## Użycie

```bash
uv sync
uv run python -m siwy.experiments.run            # zapisze do results/results.json
uv run python -m siwy.experiments.run results/my_run.json
uv run pytest
```

## Metryki

- **Fleiss' κ** - zgodność między powtórzeniami
- **Krippendorff α** - uogólnienie kappa
- **Entropia Shannona** - niepewność odpowiedzi
- **Odchylenie standardowe** - stabilność per pytanie
- **Cosine similarity** - podobieństwo semantyczne
- **Levenshtein** - odległość edycyjna

## Modele i prompty

- Modele: Mistral 7B (Ollama), Llama 3.1 8B (Ollama), gpt-oss-20b (OpenRouter free tier)
- Prompty: baseline, few-shot, format-constrained

## Wyniki

Pełny raport końcowy z wykresami: **[`docs/final_report.md`](docs/final_report.md)**

TL;DR: **few-shot + niska temperatura wygrywa.** Najlepsza konfiguracja: `mistral + few_shot @ T=0.3` → Fleiss κ = 1.000.

## Generowanie wykresów

```bash
uv run python -m siwy.experiments.visualize
# → results/plots/{01_temperature_effect,02_prompt_effect,03_ranking}.png
```

## Dostawcy modeli

- **Ollama** (lokalnie): `ollama pull mistral && ollama pull llama3.1`
- **OpenRouter** (zdalnie, free tier): `export OPENROUTER_API_KEY=sk-or-v1-...`
