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
import re 
import random

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def get_json_response1():
    """Returns a default JSON response when query validation fails."""
    data = {
        "summary_answer": "#  Invalid Query\n  We can only answer questions related to **Bhagavad Gita** or **Patanjali Yoga Sutras**.",
        "detailed_answer": (
            "## Example Questions\n\n"
            " You can try asking questions like:\n\n"
            "* What is the significance of karma in the **Bhagavad Gita**?\n"
            "* What are the four paths of yoga described in the **Gita**?\n"
            "* What is the first sutra of **Patanjali Yoga Sutras** and its meaning?\n"
            "* How does Patanjali describe the concept of **'Chitta Vritti Nirodha'**?\n\n"
            "_Feel free to ask anything related to these scriptures!_"
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


def is_small_talk(query):
    """
    Detect small talk queries using comprehensive regex patterns and common phrases.
    
    Args:
        query (str): Input query to check for small talk.
    
    Returns:
        bool: True if query is small talk, False otherwise.
    """
    small_talk_patterns = [
        # Greetings
        r'^(hi|hey|hello|howdy|hiya|yo)[\s!]*$',
        r'^(hi+|hey+|hello+)[\s!]*$',
        r'^(morning|afternoon|evening)[\s!]*$',
        r'^good (morning|afternoon|evening)[\s?!]*$',
        
        # How are you variations
        r'^how are you[\s?!]*$',
        r'^how\'?re you[\s?!]*$',
        r'^how you doing[\s?!]*$',
        r'^what\'?s up[\s?!]*$',
        r'^wassup[\s?!]*$',
        r'^sup[\s?!]*$',
        
        # Introductions and pleasantries
        r'^(nice to|pleased to) meet you[\s!]*$',
        r'^(hey there|greetings|salutations)[\s!]*$',
        r'^(good day|top of the morning)[\s!]*$',
        r'^(long time no see|it\'?s been a while)[\s!]*$',
        
        # Casual check-ins
        r'^how\'?s it going[\s?!]*$',
        r'^how\'?s everything[\s?!]*$',
        r'^how are things[\s?!]*$',
        
        # Polite acknowledgments
        r'^(thanks|thank you)[\s!]*$',
        r'^(appreciate it|thx)[\s!]*$',
        
        # Farewell and exit
        r'^(bye|goodbye|see you|take care)[\s!]*$',
        r'^(catch you later|ttyl)[\s!]*$'
    ]
    
    # Convert query to lowercase and remove extra whitespace
    normalized_query = query.lower().strip()
    
    # Check against small talk patterns
    for pattern in small_talk_patterns:
        if re.match(pattern, normalized_query):
            return True
    
    return False

def get_small_talk_response(query):
    """
    Generate a diverse and friendly small talk JSON response.
    
    Args:
        query (str): Original small talk query.
    
    Returns:
        dict: JSON response with friendly small talk content.
    """
    greeting_responses = [
        {
            "summary_answer": "# Hello There! 👋",
            "detailed_answer": (
                "## Welcome!\n\n"
                "I'm an AI assistant specialized in providing insights about the "
                "**Bhagavad Gita** and **Patanjali Yoga Sutras**. Feel free to ask "
                "me any questions about these profound spiritual texts."
            ),
            "references": [
                {
                    "source": "AI Assistant Greeting",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Wisdom begins with a warm welcome."
                }
            ]
        },
        {
            "summary_answer": "# Namaste! 🙏",
            "detailed_answer": (
                "## Greetings!\n\n"
                "I'm here to help you explore the wisdom of ancient Indian spiritual "
                "texts. Would you like to learn about the **Bhagavad Gita** or "
                "**Patanjali Yoga Sutras**?"
            ),
            "references": [
                {
                    "source": "AI Assistant Salutation",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Every conversation is an opportunity for learning."
                }
            ]
        }
    ]

    how_are_you_responses = [
        {
            "summary_answer": "# I'm Doing Well! 🌟",
            "detailed_answer": (
                "## Thank you for asking!\n\n"
                "As an AI, I'm always ready to assist you in exploring the profound "
                "wisdom of the **Bhagavad Gita** and **Patanjali Yoga Sutras**. "
                "What spiritual insights can I help you with today?"
            ),
            "references": [
                {
                    "source": "AI Wellness Reflection",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Inner peace is the true measure of well-being."
                }
            ]
        },
        {
            "summary_answer": "# Excellent and Eager to Help! 💡",
            "detailed_answer": (
                "## I appreciate your kind inquiry!\n\n"
                "My purpose is to share knowledge about spiritual texts. I'm "
                "fully operational and excited to dive into discussions about "
                "**yoga**, **karma**, or any philosophical insights you're curious about."
            ),
            "references": [
                {
                    "source": "AI Readiness Statement",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Readiness is the first step towards understanding."
                }
            ]
        }
    ]

    thanks_responses = [
        {
            "summary_answer": "# You're Welcome! 😊",
            "detailed_answer": (
                "## Happy to help!\n\n"
                "If you're interested in deeper wisdom, I'm always ready to discuss "
                "the profound teachings of the **Bhagavad Gita** or "
                "**Patanjali Yoga Sutras**."
            ),
            "references": [
                {
                    "source": "AI Gratitude Response",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Gratitude opens the door to further learning."
                }
            ]
        }
    ]

    farewell_responses = [
        {
            "summary_answer": "# Goodbye! 👋",
            "detailed_answer": (
                "## Until we meet again!\n\n"
                "May your journey be filled with wisdom and inner peace. "
                "Whenever you're ready to explore the **Bhagavad Gita** or "
                "**Patanjali Yoga Sutras**, I'll be here."
            ),
            "references": [
                {
                    "source": "AI Farewell Message",
                    "chapter": "1",
                    "verse": "1",
                    "text": "Every ending is a new beginning."
                }
            ]
        }
    ]
    
    # Detect type of small talk and return appropriate response
    normalized_query = query.lower().strip()
    
    # Greetings
    if re.match(r'^(hi|hey|hello|howdy|hiya|yo)[\s!]*$', normalized_query):
        return random.choice(greeting_responses)
    
    # How are you
    if re.match(r'^(how are you|how\'?re you|what\'?s up|how you doing)[\s?!]*$', normalized_query):
        return random.choice(how_are_you_responses)
    
    # Thanks
    if re.match(r'^(thanks|thank you|appreciate it|thx)[\s!]*$', normalized_query):
        return random.choice(thanks_responses)
    
    # Farewell
    if re.match(r'^(bye|goodbye|see you|take care|catch you later|ttyl)[\s!]*$', normalized_query):
        return random.choice(farewell_responses)
    
    # Fallback
    return random.choice(greeting_responses)

def pipeline_rag_cache(query):
    """
    Modified pipeline to handle small talk and retrieve context.
    
    Args:
        query (str): User input query.
    
    Returns:
        dict: JSON response for the query.
    """
    start_time = time.time()
    query = query.lower()
    print(f"Step 1: Query converted to lowercase - {time.time() - start_time:.4f} sec")
    
    if check_offensive_language(query) == 1:
        print(f"Step 2: Offensive language detected - {time.time() - start_time:.4f} sec")
        return get_json_response1()
    
    # Check for small talk before retrieving context
    if is_small_talk(query):
        print(f"Step 2: Small talk detected - {time.time() - start_time:.4f} sec")
        return get_small_talk_response(query)
    
    context = retrieve_context_cache(query)
    print(f"Step 3: Context retrieved - {time.time() - start_time:.4f} sec")
    return context
