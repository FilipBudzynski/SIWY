import re
from typing import Optional


def parse_ratings(response: str) -> Optional[list[int]]:
    response = response.strip()
    
    if "," in response and all(c in "0123456789,- " for c in response.replace(" ", "")):
        numbers = re.findall(r'\d+', response.replace(" ", ""))
        valid = [int(n) for n in numbers if 1 <= int(n) <= 5]
        if len(valid) >= 10:
            return valid[:10]
    
    pattern = r'(?:^|\n)(\d+)[:.\s]+([1-5])'
    matches = re.findall(pattern, response)
    if len(matches) >= 10:
        return [int(m[1]) for m in matches[:10]]
    
    numbers = re.findall(r'\b([1-5])\b', response)
    if len(numbers) >= 10:
        return [int(n) for n in numbers[:10]]
    
    return None
