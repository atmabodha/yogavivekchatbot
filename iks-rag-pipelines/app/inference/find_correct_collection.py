from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

# Load the embedding model
model = SentenceTransformer("sentence-transformers/multi-qa-distilbert-cos-v1")

# Connect to Qdrant
qdrant_client = QdrantClient(
    url="https://bbe512e4-6b6e-475e-bfb5-fe04f5797900.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.environ.get('QDRANT_API_KEY')
)

def get_best_match(query: str, collection1: str = "yoga_collection", collection2: str = "gita_collection", limit: int = 1):
    query_embedding = model.encode(query).tolist()
    answers1 = qdrant_client.query_points(collection_name=collection1, query=query_embedding, limit=limit)
    answers2 = qdrant_client.query_points(collection_name=collection2, query=query_embedding, limit=limit)

    print(answers1)
    
    score1 = answers1.points[0].score if answers1.points else 0
    score2 = answers2.points[0].score if answers2.points else 0

    print(score1)
    print(score2)

    if(score1 > 0.5 or score2 > 0.5):
        if score1 >= score2:
            best_collection = collection1
        else:
            best_collection = collection2
    else:
        if(query.lower().count("gita") > query.lower().count("yoga")):
            best_collection = collection2
        else:
            best_collection = collection1

    return best_collection

