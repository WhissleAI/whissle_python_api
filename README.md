# Whissle API Python Package

`whissle` is a Python package for the **Whissle production gateway** (`https://api.whissle.ai`, Bearer `wh_…` tokens) and a **legacy** HTTP API used by some internal flows (query-param auth, different paths).

## Features

- 🌐 **`WhissleGatewayClient` / `WhissleGatewayAsyncClient`** — transcribe, validate token, and generic JSON posts against the public gateway
- 🎙️ **Legacy** Speech-to-Text (STT) with multiple model support and customization options
- 🗣️ Speaker Diarization for multi-speaker audio transcription
- 🌍 Machine Translation across various languages
- 📝 Text Summarization using LLM models
- ⚡ Both synchronous and asynchronous clients
- 🔄 Automatic response parsing to Pydantic models

## Installation

Install Whissle using pip:
```bash
pip install whissle
```

For local development:
```bash
pip install -e .
```

## Production gateway client

Use **`WhissleGatewayClient`** for the same HTTP API documented at [api.whissle.ai/redoc](https://api.whissle.ai/redoc). Tokens are **`wh_…`** (create them from [browser.whissle.ai/access](https://browser.whissle.ai/access)).

```bash
export WHISSLE_API_TOKEN=wh_your_token_here
```

```python
from whissle import WhissleGatewayClient

with WhissleGatewayClient() as gw:
    print(gw.validate_token())
    result = gw.transcribe_file(
        "recording.wav",
        extra_form={"language": "en", "use_lm": "true", "hotwords": "Acme,SKU-42"},
    )
    print(result.get("transcript"))
```

Async:

```python
from whissle import WhissleGatewayAsyncClient

async with WhissleGatewayAsyncClient() as gw:
    j = await gw.validate_token()
```

For **SSE** (e.g. `POST /agent/route/stream`), use `post_json(..., extra_headers={"Accept": "text/event-stream"})` and read `response.text` or iterate the stream — see `httpx` streaming docs.

---

## Legacy client authentication

The **`WhissleClient`** class targets the **legacy** service (default base URL may include `/v1`, **`auth_token` query parameter**). Use only if you still integrate with that backend.

Provide your authentication token in one of two ways:

1. Direct initialization:
```python
from whissle import WhissleClient

client = WhissleClient(auth_token="your_auth_token_here")
```

2. Environment variable:
```bash
export WHISSLE_AUTH_TOKEN=your_auth_token_here
```

## Legacy client options

### Synchronous legacy client
Use the sync client for straightforward, sequential operations:

```python
from whissle import WhissleClient

client = WhissleClient().sync_client

# List ASR models
models = client.list_asr_models()

# Speech to text
response = client.speech_to_text(
    audio_file_path="audio.wav",
    model_name="en-US-0.6b",
    timestamps=True,
    boosted_lm_words=["specific", "terms"],
    boosted_lm_score=80
)

# Translation
translation = client.machine_translation(
    text="Hello, world!",
    source_language="en",
    target_language="es"
)

# Summarization
summary = client.llm_text_summarizer(
    content="Long text here...",
    model_name="openai",
    instruction="Provide a brief summary"
)

# Speech to text with speaker diarization
diarized_response = client.diarize_stt(
    audio_file_path="multi_speaker_audio.wav",
    model_name="en-US-0.6b",
    max_speakers=2,
    boosted_lm_words=["specific", "terms"],
    boosted_lm_score=80
)
```

### Asynchronous legacy client
Use the async client for concurrent operations and non-blocking I/O:

```python
import asyncio
from whissle import WhissleClient

async def main():
    client = WhissleClient().async_client

    # List ASR models
    models = await client.list_asr_models()

    # Speech to text
    response = await client.speech_to_text(
        audio_file_path="audio.wav",
        model_name="en-US-0.6b",
        timestamps=True
    )

    # Translation
    translation = await client.machine_translation(
        text="Hello, world!",
        source_language="en",
        target_language="es"
    )

    # Summarization
    summary = await client.llm_text_summarizer(
        content="Long text here...",
        model_name="openai",
        instruction="Provide a brief summary"
    )

    # Speech to text with speaker diarization
    diarized_response = await client.diarize_stt(
        audio_file_path="multi_speaker_audio.wav",
        model_name="en-US-0.6b",
        max_speakers=2
    )

asyncio.run(main())
```

## API Methods

### List ASR Models
```python
models = client.list_asr_models()  # or await client.list_asr_models()
```

### Speech-to-Text
```python
response = client.speech_to_text(
    audio_file_path="path/to/audio.wav",
    model_name="en-US-0.6b",
    timestamps=False,  # Optional: Include word timestamps
    boosted_lm_words=["specific", "terms"],  # Optional: Boost specific words
    boosted_lm_score=80  # Optional: Boosting score
)
```

### Speaker Diarization with Speech-to-Text
```python
response = client.diarize_stt(
    audio_file_path="path/to/multi_speaker_audio.wav",
    model_name="en-US-0.6b",
    max_speakers=2,  # Optional: Maximum number of speakers to identify
    boosted_lm_words=["specific", "terms"],  # Optional: Boost specific words
    boosted_lm_score=80  # Optional: Boosting score
)
```

### Machine Translation
```python
translation = client.machine_translation(
    text="Hello, world!",
    source_language="en",
    target_language="es"
)
```

### Text Summarization
```python
summary = client.llm_text_summarizer(
    content="Your long text here...",
    model_name="openai",
    instruction="Provide a brief summary"
)
```

## Configuration

**Gateway**

- `WHISSLE_API_TOKEN` or `WHISSLE_AUTH_TOKEN`: Bearer token (`wh_…`) for `WhissleGatewayClient`

**Legacy**

- `WHISSLE_AUTH_TOKEN`: Legacy API token
- `WHISSLE_SERVER_URL`: Optional custom legacy base URL (default `https://api.whissle.ai/v1`)

## Error Handling

The library provides consistent error handling for both sync and async clients:

```python
from whissle import HttpError

try:
    # Whissle API calls
except HttpError as e:
    print(f"API Error: {e.status_code} - {e.message}")
```

## Dependencies

- Python 3.8+
- httpx: For HTTP requests (both sync and async)
- pydantic: For response modeling

## Type Hints

All methods include proper type hints for better IDE support:
- `ASRModel`: ASR model information
- `STTResponse`: Speech-to-text response
- `MTResposne`: Machine translation response
- `LLMSummarizerResponse`: Text summarization response
- `DiarizeSTTResponse`: Speech-to-text with speaker diarization response

## Examples

For more detailed examples, check out the `examples/` directory:
- `examples/sync/`: Synchronous client examples
- `examples/async/`: Asynchronous client examples

## Publishing (maintainers)

```bash
pip install build twine
python -m build
twine upload dist/*
```

Bump `version` in `pyproject.toml` and `__version__` in `whissle/__init__.py` before each release.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.

## Contact

For support or inquiries, contact: nsanda@whissle.ai
