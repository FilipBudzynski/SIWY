from dataclasses import dataclass


@dataclass
class BFI10Question:
    id: int
    dimension: str
    statement: str
    reverse_scored: bool = False


BFI10_QUESTIONS = [
    BFI10Question(id=1, dimension="Extraversion", 
                  statement="I see myself as someone who is talkative, outgoing."),
    BFI10Question(id=2, dimension="Agreeableness", 
                  statement="I see myself as someone who tends to find fault with others."),
    BFI10Question(id=3, dimension="Conscientiousness", 
                  statement="I see myself as someone who does a thorough job."),
    BFI10Question(id=4, dimension="Neuroticism", 
                  statement="I see myself as someone who gets nervous easily."),
    BFI10Question(id=5, dimension="Openness", 
                  statement="I see myself as someone who has an active imagination."),
    BFI10Question(id=6, dimension="Openness", 
                  statement="I see myself as someone who is original, comes up with new ideas."),
    BFI10Question(id=7, dimension="Agreeableness", 
                  statement="I see myself as someone who has a forgiving nature."),
    BFI10Question(id=8, dimension="Conscientiousness", 
                  statement="I see myself as someone who tends to be lazy.", reverse_scored=True),
    BFI10Question(id=9, dimension="Neuroticism", 
                  statement="I see myself as someone who is relaxed, handles stress well.", 
                  reverse_scored=True),
    BFI10Question(id=10, dimension="Openness", 
                  statement="I see myself as someone who has few artistic interests.", 
                  reverse_scored=True),
]


def get_dimensions() -> dict[str, list[int]]:
    return {
        "Extraversion": [1],
        "Agreeableness": [2, 7],
        "Conscientiousness": [3, 8],
        "Neuroticism": [4, 9],
        "Openness": [5, 6, 10],
    }


def questions_to_text() -> str:
    lines = []
    for q in BFI10_QUESTIONS:
        lines.append(f"{q.id}. {q.statement}")
    return "\n".join(lines)


def reverse_score(value: int) -> int:
    return 6 - value
