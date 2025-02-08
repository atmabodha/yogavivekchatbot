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
load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def pipeline_rag(query, max_retries=3):
    start_time = time.time()
    query = query.lower()
    print(f"Step 1: Query converted to lowercase - {time.time() - start_time:.4f} sec")

    if not check_offensive_language(query):
        print(f"Step 2: Offensive language check passed - {time.time() - start_time:.4f} sec")

        if check_valid(query):
            print(f"Step 3: Query validity check passed - {time.time() - start_time:.4f} sec")

            retries = 0
            while retries < max_retries:
                query_reform = rewrite_query_for_rag(query).lower()
                print(f"Step 4: Query reformulated - {time.time() - start_time:.4f} sec (Attempt {retries+1})")

                collection_name = get_best_match(query=query_reform)
                print(f"Step 5: Best-matching collection found - {time.time() - start_time:.4f} sec")

                context = retrieve_context(query_reform, collection_name)
                print(f"Step 6: Context retrieved - {time.time() - start_time:.4f} sec")

                answer = get_bot_response(context, query)
                print(f"Step 7: Response generated - {time.time() - start_time:.4f} sec")

                validation = check_valid_answer(q=query, a=answer, c=context)
                print(f"Step 8: Validation check - {validation} - {time.time() - start_time:.4f} sec")

                if int(validation) == 1:
                    return answer  # Return the validated answer

                print("Validation failed. Retrying query reformulation...")
                retries += 1

            return "Could not generate a valid response after multiple attempts."

    return "Query blocked due to invalid or offensive content."

