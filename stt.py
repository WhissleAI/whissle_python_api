import requests
from .config import get_auth_token
from .utils import prepare_url

def speech_to_text(audio_file_path, model_name='EN'):
    base_url = 'https://api.whissle.ai/v0/conversation/STT'
    params = {
        'model_name': model_name,
        'auth_token': get_auth_token()
    }
    
    url = prepare_url(base_url, params)
    with open(audio_file_path, 'rb') as audio_file:
        files = [('audio', audio_file)]
        response = requests.post(url, files=files)
        
    if response.status_code == 200:
        return response.json()
    else:
        return response.text
