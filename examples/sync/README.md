# Whissle Sync Client Example Script

## Overview

This example script demonstrates how to use the Whissle synchronous client for common operations. For asynchronous operations, see the async client example instead.

The script shows straightforward synchronous usage patterns for:
- Listing available ASR models
- Converting speech to text with customizable options
- Translating text between languages
- Summarizing text using LLM models

## Prerequisites

- Python 3.8+
- Whissle package
- python-dotenv

## Setup

1. Install required packages:
   ```bash
   pip install whissle python-dotenv
   ```

2. Create a `.env` file with your Whissle credentials

## Example Usage

The script demonstrates four main examples:

### 1. List ASR Models

```python
client = WhissleClient().sync_client
models = client.list_asr_models()
```

### 2. Speech to Text

```python
transcription = client.speech_to_text(
    "./data/sample.wav",
    model_name="en-US-0.6b",
    timestamps=False,
    boosted_lm_words=["reformer"],
    boosted_lm_score=80
)
```

### 3. Text Translation

```python
translation = client.machine_translation(
    "Hello, how are you today?",
    source_language="en",
    target_language="es"
)
```

### 4. Text Summarization

```python
summary = client.llm_text_summarizer(
    content=long_text,
    model_name="openai",
    instruction="Provide a brief summary"
)
```

## Implementation Details

The script demonstrates key sync patterns:
- Using `WhissleClient().sync_client` for synchronous operations
- Direct method calls without async/await
- Simple sequential execution flow
- Basic error handling approach

## Script Components

1. Client initialization with environment variables
2. Model listing demonstration
3. Speech-to-text conversion with optional parameters
4. Text translation between languages
5. Text summarization using LLM

## Key Differences from Async Client

- Uses `sync_client` instead of `async_client`
- Direct synchronous method calls
- No async/await syntax
- No asyncio requirements
- Sequential execution flow

## Notes

- This is specifically a sync client example - see async client example for asynchronous operations
- Error handling is minimal for demonstration purposes
- See Whissle documentation for complete API details
- The sample code assumes existence of "./data/sample.wav" - adjust path as needed
