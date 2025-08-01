import json
import random
from pathlib import Path

from .template_engine import TemplateRenderer, available_templates
from .dictionary import describe


class PromptEngine:
    """Generate prompts from a vocabulary bank."""

    def __init__(self, vocab_path: str, template_renderer: TemplateRenderer | None = None):
        self.vocab_path = Path(vocab_path)
        self.vocab = self._load_vocab(self.vocab_path)
        self.template_renderer = template_renderer or TemplateRenderer()

    def _load_vocab(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def categories(self):
        """Return available vocabulary categories."""
        return list(self.vocab.keys())

    def category_definition(self, category: str) -> str | None:
        """Return human-readable definition for a category if available."""
        return describe(category)

    def generate_prompt(
        self,
        diff_level: int = 5,
        baseline: str = "",
        category: str | None = None,
        template: str = "plain",
    ):
        """Generate a single prompt.

        Args:
            diff_level: number of terms to sample per category.
            baseline: baseline text to prepend.
            category: restrict sampling to a specific category.
        """
        parts = []
        if category and category in self.vocab:
            words = self.vocab[category]
            sample = random.sample(words, min(diff_level, len(words)))
            parts.extend(sample)
        else:
            # sample diff_level terms from each category
            for cat, words in self.vocab.items():
                sample = random.sample(words, min(diff_level, len(words)))
                parts.extend(sample)
        content = ", ".join(parts)
        return self.template_renderer.render(content, baseline=baseline, template=template)

    def generate_batch(
        self,
        n: int = 100,
        diff_level: int = 5,
        baseline: str = "",
        category: str | None = None,
        template: str = "plain",
    ):
        return [self.generate_prompt(diff_level, baseline, category, template) for _ in range(n)]


def templates() -> list[str]:
    """Expose available templates."""
    return available_templates()
