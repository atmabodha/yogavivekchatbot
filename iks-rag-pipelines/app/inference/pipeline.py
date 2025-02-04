import time
from groq import Groq
import os
from better_profanity import profanity
from dotenv import load_dotenv
from query_filter import *
from query_reform import rewrite_query_for_rag
from find_correct_collection import *
from retrieve_documents import *
from response_gen import *

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def pipeline_rag(query):
    start_time = time.time()
    
    query = query.lower()
    print(f"Step 1: Query converted to lowercase - {time.time() - start_time:.4f} sec")

    if not check_offensive_language(query):
        print(f"Step 2: Offensive language check passed - {time.time() - start_time:.4f} sec")

        if check_valid(query):
            print(f"Step 3: Query validity check passed - {time.time() - start_time:.4f} sec")

            query_reform = rewrite_query_for_rag(query).lower()
            print(f"Step 4: Query reformulated - {time.time() - start_time:.4f} sec")

            collection_name = get_best_match(query=query)
            print(f"Step 5: Best-matching collection found - {time.time() - start_time:.4f} sec")

            context = retrieve_context(query_reform, collection_name)
            print(f"Step 6: Context retrieved - {time.time() - start_time:.4f} sec")

            answer = get_bot_response(context, query)
            print(f"Step 7: Response generated - {time.time() - start_time:.4f} sec")

            return answer

    return "Query blocked due to invalid or offensive content."

print(pipeline_rag("how does the gita start?"))
