import os
import time
from enum import Enum
from abc import ABC, abstractmethod


class ModelName(Enum):
    CHATGPT = "gpt-3.5-turbo"
    MISTRAL = "mistral"
    LLAMA = "llama3.1"
    GPT_OSS = "gpt-oss"


class Model(ABC):
    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7, seed: int | None = None) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class OpenAIModel(Model):
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: str | None = None):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7, seed: int | None = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def name(self) -> str:
        return self.model_name


class OpenRouterModel(Model):
    def __init__(self, model_id: str, api_key: str | None = None):
        from openai import OpenAI
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError(
                "OPENROUTER_API_KEY not set. Get a free key at https://openrouter.ai/keys "
                "and export OPENROUTER_API_KEY=..."
            )
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
            default_headers={
                "HTTP-Referer": "https://github.com/filip-budzynski/siwy",
                "X-Title": "SIWY BFI-10 stability study",
            },
        )
        self.model_id = model_id

    def generate(self, prompt: str, temperature: float = 0.7, seed: int | None = None) -> str:
        from openai import RateLimitError, APIError

        delay = 4.0
        for attempt in range(6):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=2048,
                )
                if response.choices is None:
                    err = getattr(response, "error", None)
                    raise RuntimeError(f"OpenRouter returned no choices. error={err}")
                return response.choices[0].message.content or ""
            except (RateLimitError, APIError) as e:
                if attempt == 5:
                    raise
                print(f"  [retry {attempt + 1}/5 after {delay:.0f}s] {type(e).__name__}")
                time.sleep(delay)
                delay = min(delay * 2, 60)
        raise RuntimeError("unreachable")

    def name(self) -> str:
        return self.model_id


class OllamaModel(Model):
    def __init__(self, model_name: str):
        import ollama
        self.client = ollama
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7, seed: int | None = None) -> str:
        options = {"temperature": temperature}
        if seed is not None:
            options["seed"] = seed
        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            options=options,
        )
        return response.response

    def name(self) -> str:
        return self.model_name


def load_model(model_name: ModelName) -> Model:
    if model_name == ModelName.CHATGPT:
        return OpenAIModel()
    elif model_name == ModelName.MISTRAL:
        return OllamaModel("mistral")
    elif model_name == ModelName.LLAMA:
        return OllamaModel("llama3.1")
    elif model_name == ModelName.GPT_OSS:
        return OpenRouterModel("openai/gpt-oss-20b:free")
    else:
        raise ValueError(f"Unknown model: {model_name}")
