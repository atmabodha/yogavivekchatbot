from groq import Groq
import os
import re

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def remove_think_tokens(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def rewrite_query_for_rag(query=""):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that rewrites user queries to improve retrieval for a RAG system. "
                    "Your task is to reformat the input query into the following format: <query><new key words related to the query>. "
                    "The new keywords should be relevant to the original query and should help in retrieving more accurate information. "
                    "Focus on extracting key concepts, entities, or themes from the query. "
                    "For example, if the query is about 'the concept of dharma in the Bhagavad Gita,' the output could be: "
                    "<What is the concept of dharma in the Bhagavad Gita?><dharma, Bhagavad Gita, concept, philosophy>. "
                    "Ensure the rewritten query is concise and the keywords are highly relevant."
                    "the key words must be related to the query and nothing else"
                ),
            },
            {
                "role": "user",
                "content": f"Rewrite the following query for better retrieval: {query} i only want the reforved query output in the format i have given to you i want no output else in it at all only the format i have given not even here is the response",
            },
        ],
        model="llama3-8b-8192",
        max_tokens=500,
    )
    return  remove_think_tokens(chat_completion.choices[0].message.content)


