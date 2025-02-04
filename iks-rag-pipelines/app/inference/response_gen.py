from groq import Groq
import os,sys
from dotenv import load_dotenv
import re 
sys.path.append('iks-rag-pipelines/app/utils')
from prompts import PromptTemplates

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# ---- Query classification based on keywords ----
def classify_query(query):
    query_lower = query.lower().strip()

    categories = {
        "philosophical": [
            'meaning', 'truth', 'nature', 'reality', 'consciousness', 'soul',
            'dharma', 'karma', 'existence', 'purpose', 'free will', 'illusion',
            'self', 'ego', 'mind', 'maya', 'moksha', 'non-duality', 'eternal'
        ],
        "practical": [
            'how to', 'what should', 'guide', 'help', 'advice', 'practice',
            'technique', 'method', 'way', 'steps', 'daily', 'routine', 'apply',
            'habit', 'improve', 'develop'
        ],
        "comparative": [
            'difference', 'compare', 'versus', 'vs', 'contrast', 'relation',
            'similarities', 'distinction', 'connection'
        ],
        "storytelling": [
            'story', 'example', 'parable', 'analogy', 'illustration', 'narrative'
        ],
        "meditation": [
            'meditation', 'reflect', 'contemplate', 'focus', 'inner peace',
            'mindfulness', 'self-awareness', 'visualization'
        ]
    }

    for category, keywords in categories.items():
        if any(kw in query_lower for kw in keywords):
            return category

    if len(query_lower.split()) < 3 or query_lower in ["?", "explain", "clarify"]:
        return "clarification"

    return "default"

# ---- Prompt construction ----
def prepare_prompt(query, verses, query_type):
    template = getattr(PromptTemplates, query_type, PromptTemplates.default)
    return template.format(query=query, verses=verses)


def remove_think_tokens(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def get_bot_response(context="", question=""):
    query_type = classify_query(question)
    prompt = prepare_prompt(question, context, query_type)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a highly knowledgeable and detail-oriented assistant, specializing in providing precise and contextually accurate answers. Your responses should follow a structured format: Summary, Answer, and Conclusion.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="deepseek-r1-distill-llama-70b",
        max_tokens=1000,
    )
    return remove_think_tokens(chat_completion.choices[0].message.content)

