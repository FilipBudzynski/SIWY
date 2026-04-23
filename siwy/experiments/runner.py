from datetime import datetime
from itertools import product
from typing import Generator
from siwy.data.schema import ExperimentConfig, ExperimentResult
from siwy.models.loader import Model, load_model, ModelName
from siwy.prompts.templates import PromptType, get_prompt
from siwy.inference.parser import parse_ratings


class ExperimentRunner:
    def __init__(
        self,
        models: list[ModelName] = list(ModelName),
        prompt_types: list[PromptType] = list(PromptType),
        repetitions: int = 10,
        temperature: float = 0.7,
        base_seed: int = 42,
    ):
        self.models = models
        self.prompt_types = prompt_types
        self.repetitions = repetitions
        self.temperature = temperature
        self.base_seed = base_seed
        self._loaded_models: dict[ModelName, Model] = {}

    def _get_model(self, model_name: ModelName) -> Model:
        if model_name not in self._loaded_models:
            self._loaded_models[model_name] = load_model(model_name)
        return self._loaded_models[model_name]

    def run_single(
        self,
        model_name: ModelName,
        prompt_type: PromptType,
        repetition: int,
        seed: int,
    ) -> ExperimentResult:
        model = self._get_model(model_name)
        prompt = get_prompt(prompt_type)
        raw_response = model.generate(prompt, temperature=self.temperature, seed=seed)
        parsed_ratings = parse_ratings(raw_response)
        
        return ExperimentResult(
            model_name=model_name.value,
            prompt_type=prompt_type.value,
            repetition=repetition,
            timestamp=datetime.now(),
            raw_response=raw_response,
            parsed_ratings=parsed_ratings,
            parse_success=parsed_ratings is not None,
            seed=seed,
        )

    def run_all(self) -> Generator[ExperimentResult, None, None]:
        for model, prompt in product(self.models, self.prompt_types):
            for rep in range(self.repetitions):
                seed = self.base_seed + rep
                result = self.run_single(model, prompt, rep, seed=seed)
                yield result
                print(f"Done: {model.value} | {prompt.value} | rep {rep}")
