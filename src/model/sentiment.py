from ..llm.gemini import gemini
from ..prompts.sentiment_prompt import sentiment_template, parse_sentiment_response


def ternary_analysis(text: str) -> int:
    """Perform sentiment analysis on the given text."""
    """Returns -1 for negative, 0 for neutral, 1 for positive sentiment."""
    prompt = sentiment_template.format(text=text)
    response = gemini.invoke(prompt)
    sentiment_response = parse_sentiment_response(response)
    return sentiment_response.sentiment

