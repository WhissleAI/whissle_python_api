import requests
from .config import get_auth_token
from .utils import prepare_url

def send_message(conversation_history, content, emotion, model_name='whissle'):
    base_url = "https://api.whissle.ai/v1/conversation/message"
    params = {
        'auth_token': get_auth_token()
    }
    payload = {
        'model_name': model_name,
        'conversation_history': conversation_history,
        'content': content,
        'emotion': emotion,
        'system_instruction': 'Give intelligent answer.'
    }
    url = prepare_url(base_url, params)

    files = [('input_file', open('path_to_audio_file.wav', 'rb'))]

    response = requests.post(url, data=payload, files=files)
    return response.json()
