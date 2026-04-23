from enum import Enum
from siwy.prompts.bfi10 import BFI10_QUESTIONS, questions_to_text, reverse_score


class PromptType(Enum):
    BASELINE = "baseline"
    FEW_SHOT = "few_shot"
    FORMAT_CONSTRAINED = "format_constrained"


_questions_text = questions_to_text()

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


FORMAT_CONSTRAINED_PROMPT = """Answer the 10 questions below. For each question, give a rating from 1 to 5 where:
1 = Disagree strongly
2 = Disagree
3 = Neutral
4 = Agree
5 = Agree strongly

{questions}

Respond with EXACTLY 10 numbers, one for each question, separated by commas.
Example valid response: 4,3,5,2,4,3,5,2,4,3
Your response (10 numbers only, no other text):"""


def get_prompt(prompt_type: PromptType) -> str:
    prompt = {
        PromptType.BASELINE: BASELINE_PROMPT,
        PromptType.FEW_SHOT: FEW_SHOT_PROMPT,
        PromptType.FORMAT_CONSTRAINED: FORMAT_CONSTRAINED_PROMPT,
    }[prompt_type]
    return prompt.format(questions=_questions_text)
