import requests
from .config import get_auth_token

def text_to_speech(text, output_filename='output.wav'):
    base_url = 'https://api.whissle.ai/v0/conversation/TTS'
    params = {'auth_token': get_auth_token()}
    
    files = {
        'text': (None, text),
        'output_filename': (None, output_filename)
    }

    response = requests.post(f"{base_url}?auth_token={params['auth_token']}", files=files)
    
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        return f"File saved as {output_filename}"
    else:
        return f"Error: {response.status_code}, {response.text}"
