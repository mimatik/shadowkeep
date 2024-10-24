from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
)


class ChatGTP:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.conversation = []

    def open_ai_get_response(self):
        self.conversation.append(
            {
                "role": "user",
                "content": self.text,
            }
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Jses prisera, vznikla zkrizenim monstra a ucitele cestiny, ktery rad vtipkuje. Mluv v hadankach a vyhodnocuj odpovedi. Komunikuj v cestine.",
                },
                *self.conversation,
            ],
            model="gpt-4o-mini",
        )

        assistant_message = chat_completion.choices[0].message.content
        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message
