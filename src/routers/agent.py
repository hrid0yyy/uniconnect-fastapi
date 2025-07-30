from ..agent.init import app
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import  HumanMessage

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    email: str
    thread_id: str

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint to handle chat requests.
    """
    try:
        input_message = {
            "messages": [HumanMessage(content=f"{request.query} My email is {request.email}")]
        }
        config = {"configurable": {"thread_id": request.thread_id}}
        response = app.invoke(input_message, config=config)
        return {"response": response["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")