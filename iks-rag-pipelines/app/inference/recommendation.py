import pickle
import pandas as pd
import numpy as np
import random
import time
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import sys
sys.path.append(".")
model = SentenceTransformer("sentence-transformers/multi-qa-distilbert-cos-v1")
with open("app/models/kmeans_model_l.pkl", "rb") as file:
    kmeans = pickle.load(file)
    
df = pd.read_csv("app/dataset/c_d.csv")
cluster_labels = df['Cluster_Label'].to_numpy()
questions = df['question'].to_numpy()

def get_recommended_questions(query):

    start_time = time.time()
    
    query_embedding = model.encode([query])
    
    # Predict cluster label
    cluster_label = kmeans.predict(query_embedding)[0]
    
    filtered_questions = questions[cluster_labels == cluster_label].tolist()
    
    # Select random samples
    random_questions = random.sample(filtered_questions, min(5, len(filtered_questions)))
    
    execution_time = time.time() - start_time
    print(f"Execution Time: {execution_time:.4f} seconds")
    
    return {"Questions": random_questions}



