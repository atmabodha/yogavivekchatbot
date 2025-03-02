import pickle
import pandas as pd
import numpy as np
import random
import time
import torch
from transformers import AutoModel, AutoTokenizer
import sys
from collections import Counter

sys.path.append(".")

# Load transformer model and tokenizer
MODEL_NAME = "sentence-transformers/multi-qa-distilbert-cos-v1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Move model to CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load pre-trained KMeans model
with open("app/models/kmeans_model_l.pkl", "rb") as file:
    kmeans = pickle.load(file)

# Load dataset
df = pd.read_csv("app/dataset/c_d.csv")
cluster_labels = df['Cluster_Label'].to_numpy()
questions = df['question'].to_numpy()

def encode_text(query):
    """Generate embeddings for the input text."""
    tokens = tokenizer(query, return_tensors="pt", padding=True, truncation=True)

    # Move tokens to the same device as model
    tokens = {key: val.to(device) for key, val in tokens.items()}

    with torch.no_grad():
        output = model(**tokens)

    # Mean pooling to get a fixed-size embedding
    embedding = output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    
    return embedding.reshape(1, -1)  # Reshape for KMeans input

def keyword_search(query):
    """Finds questions with the most matching keywords from the dataset."""
    query_words = set(query.lower().split())
    
    # Count keyword matches for each question
    match_counts = []
    for question in questions:
        question_words = set(question.lower().split())
        match_count = len(query_words & question_words)  # Count common words
        match_counts.append((question, match_count))
    
    # Sort by highest match count
    sorted_questions = sorted(match_counts, key=lambda x: x[1], reverse=True)

    top_questions = [q[0] for q in sorted_questions[:5] if q[1] > 0]

    return {"suggestions": top_questions if top_questions else ["No relevant questions found."]}

def get_recommended_questions(query):
    """Fetches recommended questions using clustering or keyword search."""
    start_time = time.time()

    if len(query.split(" ")) > 7:
        query_embedding = encode_text(query)

        cluster_label = kmeans.predict(query_embedding)[0]

        # Get questions from the predicted cluster
        filtered_questions = questions[cluster_labels == cluster_label].tolist()

        # Select random samples
        random_questions = random.sample(filtered_questions, min(5, len(filtered_questions)))

        execution_time = time.time() - start_time
        print(f"Execution Time: {execution_time:.4f} seconds (Cluster: {cluster_label})")

        return {"suggestions": random_questions}
    
    else:
        return keyword_search(query)  # Perform keyword search for short queries
