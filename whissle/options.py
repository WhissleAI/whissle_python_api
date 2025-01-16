import re
from typing import Optional


class WhissleClientOptions:
    def __init__(self, auth_token: str = None, server_url: Optional[str] = None):
        self.auth_token = auth_token

        if not server_url:
            # Try to get the server url from environment variable
            server_url = "https://api.whissle.ai/v1"

        self.server_url = self._get_url(server_url)

    def set_authtoken(self, auth_token: str):
        """
        set_authtoken: Sets the API key for the client.

        Args:
            auth_token: The Whissle API key used for authentication.
        """
        self.auth_token = auth_token

    def _get_url(self, url) -> str:
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = "https://" + url
        return url.strip("/")
