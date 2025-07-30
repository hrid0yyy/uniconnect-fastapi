from pymilvus import connections, Collection
from dotenv import load_dotenv
import os


load_dotenv()

connections.connect(
                alias="default",
                uri=os.getenv("MILVUS_URI"),
                token=os.getenv("MILVUS_TOKEN")
            )

def get_collection(collection_name: str) -> Collection:
    """
    Get a specific collection from Milvus.
    """
    return Collection(name=collection_name)

