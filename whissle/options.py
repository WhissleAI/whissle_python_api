import re
from typing import Optional


class WhissleClientOptions:
    """Options for :class:`WhissleClient` (legacy API — not the Bearer gateway)."""

    def __init__(self, auth_token: str = None, server_url: Optional[str] = None):
        self.auth_token = auth_token

        if not server_url:
            # Legacy service base URL (query-string auth). Use WhissleGatewayClient for api.whissle.ai Bearer routes.
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
