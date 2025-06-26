import re

def split_text_into_sentences(text: str) -> list[str]:
    """Splits a given text into a list of sentences."""
    # Basic sentence splitting using regex
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
