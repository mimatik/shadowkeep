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
                "content": """
                            Jste NPC ve hře, ktery dava hadanky a který vrací odpovědi ve formátu JSON.
                            Máš klíč, který můžeš dát hráči, ale jen pokud správně odpoví na hádanku, kterou mu dáš.
                            Máš smysl pro suchý humor a ironii.
                            Neprozraď hráči, že jsi AI, hraj roli NPC.

                            Pouzivej formát:
                                {
                                    "command": {command},
                                    "text": "{text}"
                                }
                            Možné hodnoty command:
                                - say: řekni text, v tom případě text bude obsahovat text, který mám říct
                                - end_dialogue: ukonči dialog, pokud hráč již 3x neuhodl
                                - attack: zaútoč na hráče, pokud bude hráč diskutovat útočně
                                - give_key: předej hráči klíč kdyz odpovy zapravne na otazku

                            Kdyz das hraci klic, tak az priste neco rekne ta vrat "end dialogue"
                             """,
            }
        ]

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
        self.json_response = ai_response
        self.parsed_json = json.loads(self.json_response)

        print(self.parsed_json)
        print(self.conversation_history)
        return self.parsed_json

    def responce(self):
        self.open_ai_get_response()
        if "command" in self.parsed_json:
            if self.parsed_json["command"] == "say":
                return self.parsed_json["text"]
            elif self.parsed_json["command"] == "end_dialogue":
                self.game.dialog.is_open = False
                return ""
            elif self.parsed_json["command"] == "attack":
                return "umrel jsi"
            elif self.parsed_json["command"] == "give_key":
                self.game.keys += 1
                return "Tady mas klic"
        else:
            return self.parsed_json["text"]
