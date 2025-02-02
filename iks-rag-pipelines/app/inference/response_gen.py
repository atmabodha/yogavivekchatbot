import logging
import nltk
import re
from nltk.tokenize import sent_tokenize
from typing import Dict, List

nltk.download('punkt', quiet=True)


# ---- Main function to generate response ----
async def generate_answer(
    query: str, 
    verses: List[Dict[str,]], 
    client, 
    templates
) -> Dict[str,]: 
    """
    Generate an answer based on the user's query and relevant verses.

    Args:
        query (str): The user's input question.
        verses (List[Dict[str, Any]]): A list of verses, where each verse is a dictionary 
            containing 'book', 'chapter', 'verse', 'translation', and 'explanation'.
        client (Any): The API client used for LLM response generation.
        templates (Any): An object containing predefined prompt templates.

    Returns:
        Dict[str, Any]: A dictionary containing the generated response, including a summary and sources.
    """
    try:
        if not verses or client is None:
            return handle_empty_results(verses)

        query_type = classify_query(query)
        prompt = prepare_prompt(query, verses, query_type, templates)
        response = await generate_llm_response(client, prompt)
        return format_response(response, verses)

    except Exception as e:
        logging.error(f"Answer generation failed: {e}")
        return generate_fallback_response()


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
def prepare_prompt(query, verses, query_type, templates):
    verse_citations = format_verse_citations(verses[:3])
    template = getattr(templates, query_type, templates.default)
    return template.format(query=query, verses=verse_citations)


def format_verse_citations(verses):
    return "\n\n".join(
        f"[{v['book']} {v['chapter']}.{v['verse']}]: {v['translation']}\n"
        f"Explanation: {v['explanation']}"
        for v in verses
    )


# ---- LLM interaction ----
async def generate_llm_response(client, prompt, max_tokens=500):
    try:
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=0.7
        )
        response_text = response.choices[0].message.content.strip()
        response_text = ensure_complete_sentences(response_text)
        return postprocess_response(response_text)
    except Exception as e:
        logging.error(f"LLM response generation failed: {e}")
        return generate_structured_fallback()


# ---- Response formatting and processing ----
def ensure_complete_sentences(text):
    sentences = sent_tokenize(text)
    if not sentences:
        return text.strip()

    last_sentence = sentences[-1].strip()
    if not last_sentence.endswith(('.', '?', '!')):
        sentences[-1] = last_sentence + '.'

    return ' '.join(sentences)


def postprocess_response(response):
    response = response.strip()
    
    response = re.sub(r'\s+', ' ', response)  # Remove extra spaces
    response = re.sub(r'\[\s*(\d+)\s*\]', r'[\1]', response)  # Fix citation spacing
    response = re.sub(r'([a-z])\s+([A-Z])', r'\1. \2', response)  # Ensure sentence boundaries
    return response

def format_response(response, verses):
    return {
        "type": "wisdom_response",
        "verse": verses[0],
        "response": {
            "summary": response,
            "sources": [f"{v['book']} {v['chapter']}.{v['verse']}" for v in verses[:3]]
        }
    }

# ---- Fallback responses ----
def handle_empty_results(verses):
    """Handle cases where no verses are found or the client is None"""
    if not verses:
        return {
            "type": "wisdom_response",
            "verse": None,
            "response": {
                "summary": "I couldn't find specific verses that address your question. "
                           "Could you rephrase or ask about a related topic?",
                "sources": []
            }
        }
    return {"error": "No relevant verses found"}


def generate_fallback_response():
    """Provide a fallback response when the user's query needs more clarification."""
    return {
        "type": "wisdom_response",
        "verse": None,
        "response": {
            "summary": "I appreciate your question and have identified relevant wisdom. "
                       "However, to provide a more precise answer, could you clarify or specify any particular aspect?",
            "sources": []
        }
    }


def generate_structured_fallback():
    """Provide a structured fallback response if LLM output fails."""
    return (
        "While I couldn't generate a direct response from the model,"
        "I understand your question and can draw upon the ancient wisdom."
        "Let me provide a summary of the relevant teachings and insights that address your query."
    )


def handle_clarification_needed(query):
    """Prompt the user for clarification when the input is unclear."""
    return {
        "type": "clarification_needed",
        "response": {
            "summary": f"Could you clarify your question: '{query}'? "
                      "This will help me find the most relevant wisdom.",
            "sources": []
        }
    }


def handle_no_verses():
    """Handle cases where no verses match the query."""
    return {
        "type": "no_results",
        "response": {
            "summary": "I couldn't find any relevant verses. Could you refine your question?",
            "sources": []
        }
    }


    