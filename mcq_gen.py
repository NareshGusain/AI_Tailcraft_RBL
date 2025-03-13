from groq import Groq
from flask import Flask, request, render_template, jsonify
import json
import random
import re
import os

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY_AMAN"))

def generate_mcq_from_story(story_text):
    # Define the system prompt to generate MCQs
    system_prompt = """
    You are an educational quiz creator for children. Generate 4 multiple-choice questions based on the story provided.
    Each question should:
    1. Test understanding of scientific concepts presented in the story
    2. Have 1 correct answer and 3 plausible but incorrect answers
    3. Be age-appropriate for children
    
    Return ONLY the questions in JSON format with NO additional text:
    {
      "questions": [
        {
          "question": "Question text here?",
          "options": ["A. Answer A", "B. Answer B", "C. Answer C", "D. Answer D"],
          "correct_answer": "A"
        },
        ... (more questions)
      ]
    }
    """
    
    # Create the messages for the Groq API
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate 4 multiple choice questions based on this story: {story_text}"}
    ]
    
    # Call the Groq API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,  # Changed from max_completion_tokens to max_tokens
        top_p=1,
        stream=False,
        stop=None,
    )
    
    # Get the response content
    response_content = completion.choices[0].message.content
    
    # Extract the JSON part from the response
    try:
        # Find JSON content by looking for the JSON structure
        json_pattern = r'(\{[\s\S]*"questions":\s*\[[\s\S]*\]\s*\})'
        json_match = re.search(json_pattern, response_content)
        
        if json_match:
            json_content = json_match.group(1)
            # Parse the JSON
            quiz_data = json.loads(json_content)
            
            # Process each question
            for question in quiz_data["questions"]:
                options = question["options"]
                correct_letter = question["correct_answer"]
                
                # Find the correct answer text based on the letter
                correct_answer_text = None
                for option in options:
                    if option.startswith(correct_letter + ".") or option.startswith(correct_letter + " "):
                        correct_answer_text = option
                        break
                
                if correct_answer_text is None:
                    # If we can't find the correct answer by letter, use the index
                    # (A=0, B=1, C=2, D=3)
                    letter_index = ord(correct_letter) - ord('A')
                    if 0 <= letter_index < len(options):
                        correct_answer_text = options[letter_index]
                
                # Clean up the options (remove the A., B., C., D. prefixes)
                cleaned_options = []
                for opt in options:
                    # Match patterns like "A. text" or "A text"
                    match = re.match(r'^([A-D])[.\s]\s*(.+)$', opt)
                    if match:
                        cleaned_options.append(match.group(2))
                    else:
                        cleaned_options.append(opt)
                
                # Extract the correct answer text without the prefix
                if correct_answer_text:
                    match = re.match(r'^([A-D])[.\s]\s*(.+)$', correct_answer_text)
                    if match:
                        correct_clean = match.group(2)
                    else:
                        correct_clean = correct_answer_text
                else:
                    # Fallback
                    correct_clean = "Could not determine correct answer"
                
                # Update the question data
                question["options"] = cleaned_options
                question["correct_answer"] = correct_clean
                
                # Now shuffle the cleaned options
                random.shuffle(question["options"])
                
                # Update the correct_answer index
                question["correct_index"] = question["options"].index(correct_clean)
                
            return quiz_data
        else:
            print("Could not find JSON pattern in response")
            return {"error": "Failed to parse quiz data"}
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response was: {response_content}")
        return {"error": "Failed to generate quiz", "details": str(e)}