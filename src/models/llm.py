from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()  

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

groq = ChatGroq(model_name="meta-llama/llama-4-scout-17b-16e-instruct")

vision_llm = ChatGroq(
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
