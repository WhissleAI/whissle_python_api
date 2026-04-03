"""Synchronous client for the Whissle HTTP gateway (api.whissle.ai style: Bearer tokens, /asr/*, etc.)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

import httpx

from .clients.errors import HttpError


class WhissleGatewayClient:
    """
    Call the production Whissle gateway with ``Authorization: Bearer wh_…``.

    This is separate from :class:`WhissleClient`, which targets the legacy query-token API
    (see ``WhissleClientOptions.server_url`` defaults).
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        *,
        base_url: str = "https://api.whissle.ai",
        timeout: float = 120.0,
    ):
        if api_token is None:
            api_token = os.getenv("WHISSLE_API_TOKEN") or os.getenv("WHISSLE_AUTH_TOKEN", "")
        if not api_token:
            raise ValueError(
                "api_token required, or set WHISSLE_API_TOKEN / WHISSLE_AUTH_TOKEN in the environment."
            )
        self._token = api_token
        base = base_url.rstrip("/")
        self._client = httpx.Client(base_url=base, timeout=httpx.Timeout(timeout))

    @property
    def base_url(self) -> str:
        return str(self._client.base_url)

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> WhissleGatewayClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def validate_token(self) -> Dict[str, Any]:
        """GET ``/backend/api-tokens/validate`` — returns e.g. ``valid``, ``deviceId``."""
        try:
            r = self._client.get(
                "/backend/api-tokens/validate",
                params={"token": self._token},
            )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text) from e

    def transcribe_file(
        self,
        file_path: Union[str, Path],
        *,
        extra_form: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        POST ``/asr/transcribe`` — multipart upload (WAV, etc.).

        ``extra_form`` maps to multipart fields, e.g.
                            ``language``, ``hotwords``, ``use_lm``, ``beam_width``, ``neuropsych_mode``.
        """
        path = Path(file_path)
        data = {k: str(v) for k, v in (extra_form or {}).items()}
        try:
            with path.open("rb") as f:
                files = {"file": (path.name, f, "application/octet-stream")}
                r = self._client.post(
                    "/asr/transcribe",
                    headers=self._auth_headers(),
                    files=files,
                    data=data,
                )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text) from e

    def transcribe_pcm(
        self,
        file_path: Union[str, Path],
        *,
        sample_rate: int = 16000,
        channels: int = 1,
        bit_depth: int = 16,
        extra_form: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """POST ``/asr/transcribe/pcm`` — raw PCM as ``file`` field."""
        path = Path(file_path)
        data: Dict[str, Any] = {
            "sample_rate": str(sample_rate),
            "channels": str(channels),
            "bit_depth": str(bit_depth),
        }
        data.update({k: str(v) for k, v in (extra_form or {}).items()})
        try:
            with path.open("rb") as f:
                files = {"file": (path.name, f, "application/octet-stream")}
                r = self._client.post(
                    "/asr/transcribe/pcm",
                    headers=self._auth_headers(),
                    files=files,
                    data=data,
                )
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text) from e

    def post_json(
        self,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        *,
        extra_headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        POST JSON with Bearer auth. Returns the raw ``httpx.Response``.

        Use ``extra_headers`` e.g. ``{"Accept": "text/event-stream"}`` for ``/agent/route/stream``.
        """
        p = path if path.startswith("/") else f"/{path}"
        headers = {**self._auth_headers(), "Content-Type": "application/json"}
        if extra_headers:
            headers.update(extra_headers)
        return self._client.post(p, headers=headers, json=json_body or {}, **kwargs)
