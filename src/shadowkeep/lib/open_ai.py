from openai import OpenAI
from shadowkeep.config import OPENAI_API_KEY
import json

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


class ChatGTP:
    def __init__(self, game):
        self.game = game
        self.text = ""
        self.conversation_history = [
            {
                "role": "system",
                "content": """Jste monster, ktery dava hadanky a který vrací odpovědi ve formátu JSON.
                 Pouzivej key Answers.Hodnota bude vzdy string.
                 Kdyz mi das hadanku(jenom kdys se te zeptam abys mi ji dal) a ja ti odpovim spatne,
                 tak hodnota bude Lez, pokud odpovim spravne, tak hodnota bude Pravda,
                 a pokud nebudu odpovidat na hadanku, tak hodnotu vymyslis ty.""",
            }
        ]

    def open_ai_get_response(self):

        self.conversation_history.append({"role": "user", "content": self.text})
        chat_completion = client.chat.completions.create(
            messages=self.conversation_history,
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
        )

        ai_response = chat_completion.choices[0].message.content

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": ai_response,
            }
        )
        self.json_response = ai_response
        print(self.json_response)
        self.parsed_json = json.loads(self.json_response)

        print(self.parsed_json)
        print(self.conversation_history)
        return self.parsed_json
