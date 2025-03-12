import os
from typing import Optional

from whissle.clients.async_client import AsyncWhissleClient
from whissle.clients.client import SyncWhissleClient

from .options import WhissleClientOptions


class WhissleClient:
    def __init__(
        self,
        auth_token: str = None,
        config: Optional[WhissleClientOptions] = None,
    ):
        if auth_token is None:
            auth_token = os.getenv("WHISSLE_AUTH_TOKEN", "")

        if auth_token is None and config is not None:
            auth_token = config.auth_token

        if auth_token == "":
            raise ValueError(
                "No authentication token provided. Please pass an auth_token or set WHISSLE_AUTH_TOKEN environment variable."
            )

        self.auth_token = auth_token

        if config is None:  # Use default configuration
            self._config = WhissleClientOptions(auth_token=self.auth_token)
        else:
            config.set_authtoken(self.auth_token)
            self._config = config

    @property
    def sync_client(self):
        """
        Returns a Listen dot-notation router for interacting with Deepgram's transcription services.
        """
        return SyncWhissleClient(self._config)

    @property
    def async_client(self):
        """
        Returns a Read dot-notation router for interacting with Deepgram's read services.
        """
        return AsyncWhissleClient(self._config)
