from flask import Flask, render_template, request, jsonify, redirect
import requests
from story_generation import Generate_story
from text_to_speech import text_to_speech_with_timestamp

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/storytime', methods = ['GET' , 'POST'])
def generate_story():
    return render_template('storytime.html')
    
@app.post("/create_story")
def create_story():
    if request.method == 'POST':
        age = request.form.get('age', "")
        characters = request.form.get('characters', "")  
        scientific_concept = request.form.get('scientific_concept', "")
        #print("Param: ",age, characters, scientific_concept)
        story_script = Generate_story(age=age, characters=characters, scientific_concept=scientific_concept)
        story_uuid = text_to_speech_with_timestamp(text=story_script[:200])
        return redirect(f"player/{story_uuid}")
    else:
        return "Required POST request."

@app.get('/player/<story_uuid>')
def story_player(story_uuid):
    return render_template('player.html', story_uuid=story_uuid)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/vocabBuild', methods=['GET', 'POST'])
def vocabBuild():
    word_data = None
    searched_word = ""
    error = None
    
    if request.method == 'POST':
        searched_word = request.form.get('word', '').strip()
        if searched_word:
            word_data, error = get_word_definition(searched_word)
    
    return render_template('vocabBuild.html', word_data=word_data, searched_word=searched_word, error=error)

def get_word_definition(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        if response.status_code == 200:
            data = response.json()
            return data, None
        elif response.status_code == 404:
            return None, "Word not found. Please try another word."
        else:
            return None, f"Error: {response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(port=6969, debug=True)
