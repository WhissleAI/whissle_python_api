# Whissle Examples

This directory contains example implementations of the Whissle client, demonstrating both synchronous and asynchronous usage patterns.

## Directory Structure

```
examples/
├── async/
│   ├── README.md
│   └── whissle_cli.py
├── sync/
│   ├── README.md
│   └── whissle_example.py
└── README.md (this file)
```

## Choosing an Implementation

### Synchronous Client (`/sync`)
Choose this implementation if you:
- Want simple, straightforward code
- Are building a script that runs tasks sequentially
- Don't need to handle multiple operations concurrently
- Are new to Python or prefer simpler implementations
- Don't require non-blocking operations

Example of sync usage:
```python
from whissle import WhissleClient

client = WhissleClient().sync_client
result = client.speech_to_text("audio.wav")
```

### Asynchronous Client (`/async`)
Choose this implementation if you:
- Need to handle multiple operations concurrently
- Are building a web application or API
- Want to maximize performance for I/O-bound operations
- Are comfortable with async/await patterns
- Need non-blocking operations

Example of async usage:
```python
from whissle import WhissleClient
import asyncio

async def main():
    client = WhissleClient().async_client
    result = await client.speech_to_text("audio.wav")

asyncio.run(main())
```

## Features Demonstrated

Both implementations showcase:
- ASR model listing
- Speech to text conversion
- Machine translation
- Text summarization using LLMs

## Getting Started

1. Choose your preferred implementation (sync or async)
2. Navigate to the corresponding directory
3. Follow the README in that directory for specific setup and usage instructions

## Prerequisites

- Python 3.8+
- Whissle package
- python-dotenv
- asyncio (for async implementation only)

## Additional Resources

- Main Whissle Documentation: Visit the main package documentation
- API Reference: See the API documentation for detailed method signatures
- Support: Contact the maintainers for additional help
