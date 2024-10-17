from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY


client = OpenAI(

    api_key=OPENAI_API_KEY,
)

def open_ai_get_response(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="gpt-4o-mini",
    )
    return chat_completion
