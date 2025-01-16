# Whissle API Python Package

`whissle` is a Python package that provides easy access to the Whissle API for conversation, Speech-to-Text (STT), and Text-to-Speech (TTS) functionalities.

## Features (Current)

- 🔊 Speech-to-Text (STT) conversion with multiple model support
- 🌍 Machine Translation across various languages
- Summarization

## Installation

Install Whissle using pip:

```bash
pip install whissle
```

Install Whissle locally:

```bash
pip install -e .
```

## Authentication

To use Whissle, you need an authentication token. You can provide this in two ways:

1. Directly when initializing the client:
```python
from whissle import WhissleClient

client = WhissleClient(auth_token="your_auth_token_here")
```

2. Set as an environment variable:
```bash
export WHISSLE_AUTH_TOKEN=your_auth_token_here
```

## Usage Examples

### List Available ASR Models

```python
models = await client.async_client.list_asr_models()
print(models)
```

### Speech-to-Text Conversion

```python
response = await client.speech_to_text(
        audio_file_path="path/to/your/audio.wav",
        model_name="en-US-0.6b"
    )
print(response.text)
```

### Machine Translation

```python
translation = await client.machine_translation(
        text="Hello, world!",
        target_language="es"
    )
print(translation.translated_text)
```

## Configuration

- `WHISSLE_AUTH_TOKEN`: Your authentication token
- `WHISSLE_SERVER_URL`: Optional custom server URL (defaults to https://api.whissle.ai/v1)

## Error Handling

The library raises a `HttpError` for API-related issues:

```python
from whissle import HttpError

try:
    # Whissle API calls
except HttpError as e:
    print(f"API Error: {e.status_code} - {e.message}")
```

## Dependencies

- Python 3.8+
- httpx
- pydantic

## Contributing

Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.

## Contact

For support or inquiries, contact: nsanda@whissle.ai
