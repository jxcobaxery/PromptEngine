"""Simple dictionary utilities for vocabulary categories."""

import json
from pathlib import Path
from typing import Dict


_DEF_PATH = Path("data/vocab_defs.json")


def load_definitions(path: Path = _DEF_PATH) -> Dict[str, str]:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


_DEFINITIONS = load_definitions()


def describe(category: str) -> str | None:
    """Return a human readable description for a vocabulary category."""
    return _DEFINITIONS.get(category)
