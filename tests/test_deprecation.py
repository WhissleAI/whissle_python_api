"""The contract of a tombstone: it must say where the client went.

This package has one job now. These tests are what proves it does it — that
every name the published 0.0.1 and the unreleased 0.1.0 exported still
*answers*, with the replacement named, rather than disappearing into a
generic import error.
"""

import importlib
import subprocess
import sys
import warnings

import pytest

import whissle

# Everything a user could plausibly have written against the old package.
RETIRED_NAMES = [
    "WhissleClient",
    "WhissleGatewayClient",
    "WhissleGatewayAsyncClient",
    "WhissleClientOptions",
    "SyncWhissleClient",
    "AsyncWhissleClient",
    "HttpError",
    "ASRModel",
    "STTResponse",
    "DiarizeSTTResponse",
    "MTResposne",
    "LLMSummarizerResponse",
]

RETIRED_MODULES = [
    "whissle.client",
    "whissle.clients",
    "whissle.gateway_client",
    "whissle.gateway_async_client",
    "whissle.models",
    "whissle.options",
]


def test_importing_the_package_still_works():
    """`import whissle` must not explode: the message is only useful if read."""
    assert whissle.__version__
    assert whissle.REPLACEMENT_DISTRIBUTION == "whissle-sdk"
    assert whissle.REPLACEMENT_IMPORT == "whissle_sdk"


def test_import_warns():
    """A fresh interpreter, because the warning fires once per process."""
    proc = subprocess.run(
        [sys.executable, "-W", "always::DeprecationWarning", "-c", "import whissle"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "DeprecationWarning" in proc.stderr
    assert "whissle-sdk" in proc.stderr


@pytest.mark.parametrize("name", RETIRED_NAMES)
def test_every_retired_name_raises_importerror_naming_the_replacement(name):
    """`from whissle import X` propagates ImportError verbatim.

    An AttributeError here would be swallowed into Python's generic
    "cannot import name" line and the reader would never see the note.
    """
    with pytest.raises(ImportError) as exc:
        getattr(whissle, name)
    message = str(exc.value)
    assert "whissle-sdk" in message
    assert "whissle_sdk" in message
    assert "pip install whissle-sdk" in message


@pytest.mark.parametrize("module", RETIRED_MODULES)
def test_every_retired_module_raises_importerror_naming_the_replacement(module):
    """A deeper import is explained too, not answered with ModuleNotFoundError."""
    sys.modules.pop(module, None)
    with pytest.raises(ImportError) as exc:
        importlib.import_module(module)
    assert not isinstance(exc.value, ModuleNotFoundError)
    assert "pip install whissle-sdk" in str(exc.value)


def test_unknown_attributes_are_explained_too():
    """Anything the old package might have had gets the note, not a bare AttributeError."""
    with pytest.raises(ImportError):
        whissle.some_helper_nobody_remembers


def test_dunders_still_fail_the_ordinary_way():
    """Introspection probes must not be answered with a migration essay."""
    with pytest.raises(AttributeError):
        whissle.__nonexistent_dunder__


def test_no_dead_hosts_are_named_anywhere():
    """The hosts this package used to call return 404. Nothing may point there."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        text = "\n".join(
            filter(None, [whissle.__doc__, whissle._GUIDANCE, whissle._SUMMARY])
        )
    for dead in ("browser.whissle.ai", "lulu.whissle.ai", "api.whissle.ai/redoc"):
        assert dead not in text, (
            f"{dead} is dead and must not be cited as a destination"
        )


def test_nobody_is_told_to_get_a_legacy_token():
    """`wh_` is a device token a customer cannot self-serve. Never instruct it."""
    text = whissle._GUIDANCE + (whissle.__doc__ or "")
    assert "wsk_" in text
    for instruction in ("get a wh_", "create a wh_", "obtain a wh_"):
        assert instruction not in text.lower()
