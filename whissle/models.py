from pydantic import BaseModel
from typing import Literal


class ASRModel(BaseModel):
    model: str

class STTResponse(BaseModel):
    transcript: str
    duration_seconds: float

class MTResposne(BaseModel):
    translated_text: str


ASRModelList = Literal[
    "en-US-0.6b",
    "em-ea-1.1b",
    "en-US-NER",
    "en-US-300m",
    "hi-IN-NER",
    "ia-IN-NER",
    "ru-RU-300m",
    "en-US-IoT-NER",
]
