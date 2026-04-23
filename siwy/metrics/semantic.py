import numpy as np
from dataclasses import dataclass


@dataclass
class SemanticMetrics:
    mean_cosine: float
    mean_levenshtein: float
    normalized_levenshtein: float


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev[j + 1] + 1
            deletions = curr[j] + 1
            substitutions = prev[j] + (c1 != c2)
            curr.append(min(insertions, deletions, substitutions))
        prev = curr
    return prev[-1]


def normalize_levenshtein(s1: str, s2: str) -> float:
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    return levenshtein_distance(s1, s2) / max_len


def cosine_similarity_simple(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = sum(a * a for a in v1) ** 0.5
    norm2 = sum(b * b for b in v2) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def compute_semantic_metrics(responses: list[list[int]]) -> SemanticMetrics:
    ratings_str = ["".join(map(str, r)) for r in responses]
    
    n = len(ratings_str)
    cosine_sum = 0.0
    lev_sum = 0.0
    pairs = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            cosine_sum += cosine_similarity_simple(
                [float(x) for x in responses[i]],
                [float(x) for x in responses[j]]
            )
            lev_sum += normalize_levenshtein(ratings_str[i], ratings_str[j])
            pairs += 1
    
    norm_lev = lev_sum / pairs if pairs > 0 else 0.0
    
    return SemanticMetrics(
        mean_cosine=cosine_sum / pairs if pairs > 0 else 1.0,
        mean_levenshtein=lev_sum / pairs if pairs > 0 else 0.0,
        normalized_levenshtein=norm_lev,
    )
