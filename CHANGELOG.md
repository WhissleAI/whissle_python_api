# Changelog

All notable changes to the `whissle` PyPI package. This project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2.0 — 2026-09-20

**`whissle` is deprecated. The client is now `whissle-sdk` (import `whissle_sdk`).**
This release is a signpost, not a client, and it is intended to be the last one.

### Breaking

- **Every client class is gone.** `WhissleClient`, `WhissleGatewayClient`,
  `WhissleGatewayAsyncClient`, `WhissleClientOptions`, `HttpError` and the response
  models no longer exist. Importing any of them raises `ImportError` carrying the
  install line for `whissle-sdk` and the equivalent call.
  `ImportError` and not `AttributeError`, because `from whissle import X` propagates
  the former verbatim and swallows the latter into Python's generic
  "cannot import name" message.
- **Every submodule is gone.** `whissle.client`, `whissle.clients`, `whissle.models`,
  `whissle.options`, `whissle.gateway_client`, `whissle.gateway_async_client` survive
  only as stubs that raise the same note, so a deeper import is explained rather than
  answered with `ModuleNotFoundError`.
- `import whissle` still succeeds and now emits a `DeprecationWarning`.
  `whissle.__version__` and `help(whissle)` still read.
- `examples/` is removed. Every example called a host that no longer answers.

### Why

The package was wholly non-functional, not merely stale. Checked on 2026-09-20:
`api.whissle.ai` returns `404` for `/`, `/v1`, `/redoc`, `/asr/transcribe` and
`/backend/api-tokens/validate`; `browser.whissle.ai`, where the README sent readers
for a token, does not resolve. The `wh_` token type it used is a legacy gateway
*device* token that a customer cannot self-serve; the keys a customer can create are
`wsk_` (workspace secret) and `wpk_` (publishable).

Repointing at the live platform was considered and rejected. The surface this package
wrapped largely has no live equivalent, the part that does (transcription, with
diarisation and summarisation) is already in `whissle-sdk`, and maintaining a second
Python client for one platform is how the drift being fixed here happens again.
Both packages export a class named `WhissleClient`, so leaving two live clients in
place would entrench an autocomplete trap rather than resolve it.

### Fixed

- **The licence contradiction.** `pyproject.toml` declared the
  `License :: OSI Approved :: MIT License` classifier while `LICENSE` in the same
  directory was GPL-3 — and both went out: `whissle` 0.0.1 on PyPI carries the full
  GPL-3 text in its `License:` field *and* the MIT classifier. `LICENSE` is now MIT,
  declared as a PEP 639 `license = "MIT"` expression with `license-files`, and the
  OSI classifier is dropped (PEP 639 forbids pairing the two, and PyPI rejects
  uploads that do). MIT is the original intent: the classifier predates the GPL-3
  file by a month, every sibling Whissle SDK is MIT, and MIT is the reading that
  takes nothing back from anyone who already installed 0.0.1.
- **Dead metadata.** `Documentation` pointed at `api.whissle.ai/redoc` (404). Project
  URLs now point at this repository and `whissle.ai`.
- **Packaging.** `requires-python` was `>3.8`, which excludes Python 3.8 itself;
  it is now `>=3.8`. The package explicitly lists what it ships instead of relying
  on discovery.

### Removed

- All runtime dependencies. `httpx`, `pydantic` and `python-dotenv` were needed by
  the client; a deprecation notice needs nothing, and `pip install whissle` no longer
  pulls a dependency tree.

## 0.1.0 — unreleased

Added `WhissleGatewayClient` / `WhissleGatewayAsyncClient` for the Bearer gateway.
Never published to PyPI; superseded by 0.2.0.

## 0.0.1 — 2025-04

Initial and only published release. Speech-to-text, speaker diarization, machine
translation and LLM summarisation against `api.whissle.ai`, authenticated with a
`wh_` token. Non-functional since that host stopped serving the API.
