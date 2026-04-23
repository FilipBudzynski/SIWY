import numpy as np
from dataclasses import dataclass


@dataclass
class StabilityMetrics:
    fleiss_kappa: float
    krippendorff_alpha: float
    shannon_entropy: float
    std_per_question: list[float]
    mean_std: float


def _parse_nominal(data: list[list[int]]) -> np.ndarray:
    ratings = np.array(data)
    n_questions = ratings.shape[1]
    n_raters = ratings.shape[0]
    categories = 5
    matrix = np.zeros((n_questions, categories))
    for q in range(n_questions):
        for r in range(n_raters):
            cat = ratings[r, q] - 1
            if 0 <= cat < categories:
                matrix[q, cat] += 1
    return matrix


def fleiss_kappa(data: list[list[int]]) -> float:
    matrix = _parse_nominal(data)
    n_questions, n_categories = matrix.shape
    n_raters = matrix.sum(axis=1)[0]
    n_total = matrix.sum()
    
    p_j = matrix.sum(axis=0) / n_total
    p_e = (p_j ** 2).sum()
    
    P_bar = (matrix ** 2).sum(axis=1) - matrix.sum(axis=1)
    P_bar = P_bar / (n_raters * (n_raters - 1))
    P_bar_mean = P_bar.mean()
    
    if 1 - p_e == 0:
        return 1.0
    return (P_bar_mean - p_e) / (1 - p_e)


def krippendorff_alpha(data: list[list[int]]) -> float:
    ratings = np.array(data).astype(float)
    n_raters, n_questions = ratings.shape
    mask = ~np.isnan(ratings)
    observed = ratings[mask]
    n_total = len(observed)
    
    if n_total < 2:
        return 1.0
    
    Do = np.sum((observed[:, None] - observed) ** 2) / (n_total * (n_total - 1))
    
    all_values = observed.flatten()
    unique_vals = np.unique(all_values)
    Dc = 0
    for val in unique_vals:
        count = np.sum(all_values == val)
        Dc += count * (val - all_values.mean()) ** 2
    Dc = 2 * Dc / (n_total * (n_total - 1)) if n_total > 1 else 0
    
    if Do == 0:
        return 1.0
    return 1 - Dc / Do


def shannon_entropy(data: list[list[int]]) -> float:
    ratings = np.array(data)
    total_entropy = 0.0
    for q in range(ratings.shape[1]):
        values, counts = np.unique(ratings[:, q], return_counts=True)
        probs = counts / counts.sum()
        total_entropy -= np.sum(probs * np.log2(probs + 1e-10))
    return total_entropy / ratings.shape[1]


def std_per_question(data: list[list[int]]) -> tuple[list[float], float]:
    ratings = np.array(data)
    stds = [np.std(ratings[:, q]) for q in range(ratings.shape[1])]
    return stds, np.mean(stds)


def compute_stability_metrics(data: list[list[int]]) -> StabilityMetrics:
    stds, mean_std = std_per_question(data)
    return StabilityMetrics(
        fleiss_kappa=fleiss_kappa(data),
        krippendorff_alpha=krippendorff_alpha(data),
        shannon_entropy=shannon_entropy(data),
        std_per_question=stds,
        mean_std=mean_std,
    )
