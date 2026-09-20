"""``whissle`` is deprecated. The client lives in ``whissle-sdk`` now.

This distribution no longer contains an API client. It contains this notice.

The clients it used to ship (``WhissleClient``, ``WhissleGatewayClient``,
``WhissleGatewayAsyncClient``) called ``https://api.whissle.ai``, which no
longer serves the Whissle API — every path on that host answers ``404``,
including the host root. They also authenticated with a ``wh_`` legacy
gateway *device token*, which is not something a customer can create. So
there was nothing left to point them at: the endpoints they wrapped
(``/v1`` speech-to-text, machine translation, summarisation, the
``/backend/api-tokens/validate`` door) do not exist on the live platform
under any URL.

What replaced them is a different, maintained package::

    pip install whissle-sdk

    from whissle_sdk import WhissleClient

    w = WhissleClient()                     # reads WHISSLE_API_KEY
    w.asr.transcribe("audio.wav", diarize=True)

It authenticates with a workspace **secret** key (``wsk_…``) that you create
yourself in your Whissle workspace settings, and it covers both the Voice
Agents platform API and Whissle's own speech-to-text, including the
diarisation and summarisation this package used to reach.

Note that ``whissle_sdk`` also exports a class named ``WhissleClient``. It is
not this one, and it does not take the same arguments — see that package's
README for the call shapes.
"""

from __future__ import annotations

import warnings

__version__ = "0.2.0"

#: The distribution that replaces this one, and the name you import from it.
REPLACEMENT_DISTRIBUTION = "whissle-sdk"
REPLACEMENT_IMPORT = "whissle_sdk"

__all__ = ["REPLACEMENT_DISTRIBUTION", "REPLACEMENT_IMPORT", "__version__"]

_SUMMARY = (
    "The `whissle` package is deprecated and no longer ships a client. "
    "Install `whissle-sdk` and import `whissle_sdk` instead."
)

_GUIDANCE = """\
{what} is gone from `whissle`. This distribution is now a deprecation notice,
not a client: the hosts it called (api.whissle.ai) return 404 for every path,
and the `wh_` device token it used is not self-serve.

Use the maintained SDK instead:

    pip uninstall whissle
    pip install whissle-sdk

    from whissle_sdk import WhissleClient

    w = WhissleClient()                     # reads WHISSLE_API_KEY
    w.asr.transcribe("audio.wav", diarize=True)

Authentication is a workspace secret key (`wsk_...`) you create in your
Whissle workspace settings. `whissle_sdk.WhissleClient` is a DIFFERENT class
from the one this package exported and takes different arguments; see the
`whissle-sdk` README.
"""

# Everything this package exported at 0.1.0 and at the published 0.0.1. Each
# one is intercepted by name so that an existing `from whissle import X`
# fails with the paragraph above instead of a confusing network error at the
# first call.
_RETIRED = {
    "WhissleClient": "`WhissleClient` (the legacy /v1 client)",
    "WhissleGatewayClient": "`WhissleGatewayClient`",
    "WhissleGatewayAsyncClient": "`WhissleGatewayAsyncClient`",
    "WhissleClientOptions": "`WhissleClientOptions`",
    "SyncWhissleClient": "`SyncWhissleClient`",
    "AsyncWhissleClient": "`AsyncWhissleClient`",
    "HttpError": "`HttpError`",
    "ASRModel": "`ASRModel`",
    "ASRModelList": "`ASRModelList`",
    "STTResponse": "`STTResponse`",
    "DiarizeSTTResponse": "`DiarizeSTTResponse`",
    "MTResposne": "`MTResposne`",
    "LLMSummarizerResponse": "`LLMSummarizerResponse`",
    # Submodules that used to exist. Named here so `whissle.client` explains
    # itself; `import whissle.client` still raises ModuleNotFoundError, which
    # the stub modules beside this file turn into the same paragraph.
    "client": "The `whissle.client` module",
    "clients": "The `whissle.clients` package",
    "gateway_client": "The `whissle.gateway_client` module",
    "gateway_async_client": "The `whissle.gateway_async_client` module",
    "models": "The `whissle.models` module",
    "options": "The `whissle.options` module",
}


def _message(name: str) -> str:
    return _GUIDANCE.format(what=_RETIRED.get(name, f"`whissle.{name}`"))


def __getattr__(name: str) -> object:
    """Explain the move for anything the old package used to expose.

    Raising :class:`ImportError` rather than :class:`AttributeError` matters:
    ``from whissle import WhissleClient`` propagates it verbatim, so the
    reader sees the migration note and not Python's generic
    "cannot import name" line.
    """
    if name.startswith("__") and name.endswith("__"):
        # Let dunder probes (``__path__``, ``__wrapped__``, pickling, doctest
        # collection) fail the ordinary way; they are not user code asking
        # for a client.
        raise AttributeError(f"module 'whissle' has no attribute {name!r}")
    raise ImportError(_message(name))


def __dir__() -> list:
    return sorted(set(__all__) | set(_RETIRED))


warnings.warn(_SUMMARY, DeprecationWarning, stacklevel=2)
