from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
    app.run(port= 6969, debug=True)