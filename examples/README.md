# Whissle CLI Tool Examples

## Overview

This CLI tool demonstrates the capabilities of the Whissle package, providing easy-to-use interfaces for:
- Listing available Automatic Speech Recognition (ASR) models
- Converting speech to text
- Translating text between languages

## Prerequisites

- Python 3.8+
- Whissle package installed
- Environment variables configured (see main package documentation)

## Installation

1. Ensure you have the Whissle package installed:
   ```
   pip install whissle
   ```

2. Set up your environment variables (if required)

## Usage

### List Available ASR Models

```bash
python whissle_cli.py list-models
```

This command will display all available Automatic Speech Recognition models supported by Whissle.

### Speech to Text Conversion

```bash
python whissle_cli.py speech-to-text /path/to/audio/file.wav
```

Optional arguments:
- `--model`: Specify a custom ASR model (default: en-US-0.6b)

Example:
```bash
python whissle_cli.py speech-to-text /recordings/interview.mp3 --model en-US-large
```

### Text Translation

```bash
python whissle_cli.py translate "Hello, world!" --target es
```

Optional arguments:
- `--target`: Target language code (default: es for Spanish)

Example:
```bash
python whissle_cli.py translate "Good morning" --target fr
```

## Common Use Cases

- Transcribe audio files from various languages
- Translate transcribed text
- Explore available ASR models

## Troubleshooting

- Ensure audio files are in a supported format (.wav, .mp4 file support only)
- Check that your environment variables are correctly set