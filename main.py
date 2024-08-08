# from api_test import api
# import streamlit as st

# st.title("AI - Tail Craft for Kids")
# st.text("Craft a kids' story teaching science with their keywords.")

# keywords = st.text_input("Enter you keywords here")
# button = st.button("Generate story")

# if button:
#     if not keywords:
#         st.text("No keywords entered")
#     else:
#         story_text = api.gen_story(keywords)
#         st.text(story_text)


import requests

url = "https://large-text-to-speech.p.rapidapi.com/tts"

payload = { "text": "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away." }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "bd37fbca38msh4066aaf9e776096p19e2bcjsn925fdd9dc587",
	"X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())