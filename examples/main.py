from dotenv import load_dotenv
from whissle import WhissleClient

import asyncio

async def main():
    load_dotenv()

    whissle = WhissleClient()

    models = await whissle.list_asr_models()
    print(models)

    text = await whissle.speech_to_text("./data/sample.wav", model_name="en-US-0.6b")
    print(text)

    translation = await whissle.machine_translation("Hello, how are you?", target_language="es")
    print(translation)

if __name__ == "__main__":
    asyncio.run(main())