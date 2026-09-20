# whissle — deprecated, use `whissle-sdk`

**This package is no longer a Whissle client.** It is a pointer to the one that is.

```bash
pip uninstall whissle
pip install whissle-sdk
```

```python
from whissle_sdk import WhissleClient

w = WhissleClient()                          # reads WHISSLE_API_KEY
w.asr.transcribe("audio.wav", diarize=True)  # speech-to-text, with the metadata heads
```

## Why

`whissle` wrapped an HTTP API at `api.whissle.ai` and authenticated with a `wh_` token. Neither
of those exists for you any more:

- **The host is gone.** `api.whissle.ai` returns `404` on every path this package called —
  `/v1`, `/asr/transcribe`, `/backend/api-tokens/validate`, `/redoc`, and the host root. The
  token page the old README sent you to (`browser.whissle.ai/access`) does not resolve at all.
- **The token type is not self-serve.** `wh_` is a legacy gateway *device* token. It is not
  something a customer can create. Keys you can create are `wsk_` (workspace **secret**,
  server-side) and `wpk_` (**publishable**, safe in a browser) — and it is a `wsk_` that
  `whissle-sdk` takes.

Rather than rebuild a second client against the live platform, this distribution now stands
down in favour of the maintained one. Anything you import from it raises an `ImportError`
naming the replacement, so you get told where to go instead of a confusing network failure on
your first call.

## Moving

| You had | You want |
|---|---|
| `from whissle import WhissleClient` | `from whissle_sdk import WhissleClient` — **a different class**, different arguments |
| `client.speech_to_text(...)` | `w.asr.transcribe(file, ...)` |
| `client.diarize_stt(...)` | `w.asr.transcribe(file, diarize=True, num_speakers=...)` |
| `client.llm_text_summarizer(...)` | no direct equivalent — see below. `w.asr.transcribe(file, summarize=...)` summarises a **recording**, not arbitrary text |
| `client.list_asr_models()` | `w.asr.status()` — what this deployment loaded |
| `WhissleGatewayClient.transcribe_file(...)` | `w.asr.transcribe(file, ...)` |
| `WhissleGatewayClient.transcribe_pcm(...)` | `w.asr.transcribe_pcm(samples, ...)` |
| `export WHISSLE_AUTH_TOKEN=wh_…` | `export WHISSLE_API_KEY=wsk_…` (create the key in your workspace settings) |

`whissle-sdk` also covers what this package never did: the Voice Agents platform — agents,
sessions and traces, streaming chat, browser session tokens, knowledge, tools, compliance,
analytics and usage. See its own README for the full surface.

**Three things do not carry over.** Text `machine_translation` and text `llm_text_summarizer`
took arbitrary strings and have no equivalent door on the live platform. Speech translation
(`/asr/translate`, `/asr/s2s`) exists but is deliberately still restricted to the legacy token —
those legs compose speech with a language model and have no per-second price, so a workspace key
there would be an unbilled door. If you depend on any of the three, talk to us before you
migrate.

## Name collision

`whissle_sdk` exports a class **also** called `WhissleClient`. It is not this package's
`WhissleClient` and does not take the same arguments. If an editor autocompletes you into
`whissle`, that is this tombstone — the working one is imported from `whissle_sdk`.

## Still installed?

`import whissle` keeps working and emits a `DeprecationWarning`; `whissle.__version__` and
`help(whissle)` still read. Every client name, and every module that used to hold one, raises
`ImportError` with the migration note above.

## Licence

MIT. See [LICENSE](LICENSE). Releases up to and including `0.0.1` shipped contradictory
metadata — an MIT classifier over GPL-3 licence text. MIT is and always was the intent; `0.2.0`
makes the file and the metadata agree.

## Maintainers

`whissle-sdk` must be on PyPI **before** this release is published, or the install line above
points at nothing. Then:

```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

## Contact

support@whissle.ai
