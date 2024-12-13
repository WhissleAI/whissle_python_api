import os
from typing import List

import httpx

from .models import ASRModel, STTResponse, ASRModelList, MTResposne


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class WhissleClient:
    def __init__(self, auth_token: str = None):
        if not auth_token:
            # Try to get the token from environment variable
            auth_token = os.getenv("WHISSLE_AUTH_TOKEN")

        # Raise an error if no auth token is found
        if not auth_token:
            raise ValueError("No authentication token provided. Please pass an auth_token or set WHISSLE_AUTH_TOKEN environment variable.")

        self.auth_token = auth_token

        self.server_url = "https://api.whissle.ai/v1" or os.getenv("WHISSLE_SERVER_URL")
        self.httpx_client = httpx.AsyncClient(base_url=self.server_url)

    def _append_auth_token(self, url):
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}auth_token={self.auth_token}"

    async def authorized_get(self, url):
        """
        Perform an authorized API fetch with the necessary headers.

        Args:
            url (str): The API endpoint URL.

        Returns:
            Any: The API response JSON parsed into a Pydantic model.
        """
        headers = {
            "Content-Type": "application/json",
        }

        try:
            url = self._append_auth_token(url)
            response = await self.httpx_client.get(url, headers=headers)

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text)

    async def authorized_post(self, url, file=None, data=None):
        headers = {}

        try:
            url = self._append_auth_token(url)
            if file:
                response = await self.httpx_client.post(
                    url=url,
                    headers=headers,
                    data=data or {},
                    files={
                        'audio': ('file', open(file, 'rb'), 'application/octet-stream')
                    }
                )
            elif data:
                response = await self.httpx_client.post(
                    url=url,
                    headers={"Content-Type": "application/json"},
                    json=data
                )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text)
        
    async def list_asr_models(self) -> List[ASRModel]:
        response_data = await self.authorized_get(f"/list-asr-models")
        return response_data

    async def speech_to_text(
        self, audio_file_path, model_name: ASRModelList
    ) -> STTResponse:
        url = f"/conversation/STT?model_name={model_name}"
        response = await self.authorized_post(url, file=audio_file_path)
        return STTResponse(**response)
    
    async def machine_translation(self, text: str, target_language: str) -> MTResposne:
        url = f"/MT?target_language={target_language}"
        response = await self.authorized_post(url, data={"text": text})
        return MTResposne(**response)