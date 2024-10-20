from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY


client = OpenAI(

    api_key=OPENAI_API_KEY,
)

class ChatGTP:
    def __init__(self, game):
        self.game = game
        self.text = ""
    def open_ai_get_response(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.text,
                }
            ],
            model="gpt-4o-mini",
        )
        return chat_completion.choices[0].message.content
