"""Utility helpers for vocabulary category definitions."""

import json
from pathlib import Path
from typing import Dict

_DEF_PATH = Path('data/vocab_defs.json')


def load_definitions(path: Path = _DEF_PATH) -> Dict[str, str]:
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


_DEFINITIONS = load_definitions()


def describe(category: str) -> str | None:
    """Return a human readable description for a vocabulary category."""
    return _DEFINITIONS.get(category)


def definitions() -> Dict[str, str]:
    """Return a copy of all loaded definitions."""
    return dict(_DEFINITIONS)


def add_definition(category: str, text: str) -> None:
    """Add or update a category definition and persist it."""
    _DEFINITIONS[category] = text
    with open(_DEF_PATH, 'w', encoding='utf-8') as f:
        json.dump(_DEFINITIONS, f, indent=2)
