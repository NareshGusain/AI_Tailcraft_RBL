import requests, os
from PIL import Image
from io import BytesIO
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

hg_client = InferenceClient(
    api_key=os.getenv("HUGGING_FACE_API"),
)

grok_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"), 
)


def generate_story_cover(cover_description, story_uuid):
    image = hg_client.text_to_image(
        "[In cartoon style]: "+cover_description,
        model="stabilityai/stable-diffusion-3.5-large",
        height=800,
        width=400
    )
    image.save(f"static/story/{story_uuid}.png", format="PNG")
    

def generate_cover_description(story_text):
    prompt = (
        "Based on the following story, provide a concise and clear description "
        "of a suitable cover image. Keep the description under 30 words.\n\n"
        f"Story:\n{story_text}\n\n"
        "Cover Image Description:"
    )

    chat_completion = grok_client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )

    description = chat_completion.choices[0].message.content.strip()
    return description
