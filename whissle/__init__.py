from .config import set_auth_token
from .conversation import send_message
from .whissle.stt import speech_to_text
from .whissle.tts import text_to_speech

__all__ = ['set_auth_token', 'send_message', 'speech_to_text', 'text_to_speech']

from .client import WhissleSTTClient
from .exceptions import WhissleSTTError

__all__ = ['WhissleSTTClient', 'WhissleSTTError']
__version__ = '0.1.0'
