from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
)


class ChatGTP:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.last_response = ""
        self.last_text = ""

    def open_ai_get_response(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Vymyslis otazky"},
                {"role": "user", "content": self.last_text},
                {"role": "assistant", "content": self.last_response},
                {"role": "user", "content": self.text},
            ],
            model="gpt-4o-mini",
        )
        self.last_text = self.text
        self.last_response = chat_completion.choices[0].message.content
        return chat_completion.choices[0].message.content
