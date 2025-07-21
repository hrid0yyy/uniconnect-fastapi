from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  


model = "gemini-2.0-flash"

gemini = ChatGoogleGenerativeAI(model=model)


