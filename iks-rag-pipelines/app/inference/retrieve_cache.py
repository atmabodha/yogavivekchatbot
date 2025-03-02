import torch
import os
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer
from qdrant_client import QdrantClient, models

load_dotenv()

# Load tokenizer and model
MODEL_NAME = "sentence-transformers/multi-qa-distilbert-cos-v1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Move model to CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def encode_text(query):
    tokens = tokenizer(query, return_tensors="pt", padding=True, truncation=True)
    
    # Move tokens to the same device as model
    tokens = {key: val.to(device) for key, val in tokens.items()}

    with torch.no_grad():
        output = model(**tokens)

    # Mean pooling to get a fixed-size embedding
    embedding = output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embedding.tolist()

def mock_response():
    """Returns a default response when no relevant answer is found."""
    return {
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

# Connect to Qdrant
qdrant_client = QdrantClient(
    url="https://bbe512e4-6b6e-475e-bfb5-fe04f5797900.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.environ.get('QDRANT_API_KEY')
)

def retrieve_context_cache(query, collection_name="QnA_collection"):
    """Retrieves relevant context from Qdrant based on query similarity."""
    query = query.lower()
    query_embedding = encode_text(query)
    
    response = qdrant_client.query_points(collection_name=collection_name, query=query_embedding, limit=1)
    points = response.points
    
    if not points:
        return mock_response()

    score = points[0].score
    print(points[0].id)

    if score > 0.6:
        return points[0].payload['answer']
    else:
        return mock_response()
