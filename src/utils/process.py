from ..models.llm import vision_llm, embeddings
from langchain.schema import HumanMessage
import requests

def process_files(URL):
    """ Process Image URL to extract text and generate vector """
    response = requests.head(URL)
    if response.status_code != 200:
        return {"success": False ,"error": "File not found at the provided URL."}
    
    if URL.endswith(('.png', '.jpg', '.jpeg')):
        messages = [
            HumanMessage(
                content=[
                    {"type": "text", "text": "Extract the text from this image, dont add extra text"},
                    {"type": "image_url", "image_url": {"url": URL}}
                ]
            )
        ]
        response = vision_llm.invoke(messages)
        vector = embeddings.embed_query(response.content)
        return {"success": True, "text": response.content, "vector": vector}

