import requests

class WhissleClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_conversation(self, data):
        response = requests.post(f"{self.base_url}/v0/conversation/create", json=data)
        return response.json()

    def send_message(self, data):
        response = requests.post(f"{self.base_url}/v0/conversation/message", json=data)
        return response.json()

    def fetch_conversation(self, params=None):
        response = requests.get(f"{self.base_url}/v0/conversation/chat", params=params)
        return response.json()

    def fetch_all_conversations(self):
        response = requests.get(f"{self.base_url}/v0/conversation/all")
        return response.json()