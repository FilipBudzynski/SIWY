from enum import Enum
from abc import ABC, abstractmethod


class ModelName(Enum):
    CHATGPT = "gpt-3.5-turbo"
    MISTRAL = "mistral"
    LLAMA = "llama3.1"


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
    else:
        raise ValueError(f"Unknown model: {model_name}")
