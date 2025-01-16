# Whissle Async Client Example Script

## Overview

This example script demonstrates how to use the Whissle asynchronous client to perform common operations asynchronously. For synchronous operations, see the sync client example instead.

The script showcases async/await patterns for:
- Listing available ASR models
- Converting speech to text with customizable options
- Translating text between languages
- Summarizing text using LLM models

## Prerequisites

- Python 3.8+
- Whissle package
- python-dotenv
- asyncio

## Setup

1. Install required packages:
   ```bash
   pip install whissle python-dotenv
   ```

2. Create a `.env` file with your Whissle credentials

## Example Usage

### List Available ASR Models

```bash
python whissle_cli.py list-models
```

The script will asynchronously fetch and display available models.

### Async Speech to Text

Basic usage:
```bash
python whissle_cli.py speech-to-text audio_file.wav
```

With async options:
```bash
python whissle_cli.py speech-to-text audio_file.wav \
    --model en-US-0.6b \
    --timestamps \
    --boosted-lm-words python programming \
    --boosted-lm-score 5
```

### Async Text Translation

```bash
python whissle_cli.py translate "Hello, world!" --source en --target es
```

### Async Text Summarization

```bash
python whissle_cli.py summarize "Your text to summarize" \
    --model openai \
    --instruction "summarize"
```

## Async Implementation Details

The script demonstrates key async patterns:
- Using `WhissleClient().async_client` for async operations
- Implementing async functions with `async/await`
- Running async operations with `asyncio.run()`
- Structuring CLI commands to work with async functions

## Script Components

1. `async list_models()`: Asynchronously fetches available ASR models
2. `async do_speech_to_text()`: Performs async speech-to-text conversion
3. `async do_translation()`: Handles async text translation
4. `async llm_text_summarizer()`: Demonstrates async text summarization
5. `main()`: Orchestrates async operations using asyncio

## Key Differences from Sync Client

- Uses `async_client` instead of regular client methods
- All operations are async/await based
- Uses `asyncio.run()` to execute async functions
- Designed for non-blocking operations

## Notes

- This is specifically an async client example - see sync client example for synchronous operations
- Error handling is minimal for clarity
- See Whissle documentation for complete API details
