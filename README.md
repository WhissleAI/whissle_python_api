# Whissle python API Client

```
pip import whissle
```

### python requirements (for pushing to pypi)

Ensure you have `twine` installed:

```bash
pip install twine
```

Build your package
```
python setup.py sdist bdist_wheel
```
Push to Pypi
```
twine upload dist/*
```
### Usage 

```
from whissle.client import WhissleClient

client = WhissleClient(base_url="https://whissle.ai")

# Create a conversation
response = client.create_conversation(data={"key": "value"})
print(response)

# Send a message
response = client.send_message(data={"key": "value"})
print(response)

# Fetch a conversation
response = client.fetch_conversation(params={"key": "value"})
print(response)

# Fetch all conversations
response = client.fetch_all_conversations()
print(response)

```
