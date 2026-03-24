# Design Proposal

Autorzy:

- Filip Budzyński, 319021
- Dawid Budzyński, 319020

## Spis treści

1. [Opis problemu](#1-opis-problemu)
2. [Hipoteza badawcza](#2-hipoteza-badawcza)
3. [Cel projektu](#3-cel-projektu)
4. [Metody i narzędzia](#4-metody-i-narzędzia)
5. [Zestaw danych](#5-zestaw-danych)
6. [Metryki oceny](#6-metryki-oceny)
7. [Plan pracy](#7-plan-pracy)
8. [Analiza ryzyka](#8-analiza-ryzyka)
9. [Podsumowanie](#9-podsumowanie)
10. [Oczekiwane wyniki](#10-oczekiwane-wyniki)
11. [Bibliografia](#11-bibliografia)

---

## 1. Opis problemu

### 1.1 Temat projektu

**Wpływ promptów na stabilność cech zachowania w modelach językowych: analiza powtarzalności odpowiedzi w testach osobowości**

### 1.2 Motywacja

Modele językowe są coraz częściej wykorzystywane w aplikacjach wymagających spójnego zachowania, takich jak:

- Asystenci AI w dziedzinie zdrowia psychicznego
- Narzędzia do rekrutacji i oceny osobowości
- Interaktywne systemy edukacyjne

Niestabilność odpowiedzi może prowadzić do niespójnych rekomendacji, błędnych ocen lub utraty zaufania użytkowników. Zrozumienie, jak prompt engineering wpływa na powtarzalność zachowań, jest kluczowe dla odpowiedzialnego wdrażania LLM.

### 1.3 Kontekst XAI

Projekt wpisuje się w obszar Wyjaśnialnej Sztucznej Inteligencji poprzez:

- Analizę wpływu wejść (promptów) na wyjścia modelu
- Identyfikację, które elementy promptu najsilniej wpływają na zmienność odpowiedzi
- Oferowanie wglądu w mechanizmy zachowania modeli językowych

---

## 2. Hipoteza badawcza

**Hipoteza główna:** Wariancja w sformułowaniu promptów (struktura, instrukcje, kontekst) istotnie wpływa na zmienność odpowiedzi udzielanych przez LLM w testach osobowości.

---

## 3. Cel projektu

### 3.1 Cel główny

Celem projektu jest zbadanie i kwantyfikacja wpływu różnych strategii promptowania na stabilność wyników testów osobowościowych w dużych modelach językowych, oraz opracowanie wytycznych dotyczących optymalnego konstruowania promptów dla zastosowań wymagających spójnego zachowania.

### 3.2 Cele szczegółowe

1. Zidentyfikowanie i klasyfikacja typów promptów wpływających na zmienność odpowiedzi
2. Porównanie stabilności wybranych modeli językowych w testach osobowości
3. Opracowanie metryk oceny powtarzalności odpowiedzi w kontekście testów osobowości
4. Analiza statystyczna zależności między cechami promptów a stabilnością wyników
5. Stworzenie rekomendacji praktycznych dla developerów aplikacji wykorzystujących LLM

### 3.3 Kryteria sukcesu

- Opracowanie działającego pipeline'u badawczego
- Wykazanie istotności statystycznej dla hipotezy głównej
- Dokumentacja wyników w formie raportu

---

## 4. Metody i narzędzia

### 4.1 Język programowania

- **Python 3.11+**

### 4.2 Środowisko zarządzania pakietami

- **uv** - szybkie narzędzie do zarządzania środowiskiem Python

### 4.3 Główne biblioteki

| Biblioteka               | Wersja    | Zastosowanie                          |
| ------------------------ | --------- | ------------------------------------- |
| `transformers`           | 4.40+     | Ładowanie i inferencja modeli         |
| `torch`                  | 2.3+      | Framework głębokiego uczenia          |
| `openai`                 | 1.0+      | API dla ChatGPT                       |
| `ollama`                 | 0.1+      | Lokalna inferencja modeli open-source |
| `pandas`                 | 2.2+      | Analiza danych                        |
| `numpy`                  | 1.26+     | Operacje numeryczne                   |
| `scipy`                  | 1.13+     | Testy statystyczne                    |
| `scikit-learn`           | 1.5+      | Metryki powtarzalności                |
| `sentence-transformers`  | 2.5+      | Embeddingi semantyczne                |
| `matplotlib` / `seaborn` | najnowsza | Wizualizacja wyników                  |
| `pytest`                 | 8+        | Testy jednostkowe                     |
| `black`                  | najnowsza | Formatowanie kodu                     |
| `ruff`                   | najnowsza | Linting                               |

### 4.4 Modele językowe

| Model                       | Parametry | Licencja     | Uwagi                   |
| --------------------------- | --------- | ------------ | ----------------------- |
| **ChatGPT (GPT-3.5-turbo)** | ~175B     | OpenAI Terms | Najpopularniejszy model |
| **Mistral 7B Instruct**     | 7B        | Apache 2.0   | Wysoka wydajność        |
| **Llama 3.1 8B Instruct**   | 8B        | Llama 3.1    | Duża społeczność        |

---

## 5. Zestaw danych

### 5.1 Test osobowości: BFI-10

Wykorzystujemy **BFI-10 (Big Five Inventory - 10 item)** - skróconą wersję narzędzia do pomiaru Wielkiej Piątki cech osobowości.

| Wymiar       | Pozycje | Przykładowe stwierdzenie                             |
| ------------ | ------- | ---------------------------------------------------- |
| Ekstrawersja | 2       | "I see myself as someone who is talkative..."        |
| Ugodowość    | 2       | "I see myself as someone who has a forgiving nature" |
| Sumienność   | 2       | "I see myself as someone who does a thorough job"    |
| Neurotyzm    | 2       | "I see myself as someone who can be moody"           |
| Otwartość    | 2       | "I see myself as someone who is original..."         |

**Skala Likerta 1-5:** Disagree strongly → Agree strongly

### 5.2 Struktura eksperymentu

```
Eksperyment = {
    model: ModelName,
    prompt_type: PromptType,
    repetitions: int,
    seed: int
}

Parametry stałe:
- temperature = 0.7

Parametry zmienne:
- ModelName ∈ {ChatGPT, Mistral, Llama}
- PromptType ∈ {baseline, few_shot, format_constrained}
- repetitions ∈ {10}
```

### 5.3 Przykładowe prompty

#### 5.3.1 Baseline (zero-shot)

```
[SYSTEM]
You are a thoughtful person completing a personality questionnaire.

[QUESTIONS]
1. I see myself as someone who is talkative, talkative.
2. I see myself as someone who tends to find fault with others.
3. I see myself as someone who does a thorough job.
4. I see myself as someone who gets nervous easily.
5. I see myself as someone who has an active imagination.
6. I see myself as someone who is original, comes up with new ideas.
7. I see myself as someone who has a forgiving nature.
8. I see myself as someone who tends to be lazy.
9. I see myself as someone who is relaxed, handles stress well.
10. I see myself as someone who has few artistic interests.

[INSTRUCTION]
Rate each statement 1-5 (1=Disagree strongly, 5=Agree strongly).
Format: 1: [rating], 2: [rating], ... 10: [rating]
```

#### 5.3.2 Few-shot

```
[SYSTEM]
You are a thoughtful person completing a personality questionnaire.

[EXAMPLES]
- "I see myself as someone who is outgoing" → 4
- "I see myself as someone who can be cold" → 2
- "I see myself as someone who is reliable" → 5

[QUESTIONS]
1-10. (jak wyżej)

[INSTRUCTION]
Rate each statement using the scale 1-5.
```

#### 5.3.3 Format-constrained

```
[SYSTEM]
You are completing a personality questionnaire.

[QUESTIONS]
1-10. (jak wyżej)

[INSTRUCTION]
CRITICAL: Respond with ONLY a comma-separated list of numbers.
Format: "1,2,3,4,5,6,7,8,9,10"
```

---

## 6. Metryki oceny

### 6.1 Metryki stabilności

| Metryka                    | Opis                                                                |
| -------------------------- | ------------------------------------------------------------------- |
| **Fleiss' κ**              | Zgodność między powtórzeniami. Zakres: -1 do 1 (1 = pełna zgodność) |
| **Alpha Krippendorffa**    | Uogólnienie kappa dla dowolnej liczby powtórzeń                     |
| **Entropia Shannona**      | Miara niepewności. Niższa = wyższa stabilność                       |
| **Odchylenie standardowe** | Niższe = wyższa stabilność                                          |

### 6.2 Metryki semantyczne

| Metryka                  | Opis                                             |
| ------------------------ | ------------------------------------------------ |
| **Cosine Similarity**    | Porównanie semantycznego podobieństwa odpowiedzi |
| **Levenshtein Distance** | Odległość edycyjna między odpowiedziami          |

### 6.3 Metryki odzwierciedlania osobowości

Dodatkowo badamy, czy modele poprawnie odzwierciedlają przypisaną im osobowość. Proces:

1. Przypisanie modelowi określonego profilu osobowości (np. "wysoka ekstrawersja, niski neurotyzm")
2. Porównanie wyników BFI-10 z oczekiwanym profilem

---

## 7. Plan pracy

### 7.1 Tabela przeglądowa

| Tydzień | Daty          | Główne zadania              | Osoba         |
| ------- | ------------- | --------------------------- | ------------- |
| 1       | 30.03 - 05.04 | Setup, prompty, BFI-10      | Filip + Dawid |
| 2       | 06.04 - 12.04 | Pipeline modeli + testy     | Filip + Dawid |
| 3       | 13.04 - 19.04 | Pipeline metryk + testy     | Filip + Dawid |
| 4       | 20.04 - 26.04 | Eksperymenty + metryki      | Filip + Dawid |
| 5       | 27.04 - 03.05 | Eksperymenty + konsolidacja | Filip + Dawid |
| 6       | 04.05 - 10.05 | Analiza + wykresy           | Filip + Dawid |
| 7       | 11.05 - 17.05 | Dokumentacja                | Filip + Dawid |
| 8       | 18.05 - 21.05 | Prezentacja                 | Filip + Dawid |

### 7.2 Szczegółowy podział

#### Tydzień 1: Setup

| Zadanie | Opis                                  | Osoba |
| ------- | ------------------------------------- | ----- |
| 1.1     | Repozytorium, uv, black, ruff, pytest | Filip |
| 1.2     | Kwestionariusz BFI-10                 | Dawid |
| 1.3     | Szablony promptów                     | Dawid |
| 1.4     | Schemat zbierania danych              | Filip |

#### Tydzień 2: Pipeline modeli

| Zadanie | Opis                   | Osoba |
| ------- | ---------------------- | ----- |
| 2.1     | Moduł ładowania modeli | Filip |
| 2.2     | Moduł inferencji       | Dawid |
| 2.3     | ExperimentRunner       | Filip |
| 2.4     | Testy jednostkowe      | Dawid |

#### Tydzień 3: Pipeline metryk

| Zadanie | Opis                      | Osoba |
| ------- | ------------------------- | ----- |
| 3.1     | Moduł metryk stabilności  | Dawid |
| 3.2     | Integracja z pipeline     | Filip |
| 3.3     | Testy jednostkowe metryk  | Dawid |
| 3.4     | Walidacja na małej próbce | Filip |

#### Tydzień 4: Eksperymenty - część 1

| Zadanie | Opis                 | Osoba |
| ------- | -------------------- | ----- |
| 4.1     | Eksperymenty ChatGPT | Filip |
| 4.2     | Eksperymenty Mistral | Dawid |
| 4.3     | Obliczanie metryk    | Filip |

#### Tydzień 5: Eksperymenty - część 2

| Zadanie | Opis                | Osoba |
| ------- | ------------------- | ----- |
| 5.1     | Eksperymenty Llama  | Dawid |
| 5.2     | Obliczanie metryk   | Filip |
| 5.3     | Konsolidacja danych | Dawid |

#### Tydzień 6: Analiza statystyczna

| Zadanie | Opis                 | Osoba |
| ------- | -------------------- | ----- |
| 6.1     | Testy statystyczne   | Filip |
| 6.2     | Generowanie wykresów | Dawid |
| 6.3     | Analiza korelacji    | Filip |

#### Tydzień 7: Dokumentacja

| Zadanie | Opis                    | Osoba |
| ------- | ----------------------- | ----- |
| 7.1     | Sprawozdanie            | Filip |
| 7.2     | Dokumentacja techniczna | Dawid |
| 7.3     | README                  | Filip |

#### Tydzień 8: Prezentacja

| Zadanie | Opis              | Osoba         |
| ------- | ----------------- | ------------- |
| 8.1     | Slajdy            | Filip + Dawid |
| 8.2     | Demo              | Dawid         |
| 8.3     | Próba prezentacji | Filip + Dawid |
| 8.4     | Finalne poprawki  | Filip         |

---

## 8. Analiza ryzyka

| Ryzyko                        | Prawdopodobieństwo | Waga | Minimalizacja ryzyka          |
| ----------------------------- | ------------------ | ---- | ----------------------------- |
| Modele nie mieszczą się w RAM | Ś                  | W    | Quantization, mniejsze modele |
| Czas inferencji zbyt długi    | W                  | Ś    | Równoległe przetwarzanie      |
| Błędy w parsowaniu odpowiedzi | W                  | Ś    | Robust parsing                |
| Brak istotności statystycznej | N                  | W    | Duża próbka                   |
| Opóźnienia w harmonogramie    | Ś                  | Ś    | Bufory czasowe                |

N - niskie
Ś - średnie
W - wysokie

---

## 9. Podsumowanie

Projekt bada wpływ promptów na stabilność wyników testów osobowościowych w LLM. Wykorzystując 3 modele (ChatGPT, Mistral 7B, Llama 3.1 8B), kwestionariusz BFI-10 oraz trzy strategie promptowania, przeprowadzone zostaną systematyczne eksperymenty z metrykami obliczanymi na bieżąco.

---

## 10. Oczekiwane wyniki

1. Ilościowa charakterystyka stabilności dla każdej kombinacji model-prompt
2. Ranking modeli według stabilności
3. Rekomendacje dotyczące promptowania
4. Wykresy i wizualizacje
5. Raport dokumentujący metodologię i wyniki

---

## 11. Bibliografia

1. Brown, T. B., et al. (2020). "Language Models are Few-Shot Learners." _NeurIPS 2020_. <https://arxiv.org/abs/2005.14165>

2. Huang, J., et al. (2023). "Revisiting the Reliability of Psychological Scales on Large Language Models." _arXiv_. <https://arxiv.org/abs/2305.19926>

3. Rammstedt, B., & John, O. P. (2007). "Measuring personality in one minute or less." _Journal of Research in Personality_, 41(1), 203-212. <https://doi.org/10.1016/j.jrp.2006.02.001>

4. Serapio-García, G., et al. (2023). "Personality Traits in Large Language Models." _arXiv_. <https://arxiv.org/abs/2307.00184>

5. Shu, B., et al. (2023). "You don't need a personality test to know these models are unreliable." _arXiv_. <https://arxiv.org/abs/2311.09718>
