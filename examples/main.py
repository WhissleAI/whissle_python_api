from dotenv import load_dotenv
from whissle import WhissleClient

import asyncio

async def main():
    load_dotenv()

    whissle = WhissleClient()

    text = await whissle.speech_to_text("./data/sample.wav", model_name="en-US-0.6b")
    print(text)

if __name__ == "__main__":
    asyncio.run(main())