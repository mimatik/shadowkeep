from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


class ChatGTP:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.conversation_history = []

    def open_ai_get_response(self):

        self.conversation_history.append({"role": "user", "content": self.text})
        chat_completion = client.chat.completions.create(
            messages=self.conversation_history,
            model="gpt-4o-mini",
        )

        ai_response = chat_completion.choices[0].message.content

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": ai_response,
            }
        )

        print(self.conversation_history)
        return ai_response
