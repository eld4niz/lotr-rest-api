import requests
from dotenv import load_dotenv
import os
load_dotenv()

one_api = os.environ.get("ONE_API")
one_api_key = os.environ.get("ONE_API_KEY")
character_url = f"https://{one_api}/character"


def get_character(character_id, api_key):
    
    url = f"{character_url}/{character_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    
    return response.json()
