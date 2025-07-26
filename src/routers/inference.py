from fastapi import APIRouter, HTTPException
from ..handler.Sentiment import ternary_analysis
from ..handler.SkillTest import generate_questions
from ..utils.schemas import SentimentRequest, SentimentResponse, MCQ, MCQRequest, MCQResponse

router = APIRouter(
    tags=["sentiment"]
)

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

@router.post("/generate_mcq", response_model=MCQResponse)
async def generate_mcq(request: MCQRequest):
    try:
        if request.skill_level < 1 or request.skill_level > 5:
            raise HTTPException(status_code=400, detail="Skill level must be between 1 and 5")
        if request.num_questions < 1 or request.num_questions > 50:
            raise HTTPException(status_code=400, detail="Number of questions must be between 1 and 50")

        questions = generate_questions(request.skill_name, request.skill_level, request.num_questions)

        pydantic_questions = []
        for q in questions:
            pydantic_questions.append(MCQ(
                number=q.number,
                question=q.question,
                options=q.options,
                correct_answer=q.correct_answer
            ))
        
        return MCQResponse(
            skill_name=request.skill_name,
            skill_level=request.skill_level,
            questions=pydantic_questions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")