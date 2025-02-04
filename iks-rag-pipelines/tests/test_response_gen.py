from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def remove_think_tokens(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def get_bot_response(context="", question=""):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a highly knowledgeable and detail-oriented assistant, specializing in providing precise and contextually accurate answers. Your responses should follow a structured format: Summary, Answer, and Conclusion.",
            },
            {
                "role": "user",
                "content": (
                    f"Given the following context:\n\n"
                    f"--- Context Start ---\n{context}\n--- Context End ---\n\n"
                    f"Answer the question: {question}\n\n"
                    f"Instructions:\n"
                    f"- First, summarize the relevant parts of the context that are used to answer the question.\n"
                    f"- Then, provide a detailed and precise answer to the question based on the summarized context.\n"
                    f"- Finally, conclude by reiterating the main points and ensuring the answer is clear and concise.\n"
                    f"- Your response should rely strictly on the provided context.\n"
                    f"- Do not add any information or assumptions not explicitly mentioned in the context.\n"
                    f"- Use clear reasoning and explain your answer in a way that is simple and easy to understand.\n"
                ),
            },
        ],
        model="deepseek-r1-distill-llama-70b",
        max_tokens=1000,
    )
    return remove_think_tokens(chat_completion.choices[0].message.content)

