from pydantic import BaseModel
from typing import Dict, List

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: int

# Pydantic models for request/response
class MCQ(BaseModel):
    number: int
    question: str
    options: Dict[str, str]
    correct_answer: str

class MCQRequest(BaseModel):
    skill_name: str
    skill_level: float
    num_questions: int = 10

class MCQResponse(BaseModel):
    skill_name: str
    skill_level: float
    questions: List[MCQ]
