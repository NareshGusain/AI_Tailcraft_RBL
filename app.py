from flask import Flask, render_template, request, jsonify
from api_test import api

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/storytime', methods = ['GET' , 'POST'])
def generate_story():
    story = None
    if request.method == 'POST':
        keywords = request.form.get('keywords')  # Get the form data from POST request
        if keywords:
            story = api.gen_story(keywords)  # Call your story generation function
    return render_template('storytime.html', story=story)
    


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(port=8080, debug=True)
