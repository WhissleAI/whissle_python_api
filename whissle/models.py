from typing import List, Literal, Optional

from pydantic import BaseModel


class ASRModel(BaseModel):
    model: str


class STTResponse(BaseModel):
    transcript: str
    duration_seconds: float
    language_code: Optional[str]
    timestamps: Optional[List]

class DiarizeSTTResponse(BaseModel):
    transcript: str
    duration_seconds: float
    language_code: Optional[str]
    diarize_output: Optional[List]
    timestamps: Optional[List]  # For Normal STT


class MTResposne(BaseModel):
    translated_text: str


class LLMSummarizerResponse(BaseModel):
    response: str
    input_text: str
    input_tokens: int
    output_tokens: int


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
