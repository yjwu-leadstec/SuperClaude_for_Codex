"""Load shared SuperClaude global flag metadata."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_GLOBAL_FLAGS_PATH = (
    Path(__file__).resolve().parent.parent / "assets" / "global_flags.yaml"
)


@lru_cache(maxsize=1)
def load_global_flags() -> dict[str, Any]:
    """Return the shared global flag metadata used by renderers."""
    with open(_GLOBAL_FLAGS_PATH) as f:
        data = yaml.safe_load(f) or {}
    data.setdefault("flags", [])
    data.setdefault("priority_rules", [])
    return data
