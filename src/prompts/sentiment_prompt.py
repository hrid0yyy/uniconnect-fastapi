from langchain.prompts import PromptTemplate
from pydantic import BaseModel

class SentimentResponse(BaseModel):
    sentiment: int  # -1, 0, or 1

sentiment_template = """Analyze the sentiment of the following text and return only a single number.

Text to analyze: {text}

Rules:
Return exactly one number based on these rules:
-1 = negative sentiment (sadness, anger, disappointment)
0 = neutral sentiment (factual, no emotion)
1 = positive sentiment (happiness, satisfaction, praise)

Return only the number (-1, 0, or 1) with no other text."""

sentiment_prompt = PromptTemplate(
    input_variables=["text"],
    template=sentiment_template
)

def parse_sentiment_response(response: str) -> SentimentResponse:
    try:
        sentiment = int(response.content.strip())
        if sentiment not in [-1, 0, 1]:
            raise ValueError
        return SentimentResponse(sentiment=sentiment)
    except ValueError:
        return SentimentResponse(sentiment=0)  # default to neutral