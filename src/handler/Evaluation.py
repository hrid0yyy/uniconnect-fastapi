from ..models.llm import groq
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

class NotesScore(BaseModel):
    score: int
class NotesFeedback(BaseModel):
    feedback: str


notesEvaluationTemplate = """Evaluate the following notes based on the criteria provided and return a score between 0 and 100.
Title of the notes: {title}
Subject: {subject}
Tags: {tags}
Content of the notes: {content}
Criteria:
1. Clarity: Is the content clear and easy to understand?
2. Relevance: Does the content relate to the subject and title and tags?
3. Completeness: Does the content cover all necessary points?

Return only the score between 0 to 100. DO NOT ADD ANY OTHER TEXT FOLLOW THIS STRICTLY!
"""

notesFeedbackTemplate = """Evaluate the following notes based on the criteria provided and return a short feedback.
Title of the notes: {title}
Subject: {subject}
Tags: {tags}
Content of the notes: {content}
Criteria:
1. Clarity: Is the content clear and easy to understand?
2. Relevance: Does the content relate to the subject and title and tags?
3. Completeness: Does the content cover all necessary points?

Return only the feedback. DO NOT ADD ANY OTHER TEXT FOLLOW THIS STRICTLY!
"""




def parse_notes_score(response: str) -> NotesScore:
    try:
        score = int(response.content.strip())
        if score < 0 or score > 100:
            raise ValueError
        return NotesScore(score=score)
    except ValueError:
        return NotesScore(score=0) 

def parse_notes_feedback(response: str) -> NotesFeedback:
    try:
        feedback = response.content.strip()
        if not feedback:
            raise ValueError
        return NotesFeedback(feedback=feedback)
    except ValueError:
        return NotesFeedback(feedback="No feedback provided")


def evaluate_notes(metadata):
    """Evaluate the notes based on the given metadata."""
    """Returns a score between 0 and 100."""
    scorePrompt = notesEvaluationTemplate.format(
        title=metadata.get("title"),
        subject=metadata.get("subject"),
        tags=", ".join(metadata.get("tags", [])),
        content=metadata.get("content")
    )
    feedbackPrompt = notesFeedbackTemplate.format(
        title=metadata.get("title"),
        subject=metadata.get("subject"),
        tags=", ".join(metadata.get("tags", [])),
        content=metadata.get("content")
    )
    feedbackResponse = groq.invoke(feedbackPrompt)
    scoreResponse = groq.invoke(scorePrompt)
    notes_score_response = parse_notes_score(scoreResponse)
    notes_feedback_response = parse_notes_feedback(feedbackResponse)
    return {"score": notes_score_response.score, "feedback": notes_feedback_response.feedback}  



