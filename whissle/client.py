import requests

class WhissleClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_conversation(self, email):
        params = {'email': email}
        response = requests.post(f"{self.base_url}/v0/conversation/create", params=params)
        response.raise_for_status()
        return response.json()

    def send_message(self, conversation_id, content, emotion=None, model_name=None, searchengine=None, 
                     system_instruction=None, url=None, conversation_history=None):
        data = {
            'conversation_id': conversation_id,
            'content': content,
            'emotion': emotion,
            'model_name': model_name,
            'searchengine': searchengine,
            'system_instruction': system_instruction,
            'url': url,
            'conversation_history': conversation_history
        }
        response = requests.post(f"{self.base_url}/v0/conversation/message", json=data)
        response.raise_for_status()
        return response.json()

    def fetch_conversation(self, conversation_id):
        params = {'conversation_id': conversation_id}
        response = requests.get(f"{self.base_url}/v0/conversation/chat", params=params)
        response.raise_for_status()
        return response.json()

    def fetch_all_conversations(self, email):
        params = {'email': email}
        response = requests.get(f"{self.base_url}/v0/conversation/all", params=params)
        response.raise_for_status()
        return response.json()
