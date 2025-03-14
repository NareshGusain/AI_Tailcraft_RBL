from flask import Flask, render_template, send_file, request, jsonify, redirect, flash, Response, Request, make_response
from fastapi.responses import FileResponse
from pathlib import Path
import requests, os
from dotenv import load_dotenv
from story_generation import Generate_story
from text_to_speech import text_to_speech_with_timestamp
from mcq_gen import generate_mcq_from_story
from utils.db import check_login
from utils.utility import cookie_hash, need_cookies, get_story, json_to_quiz, quiz_to_json, create_txt_file
from story_cover_generation import generate_cover_description, generate_story_cover
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FASTAPI_KEY")

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if need_cookies(request):
        return redirect('/login')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if check_login(email=email, password=password):
            response = make_response(redirect('/index.html'))
            response.set_cookie('email', email)
            response.set_cookie('auth_code', cookie_hash(email))
            return response
        else:
            flash("Invalid Credentials", "error")
            return redirect('/login')
    return render_template('login.html')

@app.route('/storytime', methods=['GET', 'POST'])
def generate_story():
    if need_cookies(request):
        return redirect('/login')
    else:
        return render_template('storytime.html')
    
@app.post("/create_story")
def create_story():
    if need_cookies(request):
        return redirect('/login')
    else:
        if request.method == 'POST':
            age = request.form.get('age', "")
            characters = request.form.get('characters', "")  
            scientific_concept = request.form.get('scientific_concept', "")
            story_script = Generate_story(age=age, characters=characters, scientific_concept=scientific_concept)
            story_uuid = text_to_speech_with_timestamp(text=story_script[:200])
            create_txt_file(text=story_script, story_uuid=story_uuid)
            return redirect(f"player/{story_uuid}")
        else:
            return "Required POST request."

@app.get('/player/<story_uuid>')
def story_player(story_uuid):
    if need_cookies(request):
        return render_template('index.html')
    else:
        return render_template('player.html', story_uuid=story_uuid)

@app.get("/image/<story_uuid>")
def get_image(story_uuid):
    image_path = Path(f"static/story/{story_uuid}.png")
    if image_path.is_file():
        return send_file(image_path, mimetype='image/gif')
    else:
        try:
            story_text = get_story(story_uuid)
            cover_description = generate_cover_description(story_text=story_text)
            generate_story_cover(cover_description=cover_description, story_uuid=story_uuid)
            return send_file(image_path, mimetype='image/gif')
        except:
            return send_file(f"static/story/default.jpg", mimetype='image/gif')


@app.route('/about')
def about():
    if need_cookies(request):
        return redirect('/login')
    else:
        return render_template('about.html')

@app.route('/contact.html')
def contact():
    if need_cookies(request):
        return redirect('/login')
    else:
        return render_template('contact.html')

@app.route('/vocabBuild', methods=['GET', 'POST'])
def vocabBuild():
    if need_cookies(request):
        return redirect('/login')
    else:
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
    

@app.route('/quiz/<story_uuid>', methods=['GET', 'POST'])
def generate_quiz(story_uuid):
    if need_cookies(request):
        return redirect('/login')
    else:
        return render_template('mcq.html', story_uuid=story_uuid)
            

@app.route("/get_quiz/<story_uuid>")
def get_quiz_json(story_uuid):

    if os.path.isfile(f"static/story/{story_uuid}_QUIZ.json"):
        return jsonify(json_to_quiz(story_uuid))
    else:
        try:
            quiz_json = generate_mcq_from_story(story_uuid)
            quiz_to_json(quiz_json, story_uuid)
            return jsonify(json_to_quiz(story_uuid))
        except:
            return jsonify({'msg': 'data not found'}), 400

if __name__ == '__main__':
    app.run(port=6969, debug=True)
