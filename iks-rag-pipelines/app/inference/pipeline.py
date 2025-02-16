import time
from groq import Groq
import os
from better_profanity import profanity
from dotenv import load_dotenv
import sys
sys.path.append('..')
from app.inference.query_filter import *
from app.inference.query_reform import rewrite_query_for_rag
from app.inference.find_correct_collection import *
from app.inference.retrieve_documents import *
from app.inference.response_gen import *
from app.inference.validation import check_valid_answer
import json
load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def get_json_response1():
    data = {
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
    return json.dumps(data, indent=4)

import time

def pipeline_rag(query, max_retries=3):
    start_time = time.time()
    query = query.lower()
    collection = " "
    print(f"Step 1: Query converted to lowercase - {time.time() - start_time:.4f} sec")

    # Step 2: Offensive Language Check
    if check_offensive_language(query) == 1:
        print(f"Step 2: Offensive language check failed - {time.time() - start_time:.4f} sec")
        return get_json_response1()

    print(f"Step 2: Offensive language check passed - {time.time() - start_time:.4f} sec")

    # Step 3: Query Validity Check
    if int(check_valid(query)) == 0 :
        print(f"Step 3: Query validity check failed - {time.time() - start_time:.4f} sec")
        return get_json_response1()

    print(f"Step 3: Query validity check passed - {time.time() - start_time:.4f} sec")

    retries = 0
    while retries < max_retries:
        query_reform = rewrite_query_for_rag(query).lower()
        print(f"Step 4: Query reformulated - {time.time() - start_time:.4f} sec (Attempt {retries+1})")

        print(query_reform)

        collection_name = get_best_match(query=query_reform)
        print(f"Step 5: Best-matching collection found - {time.time() - start_time:.4f} sec")

        collection = "Patanjali Yoga Sutras" if collection_name == "yoga_collection" else "Bhagwad Gita"
        print(collection)

        context = retrieve_context(query_reform, collection_name)
        print(f"Step 6: Context retrieved - {time.time() - start_time:.4f} sec")

        answer = get_bot_response(context, query, collection)
        print(f"Step 7: Response generated - {time.time() - start_time:.4f} sec")

        validation = check_valid_answer(q=query, a=answer, c=context)
        print(f"Step 8: Validation check - {validation} - {time.time() - start_time:.4f} sec")

        if int(validation) == 1:
            return answer  # Return the validated answer

        print("Validation failed. Retrying query reformulation...")
        retries += 1

    return get_json_response1()  # Return JSON response if all retries fail
