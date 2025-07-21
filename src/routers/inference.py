from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..model.sentiment import ternary_analysis

router = APIRouter(
    prefix="/model",
    tags=["sentiment"]
)

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: int

@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    try:
        sentiment = ternary_analysis(request.text)
        return SentimentResponse(
            text=request.text,
            sentiment=sentiment
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        )