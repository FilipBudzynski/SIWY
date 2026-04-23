from dataclasses import dataclass, field
from siwy.data.schema import ExperimentResult
from siwy.metrics.stability import compute_stability_metrics
from siwy.metrics.semantic import compute_semantic_metrics


@dataclass
class AggregatedMetrics:
    model_name: str
    prompt_type: str
    n_successful: int
    stability_fleiss_kappa: float
    stability_krippendorff_alpha: float
    stability_shannon_entropy: float
    stability_mean_std: float
    semantic_cosine: float
    semantic_levenshtein: float
    temperature: float = 0.7


def aggregate_results(results: list[ExperimentResult]) -> AggregatedMetrics:
    successful = [r for r in results if r.parse_success and r.parsed_ratings]
    
    if not successful:
        return AggregatedMetrics(
            model_name=results[0].model_name if results else "unknown",
            prompt_type=results[0].prompt_type if results else "unknown",
            n_successful=0,
            stability_fleiss_kappa=0.0,
            stability_krippendorff_alpha=0.0,
            stability_shannon_entropy=float('inf'),
            stability_mean_std=float('inf'),
            semantic_cosine=0.0,
            semantic_levenshtein=1.0,
        )
    
    ratings_data = [r.parsed_ratings for r in successful]
    
    stability = compute_stability_metrics(ratings_data)
    semantic = compute_semantic_metrics(ratings_data)
    
    return AggregatedMetrics(
        model_name=successful[0].model_name,
        prompt_type=successful[0].prompt_type,
        n_successful=len(successful),
        stability_fleiss_kappa=stability.fleiss_kappa,
        stability_krippendorff_alpha=stability.krippendorff_alpha,
        stability_shannon_entropy=stability.shannon_entropy,
        stability_mean_std=stability.mean_std,
        semantic_cosine=semantic.mean_cosine,
        semantic_levenshtein=semantic.normalized_levenshtein,
    )
