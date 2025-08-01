from __future__ import annotations

"""Utilities for applying high level prompt templates."""

from dataclasses import dataclass
from typing import Dict


TEMPLATES: Dict[str, str] = {
    "plain": "{baseline}{sep}{content}",
    "instruction": "Instruction: {baseline}\nPrompt: {content}",
    "cot": "{baseline} Let's think step by step. {content}",
}


def available_templates() -> list[str]:
    """Return the available template keys."""
    return list(TEMPLATES.keys())


@dataclass
class TemplateRenderer:
    """Render prompts using predefined templates."""

    def render(self, content: str, baseline: str = "", template: str = "plain") -> str:
        pattern = TEMPLATES.get(template, TEMPLATES["plain"])
        sep = ", " if baseline and content else ""
        return pattern.format(baseline=baseline, content=content, sep=sep).strip()
