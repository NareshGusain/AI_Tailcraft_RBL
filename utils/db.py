import os
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

# is_authenticated = check_login('user@example.com', 'securepassword')
# if is_authenticated:
#     print('Login successful')
# else:
#     print('Invalid credentials')
