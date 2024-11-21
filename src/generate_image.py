from shadowkeep.config import OPENAI_API_KEY, GENERATED_IMG_DIR
from openai import OpenAI
import urllib.request
client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def generate(text):
    res = client.images.generate(
        prompt=text,
        model="dall-e-3",
        size="1024x1024",

    )

    return res.data[0].url


def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)


running = True
while running:
    text = input("dej parametry k obrazku: ")
    print("waiting")
    url = generate(text)
    print(url)
    download_image(url, GENERATED_IMG_DIR/f"{text}.png")
