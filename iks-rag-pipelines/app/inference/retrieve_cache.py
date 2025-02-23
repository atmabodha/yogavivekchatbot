from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient,models

load_dotenv()

# Load the embedding model
model = SentenceTransformer("sentence-transformers/multi-qa-distilbert-cos-v1")

def mock_response():
    data = {
        "summary_answer": "**Thank you for your question!** We will get back to you soon with the answer.",
        "detailed_answer": (
            "  In the meantime, you can explore related topics such as:\n\n"
            "* **The significance of karma** in the Bhagavad Gita\n" 
            "* **The four paths of yoga** described in the Gita\n"
            "* **The first sutra** of Patanjali Yoga Sutras and its meaning\n"
            "* Patanjali's concept of **'Chitta Vritti Nirodha'**\n\n"
            "_Stay tuned — we'll provide your answer shortly!_"
        ),
        "references": [
            {
                "source": "No Source", 
                "chapter": "1",
                "verse": "1",
                "text": "No relevant verse available for this query."
            }
        ]
    }
    return data
# Connect to Qdrant
qdrant_client = QdrantClient(
    url="https://bbe512e4-6b6e-475e-bfb5-fe04f5797900.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.environ.get('QDRANT_API_KEY')
)

def retrieve_context_cache(query, collection_name = "QnA_collection"):
    query = query.lower()
    query_embedding = model.encode(query).tolist()
    response = qdrant_client.query_points(collection_name=collection_name, query=query_embedding, limit=1)
    points = response.points
    score1 = points[0].score
    print(points[0].id)
    translations = [point.payload['answer'] for point in points]
    if(score1 > 0.6):
        return translations[0]
    else:
        return mock_response()
