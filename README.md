# Whissle API Python Package

`whissle` is a Python package that provides easy access to the Whissle API for conversation, Speech-to-Text (STT), and Text-to-Speech (TTS) functionalities. 

## Features

- **Send Conversation Messages**: Send conversation content with emotion and receive intelligent responses.
- **Speech-to-Text (STT)**: Convert audio files (WAV format) into text.
- **Text-to-Speech (TTS)**: Convert text into audio files in WAV format.

## Installation

```
import whissle

# Set the auth token
whissle.set_auth_token("4db0b480a7b24be8")

# Use the conversation message function
response = whissle.send_message(
    conversation_history='[]',
    content='summarize the audio for me',
    emotion='EMOTION_SAD'
)
print(response)

# Speech-to-text functionality
stt_response = whissle.speech_to_text('/path/to/audio.wav')
print(stt_response)

# Text-to-speech functionality
tts_response = whissle.text_to_speech(
    text='Hello, this is an example.',
    output_filename='output.wav'
)
print(tts_response)
```


