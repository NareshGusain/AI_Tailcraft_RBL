import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
if supabase:
    print("connected")
else:
    print("No No")

def check_login(email: str, password: str) -> bool:
    response = supabase.table('user_login').select('password').eq('email', email).execute()
    if response.data:
        stored_password = response.data[0]['password']
        return stored_password == password
    
    print('Auth Failed')
    return False

def get_story_history(email: str):
    response = supabase.table('story_info').select('*').eq('user_id', email).execute()
    print(response.data)
    return response.data[::-1]


def save_story(age_info: str, character_info: str, scientific_info: str, email: str, uuid: str):
    response = supabase.table('story_info').insert({"user_id": email,
                                                    "uuid": uuid,
                                                    "age_info": age_info,
                                                    "character_info": character_info,
                                                    "scientific_info": scientific_info}).execute()

def upload_story_to_bucket(uuid: str, file_types: list):
    for file_type in file_types:
        with open("static/story/"+uuid+file_type, "rb") as file:
            response = supabase.storage.from_("storyfiles").upload(
                path=uuid+file_type,
                file=file,
                file_options={"content-type": "application/pdf", "upsert": False}
            )


def check_file_in_bucket_and_download(file_name: str)-> bool:
    try:
        print(f"Trying to download {file_name}")
        response = supabase.storage.from_("storyfiles").download(file_name)
        with open("static/story/"+file_name, 'wb') as f:
            f.write(response)
        print(f"Downloaded {file_name}.")
        return True
    except:
        return False


def get_story_files(uuid: str):
    file_types = ['.json', '.mp3', '.txt']

    for file_type in file_types:
        image_path = Path(f"static/story/{uuid}"+file_type)
        if not image_path.is_file():
            check_file_in_bucket_and_download(f"{uuid}{file_type}")

    

    


