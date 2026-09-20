"""One place for the "this moved" error, shared by the submodule stubs.

The modules this package used to contain are gone, so importing one would
otherwise raise ``ModuleNotFoundError: No module named 'whissle.client'`` —
technically true and completely unhelpful. Each old module name survives as
a stub that raises the migration note instead.
"""

from __future__ import annotations


def moved(what: str) -> "ImportError":
    """Build the :class:`ImportError` to raise from a retired module."""
    from . import _GUIDANCE

    return ImportError(_GUIDANCE.format(what=what))
