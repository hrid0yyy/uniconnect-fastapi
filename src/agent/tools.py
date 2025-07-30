
from src.config.milvus_config import get_collection
from src.models.llm import embeddings
from datetime import datetime
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


ddg = DuckDuckGoSearchRun()
notes = get_collection("notes")



@tool    
def get_time() -> str:
    """
    Returns the current time in ISO format and the day of the week.
    This function can be used to get the current time for task creation or updates.
    Calculate Tomorrow, yesterday, in 'n' days, etc., using this function.
    Also calculate the day of the week.

    Returns:
        str: A string containing the current time in ISO format and the day of the week.
    """
    current_time = datetime.now()
    day_of_week = current_time.strftime("%A")  # %A gives the full weekday name (e.g., Monday)
    return f"Current time: {current_time.isoformat()}, Day: {day_of_week}"





@tool
def retrieve_notes(email: str, query: str) -> str:
    """
    Retrieve notes based on the provided email and user query.
    Returns the text fields from the results appended together as a single string.
    """
    try:
        # Embed the query
        query_vector = embeddings.embed_query(query)  # Ensure this returns a list of floats

        # Perform the vector search
        res = notes.search(
            [query_vector],  # data: Single query vector
            "vector",  # anns_field: Name of the vector field
            {"metric_type": "COSINE", "params": {"nprobe": 10}},  # param: Search parameters
            3,  # limit: Number of nearest neighbors
            f"email == '{email}'",  # expr: Filter by email
            output_fields=["text"]  # Fields to return
        )

        # Extract and append text fields
        texts = [result.entity.get("text") for result in res[0] if result.entity.get("text")]
        return " ".join(texts) if texts else ""

    except Exception as e:
        print(f"Error retrieving notes: {e}")
        return ""


