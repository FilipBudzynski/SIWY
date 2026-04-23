import json
from siwy.experiments.runner import ExperimentRunner
from siwy.experiments.aggregate import aggregate_results
from siwy.models.loader import ModelName
from siwy.prompts.templates import PromptType


def run_experiments(
    output_path: str = "results.json",
    models: list[ModelName] | None = None,
    prompt_types: list[PromptType] | None = None,
    repetitions: int = 10,
    temperature: float = 1.0,
    base_seed: int = 42,
):
    if models is None:
        models = [ModelName.MISTRAL, ModelName.LLAMA]
    if prompt_types is None:
        prompt_types = list(PromptType)
    
    runner = ExperimentRunner(
        models=models,
        prompt_types=prompt_types,
        repetitions=repetitions,
        temperature=temperature,
        base_seed=base_seed,
    )
    
    results = list(runner.run_all())
    
    with open(output_path, "w") as f:
        json.dump(
            [
                {
                    "model_name": r.model_name,
                    "prompt_type": r.prompt_type,
                    "repetition": r.repetition,
                    "raw_response": r.raw_response,
                    "parsed_ratings": r.parsed_ratings,
                    "parse_success": r.parse_success,
                    "seed": r.seed,
                    "temperature": temperature,
                }
                for r in results
            ],
            f,
            indent=2,
        )
    
    grouped = {}
    for r in results:
        key = (r.model_name, r.prompt_type)
        grouped.setdefault(key, []).append(r)
    
    aggregated = {}
    for key, group_results in grouped.items():
        agg = aggregate_results(group_results)
        agg.temperature = temperature
        aggregated[key] = agg
    
    summary_path = output_path.replace(".json", "_summary.json")
    with open(summary_path, "w") as f:
        json.dump(
            {f"{k[0]}_{k[1]}": vars(v) for k, v in aggregated.items()},
            f,
            indent=2,
        )
    
    print(f"Results saved to {output_path}")
    return aggregated


if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    run_experiments(output)
