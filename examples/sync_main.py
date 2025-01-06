from dotenv import load_dotenv

from whissle import WhissleClient


def main():
    load_dotenv()

    # Initialize the client
    client = WhissleClient().sync_client

    # Example 1: List available ASR models
    print("\n=== Listing ASR Models ===")
    models = client.list_asr_models()
    for model in models:
        print(f"Available model: {model}")

    # Example 2: Speech to Text conversion
    print("\n=== Speech to Text Example ===")
    audio_file = "./data/sample.wav"
    transcription = client.speech_to_text(
        audio_file,
        model_name="en-US-0.6b",  # You can use any model from list_asr_models()
    )
    print(f"Transcription: {transcription}")

    # Example 3: Machine Translation
    print("\n=== Translation Example ===")
    text_to_translate = "Hello, how are you today?"
    translation = client.machine_translation(
        text_to_translate, source_language="en", target_language="es"
    )
    print(f"Original: {text_to_translate}")
    print(f"Translation: {translation}")

    # Example 4: Text Summarization
    print("\n=== Text Summarization Example ===")
    long_text = """
    The Industrial Revolution was a period of major industrialization and
    innovation during the late 18th and early 19th centuries. The Industrial
    Revolution began in Great Britain and quickly spread throughout Europe
    and the United States. It revolutionized the production of textiles and
    iron products, while also improving transportation and communication systems.
    """
    summary = client.llm_text_summarizer(
        content=long_text, model_name="openai", instruction="Provide a brief summary"
    )
    print(f"Original text length: {len(long_text)} characters")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()
