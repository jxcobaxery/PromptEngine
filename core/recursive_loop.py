import json
import random
import hashlib
from datetime import datetime
from pathlib import Path

from .prompt_engine import PromptEngine


class RecursivePromptDaemon:
    """Generate prompts and recursively remix them."""

    def __init__(self, vocab_path: str = "data/vocab_text.json", history_path: str = "logs/prompt_history.json"):
        self.engine = PromptEngine(vocab_path)
        self.history_path = Path(history_path)
        self.history = self._load_history()

    def _load_history(self):
        if self.history_path.exists():
            with open(self.history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_history(self):
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def _review_and_remix(self, prompt: str):
        parts = prompt.split(", ")
        if len(parts) > 2:
            idx = random.randint(0, len(parts) - 1)
            parts[idx] = "evolved " + parts[idx]
        return ", ".join(parts)

    def run_recursive_loop(self, iterations: int = 5, diff: int = 5, template: str = "plain"):
        batch = []
        for _ in range(iterations):
            original = self.engine.generate_prompt(diff, template=template)
            remixed = self._review_and_remix(original)
            entry = {
                "timestamp": datetime.now().isoformat(),
                "original": original,
                "remixed": remixed,
                "hash": hashlib.sha256(remixed.encode()).hexdigest(),
            }
            self.history.append(entry)
            batch.append(remixed)
        self._save_history()
        return batch
