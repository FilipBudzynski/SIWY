from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExperimentResult:
    model_name: str
    prompt_type: str
    repetition: int
    timestamp: datetime
    raw_response: str
    parsed_ratings: Optional[list[int]]
    parse_success: bool
    seed: int


@dataclass
class ExperimentConfig:
    model: str
    prompt_type: str
    repetitions: int = 10
    temperature: float = 0.7
    seed: int = 42
