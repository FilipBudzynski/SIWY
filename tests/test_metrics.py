import pytest
import numpy as np
from siwy.metrics.stability import (
    fleiss_kappa, krippendorff_alpha, shannon_entropy, std_per_question
)
from siwy.metrics.semantic import levenshtein_distance, normalize_levenshtein, cosine_similarity_simple


def test_fleiss_kappa_perfect():
    data = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3] for _ in range(10)]
    assert fleiss_kappa(data) == 1.0


def test_fleiss_kappa_random():
    data = [[np.random.randint(1, 6) for _ in range(10)] for _ in range(10)]
    kappa = fleiss_kappa(data)
    assert -1 <= kappa <= 1


def test_shannon_entropy():
    data = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5] for _ in range(10)]
    assert shannon_entropy(data) < 0.1


def test_std_per_question():
    data = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3] for _ in range(10)]
    stds, mean_std = std_per_question(data)
    assert mean_std < 0.1


def test_levenshtein():
    assert levenshtein_distance("kitten", "sitting") == 3


def test_normalized_levenshtein():
    assert normalize_levenshtein("12345", "12345") == 0.0
    # 4 edits (4 swaps) / 5 = 0.8
    assert normalize_levenshtein("12345", "54321") == 0.8


def test_cosine_similarity():
    assert cosine_similarity_simple([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity_simple([1.0, 0.0], [-1.0, 0.0]) == -1.0
