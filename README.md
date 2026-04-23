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
pyproject.toml
```

## Użycie

```bash
uv sync
uv run python -m siwy.experiments.run
```

## Metryki

- **Fleiss' κ** - zgodność między powtórzeniami
- **Krippendorff α** - uogólnienie kappa
- **Entropia Shannona** - niepewność odpowiedzi
- **Odchylenie standardowe** - stabilność per pytanie
- **Cosine similarity** - podobieństwo semantyczne
- **Levenshtein** - odległość edycyjna

## Modele i prompty

- Modele: ChatGPT, Mistral 7B, Llama 3.1 8B
- Prompty: baseline, few-shot, format-constrained
