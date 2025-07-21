from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = "llama-3.1-8b-instant"

chatgroq = ChatGroq(model_name=model)



