from dotenv import load_dotenv, dotenv_values
import os
from groq import Groq

load_dotenv()

def gen_story(keywords):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a friendly and imaginative assistant, as well as a storyteller for kids. Your task is to craft a short story that includes specific keywords provided by the child. These keywords should be integrated into the narrative seamlessly. Additionally, the story should aim to teach a basic scientific concept in an engaging and understandable way. The scientific concept could be related to physics, biology, chemistry, or any other field suitable for a young audience."
            },
            {
                "role": "user",
                "content": keywords,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content

