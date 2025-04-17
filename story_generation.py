import os
from dotenv import load_dotenv
from datetime import datetime

from groq import Groq
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

Groq_client = Groq(api_key=GROQ_API_KEY)

LLM_INSTRUCTIONS = lambda: f"""
LLM Instruction: Crafting Engaging, Educational Stories for Children
Objective: Generate short, engaging stories featuring popular characters and superheroes that illustrate simple scientific ideas. The stories must be fun and age-appropriate for children, scientifically accurate, and suitable for direct conversion to speech without requiring extra post-processing.

Guidelines:

Audience:
-The audience is children between 5-10 years old.
-Keep the language simple and sentences concise.
-Ensure the tone is friendly, fun, and exciting.

Structure:
-Introduction: Start with an attention-grabbing opening that introduces the popular characters or superheroes.
-Plot: Focus the plot on one clear scientific concept, such as gravity, electricity, or the water cycle unless specified some concepts in command. Ensure the concept is explained in an easy-to-understand way through the actions or dialogues of the characters.
-Conclusion: End the story with a positive message or lesson, reinforcing the scientific concept while wrapping up the plot.

Character Interaction:
-Characters should interact in a way that drives the scientific lesson forward.
-Avoid introducing too many characters. Focus on a maximum of 2-3 well-known characters to maintain clarity.
-Ensure their dialogues are engaging and explain the scientific ideas in a conversational manner.

Scientific Accuracy:
-Present the scientific information correctly, without oversimplifying or making it confusing.
-Explain complex ideas using analogies that children can easily understand.

Length:
-The story should be around 300-500 words.
-It must be concise enough for an audio playtime of approximately 3-5 minutes.

Text-to-Speech Considerations:
-Ensure there are no stray characters, special symbols, or unnecessary dialogue that could confuse the text-to-speech model.
-Do not include complex punctuation that could interfere with natural speech flow.
-Avoid producing multiple storylines or tangents. Stick to one clear, linear story.

No Extra Output:
-The final output must end after the story concludes. Do not produce any additional text (such as “The End” or commentary) as the output will go directly into the text-to-speech system for audio narration.
"""

def Generate_story(age: int|str|None = None, 
                   characters: str|list[str]|None = None, 
                   scientific_concept: str|list[str]|None = None) -> str:
    """
    Using "llama3-8b-8192"
    """
    LLM_PROMPT = """
    -The final output must end after the story concludes. Do not produce any additional text (such as “The End” or commentary) as the output will go directly into the text-to-speech system for audio narration.
    -Keep the terms in the story simple and use only word which are age comprehendable and appropriate.
    """
    if age:
        LLM_PROMPT+=f"The kid is {age}.\n"
    if scientific_concept:
        LLM_PROMPT+=f"Use Scientific concept such as {scientific_concept if type(scientific_concept)==str else ', '.join(scientific_concept)}.\n"
    if characters:
        LLM_PROMPT+=f"Use character such as {characters if type(characters)==str else ', '.join(characters)}.\n"

    chat_completion = Groq_client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": LLM_INSTRUCTIONS()
            },
            {
                "role": "user",
                "content": LLM_PROMPT,
            }
        ],
        model="llama3-8b-8192",
    )  

    return chat_completion.choices[0].message.content