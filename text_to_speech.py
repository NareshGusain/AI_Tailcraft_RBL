import requests, json, base64, os, random
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def text_to_speech_with_timestamp(text: str, Voice_ID: str = "XrExE9yKIg1WjnnlVkGX") -> str:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{Voice_ID}/with-timestamps"
    uuid_pool = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    generate_uuid = lambda: ''.join(random.choice(uuid_pool) for _ in range(5))
    uuid = generate_uuid()
    audio_file_path = f"static/story/{uuid}.mp3"
    json_file_path = f"static/story/{uuid}.json"


    headers = {
    "Content-Type": "application/json",
    "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
    }


    response = requests.post(
        url,
        json=data,
        headers=headers,
    )

    if response.status_code != 200:
        print(f"Error encountered, status: {response.status_code}, "
                f"content: {response.text}")
        quit()

    # convert the response which contains bytes into a JSON string from utf-8 encoding
    json_string = response.content.decode("utf-8")

    # parse the JSON string and load the data as a dictionary
    response_dict = json.loads(json_string)

    # the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string, 
    # we need to decode it into bytes in order to save the audio as a file
    audio_bytes = base64.b64decode(response_dict["audio_base64"])

    with open(audio_file_path, 'wb') as f:
        f.write(audio_bytes)

    # the 'alignment' entry contains the mapping between input characters and their timestamps
    print(response_dict['alignment'])

    with open(json_file_path, "w") as outfile: 
        json.dump(response_dict['alignment'], outfile)
    
    return uuid