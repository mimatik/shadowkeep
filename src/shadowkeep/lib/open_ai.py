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
        self.model = "gpt-4o-mini"

    def openai_get_init_response(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Jses prisera, vznikla zkrizenim monstra a ucitele cestiny, ktery rad vtipkuje. Mluv v hadankach a vyhodnocuj odpovedi. Komunikuj v cestine. Jako prvni vytvor otazku, na kterou neni snadne odpovedet",
                },
            ],
            model=self.model,
        )

        assistant_message = chat_completion.choices[0].message.content
        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message

    def openai_get_response(self):
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
            model=self.model,
        )

        assistant_message = chat_completion.choices[0].message.content
        self.conversation.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )
        print(self.conversation)
        return assistant_message
