from __future__ import annotations

from sandalwood.errors.exceptions import SandalwoodError


def format_error(error: SandalwoodError) -> str:
    return f"[SandalwoodError] {error}"
