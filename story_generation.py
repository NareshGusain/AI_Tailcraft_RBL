import os
from dotenv import load_dotenv
from datetime import datetime

from groq import Groq
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

Groq_client = Groq(api_key=GROQ_API_KEY,)

LLM_INSTRUCTIONS = lambda: f"""
LLM Instruction: Craft Engaging, Educational Stories for Children
Objective: Generate a captivating, age-appropriate story for children aged 5-10 that illustrates one clear scientific concept. The story should be fun, engaging, and scientifically accurate, with language simple enough for direct text-to-speech conversion. Do not include any extraneous text, greetings, or closing remarks.

Guidelines:

Audience:
- Target audience: children between 5-15 years old.
- Use simple vocabulary and short, clear sentences.
- Maintain a friendly, fun, and enthusiastic tone.

Structure:
- Introduction: Begin with a compelling opening that introduces one or two popular characters or superheroes.
- Plot: Focus the narrative on one clear scientific concept (e.g., gravity, electricity, water cycle). Illustrate this concept through the characters' actions or dialogue in a straightforward manner.
- Conclusion: End with a positive message that reinforces the scientific concept, keeping the narrative focused and linear.

Character Interaction:
- Limit characters to a maximum of 2-3 to ensure clarity.
- Characters should interact naturally and drive the scientific lesson through engaging dialogue.
- Avoid overly complex interactions; keep the conversation simple and relatable.

Scientific Accuracy:
- Present the scientific concept accurately without oversimplification.
- Use relatable analogies or examples that children can easily understand.

Length:
- The story should be approximately 300-500 words (suitable for an audio playtime of around 3-5 minutes).

Text-to-Speech Considerations:
- Avoid any stray characters, symbols, or excessive punctuation that could disrupt the natural flow in text-to-speech conversion.
- Do not include any extra text such as greetings, introductions, or conclusions like "Here's your story" or "The End."
- The output must consist solely of the story narrative.

No Extra Output:
- The final output must end immediately after the story concludes—no additional text or commentary is allowed.
"""

def Generate_story(age: int|str|None = None, 
                   characters: str|list[str]|None = None, 
                   scientific_concept: str|list[str]|None = None) -> str:
    """
    Using "llama3-8b-8192"
    """
    LLM_PROMPT = """
    - Output only the story narrative. Do not include any headers, introductions, or closing statements.
    - Use clear, simple language that is age-appropriate for children (5-15 years old).
    - Ensure that the story is engaging, educational, and strictly about the narrative.
    """
    if age:
        LLM_PROMPT += f"The kid is {age} years old.\n"
    if scientific_concept:
        if isinstance(scientific_concept, str):
            LLM_PROMPT += f"Focus on the scientific concept: {scientific_concept}.\n"
        else:
            LLM_PROMPT += f"Focus on scientific concepts such as {', '.join(scientific_concept)}.\n"
    if characters:
        if isinstance(characters, str):
            LLM_PROMPT += f"Include the character: {characters}.\n"
        else:
            LLM_PROMPT += f"Include characters such as {', '.join(characters)}.\n"
            
            
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