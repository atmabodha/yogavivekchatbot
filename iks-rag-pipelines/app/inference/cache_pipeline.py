import time
from groq import Groq
import os
from better_profanity import profanity
from dotenv import load_dotenv
import sys
import json
sys.path.append('..')
from app.inference.retrieve_cache import retrieve_context_cache
from app.inference.query_filter import *

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def extract_json_dict(s):
    """Extracts JSON dictionary from a string."""
    start = s.find('{')
    end = s.rfind('}')
    
    if start == -1 or end == -1 or start > end:
        return None 
    
    json_str = s[start:end+1]
    
    try:
        return json.loads(json_str)  
    except json.JSONDecodeError:
        return None 

def get_json_response1():
    """Returns a default JSON response when query validation fails."""
    data ={
        "summary_answer": "We can only answer questions related to **Bhagavad Gita** or **Patanjali Yoga Sutras**.",
        "detailed_answer": (
            "You can try asking questions like:\n\n"
            "- What is the significance of karma in the Bhagavad Gita?\n"
            "- What are the four paths of yoga described in the Gita?\n"
            "- What is the first sutra of Patanjali Yoga Sutras and its meaning?\n"
            "- How does Patanjali describe the concept of 'Chitta Vritti Nirodha'?\n\n"
            "Feel free to ask anything related to these scriptures!"
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

def pipeline_rag_cache(query):
    start_time = time.time()
    query = query.lower()
    print(f"Step 1: Query converted to lowercase - {time.time() - start_time:.4f} sec")

    if check_offensive_language(query) == 1:
        print(f"Step 2: Offensive language detected - {time.time() - start_time:.4f} sec")
        return get_json_response1()


    context = retrieve_context_cache(query)
    print(f"Step 3: Context retrieved - {time.time() - start_time:.4f} sec")
    return context
