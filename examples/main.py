import argparse
import asyncio

from dotenv import load_dotenv

from whissle import WhissleClient


async def list_models():
    """List available ASR models."""
    whissle = WhissleClient()
    models = await whissle.list_asr_models()
    print("Available ASR Models:")
    for model in models:
        print(model)


async def do_speech_to_text(file_path, model_name):
    """Convert speech to text using specified model."""
    whissle = WhissleClient()
    text = await whissle.speech_to_text(file_path, model_name=model_name)
    print(f"Transcription (using {model_name}):")
    print(text)


async def do_translation(text, source_language, target_language):
    """Translate text to target language."""
    whissle = WhissleClient()
    translation = await whissle.machine_translation(
        text, source_language=source_language, target_language=target_language
    )
    print(f"Translation from {source_language} to {target_language}:")
    print(translation)


async def llm_text_summarizer(content, model_name, instruction):
    """Summarize text using specified model."""
    whissle = WhissleClient()
    summary = await whissle.llm_text_summarizer(content, model_name, instruction)
    print(f"Summary (using {model_name}):")
    print(summary)


def main():
    # Load environment variables
    load_dotenv()

    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Whissle CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List models subcommand
    subparsers.add_parser("list-models", help="List available ASR models")

    # Speech to text subcommand
    parser_stt = subparsers.add_parser("speech-to-text", help="Convert speech to text")
    parser_stt.add_argument("file_path", help="Path to the audio file")
    parser_stt.add_argument(
        "--model", default="en-US-0.6b", help="ASR model name (default: en-US-0.6b)"
    )

    # Translation subcommand
    parser_trans = subparsers.add_parser("translate", help="Translate text")
    parser_trans.add_argument("text", help="Text to translate")
    parser_trans.add_argument(
        "--source", default="en", help="Source language (default: en)"
    )
    parser_trans.add_argument(
        "--target", default="es", help="Target language (default: es)"
    )

    # Summarization subcommand
    parser_sum = subparsers.add_parser("summarize", help="Summarize text")
    parser_sum.add_argument("content", help="Text to summarize")
    parser_sum.add_argument(
        "--model", default="openai", help="Model name (default: openai)"
    )
    parser_sum.add_argument(
        "--instruction", default="summarize", help="Instruction (default: summarize)"
    )

    # Parse arguments
    args = parser.parse_args()

    # Run appropriate async function based on command
    if args.command == "list-models":
        asyncio.run(list_models())
    elif args.command == "speech-to-text":
        asyncio.run(do_speech_to_text(args.file_path, args.model))
    elif args.command == "translate":
        asyncio.run(do_translation(args.text, args.source, args.target))
    elif args.command == "summarize":
        asyncio.run(llm_text_summarizer(args.content, args.model, args.instruction))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
