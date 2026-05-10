from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def detect_important_memory(message):

    prompt = f"""
    Determine if this message contains
    important long-term information.

    Important information includes:
    - goals
    - preferences
    - learning style
    - weaknesses
    - personal details
    - ongoing tasks

    Message:
    {message}

    Reply ONLY:
    YES or NO
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = (
        response.choices[0]
        .message.content
    )

    return (
        answer.strip().upper() == "YES"
    )