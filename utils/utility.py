import hashlib, json

def sha256_hash(input_string: str) -> str:
    byte_string = input_string.encode('utf-8')
    sha256_hash_object = hashlib.sha256()
    sha256_hash_object.update(byte_string)
    hex_digest = sha256_hash_object.hexdigest()
    return hex_digest

def cookie_hash(email: str) -> str:
    hash1 = sha256_hash(email)
    hash2 = sha256_hash(hash1)
    return sha256_hash(hash2)

def need_cookies(request) -> bool:
    email = request.cookies.get('email')
    auth_code = request.cookies.get("auth_code")
    print(auth_code, email)
    if email!=None and auth_code!=None:
        print("Checking auth")
        return auth_code != cookie_hash(email)
    
    return True

def get_user_email(request) -> str:
    return request.cookies.get('email')

def get_story(story_uuid):
    try:
        with open(f"static/story/{story_uuid}.txt", 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{f"static/story/{story_uuid}.txt"}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def create_txt_file(text: str, story_uuid):
    try:
        with open(f"static/story/{story_uuid}.txt", 'w') as file:
            file.write(text)
        print(f"File 'static/story/{story_uuid}.txt' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")


def quiz_to_json(data, story_uuid):

    try:
        file_path = f"static/story/{story_uuid}_QUIZ.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Quiz {story_uuid} saved to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def json_to_quiz(story_uuid):
    try:
        file_path = f"static/story/{story_uuid}_QUIZ.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
if __name__ == "__main__":
    story = get_story("GR3UW")
    print()
    create_txt_file(story, "GR3UW")