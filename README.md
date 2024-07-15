# Whissle python API Client

```
pip import whissle
```

### python requirements (for pushing to pypi)

Ensure you have `twine` installed:

```bash
pip install twine
```

Build and publish
```
python setup.py sdist bdist_wheel
twine upload dist/*
```

### Usage 

```
from whissle.client import WhissleClient

client = WhissleClient(base_url="https://whissle.ai")

# Create a conversation
response = client.create_conversation(email="user@example.com")
print(response)

# Send a message
response = client.send_message(
    conversation_id="12345",
    content="Hello, how are you?",
    emotion="happy",
    model_name="whissle",
    searchengine="google",
    system_instruction="Provide a friendly response",
    url="https://example.com",
    conversation_history=[]
)
print(response)

# Fetch a conversation
response = client.fetch_conversation(conversation_id="12345")
print(response)

# Fetch all conversations for a user
response = client.fetch_all_conversations(email="user@example.com")
print(response)


```
