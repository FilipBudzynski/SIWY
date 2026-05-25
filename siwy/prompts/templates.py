from enum import Enum
from siwy.prompts.bfi10 import BFI10_QUESTIONS, questions_to_text, reverse_score


class PromptType(Enum):
    BASELINE = "baseline"
    FEW_SHOT = "few_shot"
    FORMAT_CONSTRAINED = "format_constrained"


_questions_text = questions_to_text()
_questions_text_unnumbered = questions_to_text(numbered=False)

BASELINE_PROMPT = """[SYSTEM]
You are a thoughtful person completing a personality questionnaire.

[QUESTIONS]
{questions}

[INSTRUCTION]
Rate each statement 1-5 (1=Disagree strongly, 5=Agree strongly).
Format: 1: [rating], 2: [rating], ... 10: [rating]"""


FEW_SHOT_PROMPT = """[SYSTEM]
You are a thoughtful person completing a personality questionnaire.

[EXAMPLES]
- "I see myself as someone who is outgoing" → 4
- "I see myself as someone who can be cold" → 2
- "I see myself as someone who is reliable" → 5

[QUESTIONS]
{questions}

[INSTRUCTION]
Rate each statement using the scale 1-5.
Format: 1: [rating], 2: [rating], ... 10: [rating]"""


# Bullet-list questions (no numeric labels) — prevents small models
# from echoing the input numbering sequence (1..10) into the output.
FORMAT_CONSTRAINED_PROMPT = """You are completing a personality questionnaire.
Scale: 1=Disagree strongly, 2=Disagree, 3=Neutral, 4=Agree, 5=Agree strongly.

Statements:
{questions}

Output exactly 10 ratings (each 1-5), separated by commas. No other text.

Answer:"""


def get_prompt(prompt_type: PromptType) -> str:
    if prompt_type == PromptType.FORMAT_CONSTRAINED:
        return FORMAT_CONSTRAINED_PROMPT.format(questions=_questions_text_unnumbered)
    prompt = {
        PromptType.BASELINE: BASELINE_PROMPT,
        PromptType.FEW_SHOT: FEW_SHOT_PROMPT,
    }[prompt_type]
    return prompt.format(questions=_questions_text)
