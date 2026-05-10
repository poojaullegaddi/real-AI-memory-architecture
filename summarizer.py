from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_conversation(messages):

    conversation_text = ""

    for msg in messages:

        conversation_text += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    prompt = f"""
    Summarize this conversation.

    Preserve:
    - important concepts
    - unresolved questions
    - learning goals
    - preferences
    - important context

    Conversation:
    {conversation_text}
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

    return (
        response.choices[0]
        .message.content
    )