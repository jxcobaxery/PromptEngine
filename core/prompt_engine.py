import json
import random
import hashlib
from datetime import datetime
from pathlib import Path


class PromptEngine:
    """Generate prompts from a vocabulary bank."""

    def __init__(self, vocab_path: str):
        self.vocab_path = Path(vocab_path)
        self.vocab = self._load_vocab(self.vocab_path)

    def _load_vocab(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def categories(self):
        """Return available vocabulary categories."""
        return list(self.vocab.keys())

    def generate_prompt(self, diff_level: int = 5, baseline: str = "", category: str | None = None):
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
            for cat, words in self.vocab.items():
                sample = random.sample(words, min(diff_level, len(words)))
                parts.append(random.choice(sample))
        prompt = ", ".join(parts)
        if baseline:
            prompt = f"{baseline}, {prompt}" if prompt else baseline
        return prompt

    def generate_batch(self, n: int = 100, diff_level: int = 5, baseline: str = "", category: str | None = None):
        return [self.generate_prompt(diff_level, baseline, category) for _ in range(n)]


def save_prompt_hash(prompt: str, log_path: Path = Path("logs/prompt_hashes.txt")) -> None:
    hash_val = hashlib.sha256(prompt.encode()).hexdigest()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {hash_val} | {prompt}\n")


def save_prompts(prompts, format: str = "json", out_dir: str = "outputs", tag: str = "default", model: str | None = None) -> Path:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tag}.{format}"
    filepath = out_path / filename

    if format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(prompts, f, indent=2)
    elif format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            for p in prompts:
                f.write(p + "\n")
    elif format == "csv":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("prompt\n")
            for p in prompts:
                f.write(f"\"{p}\"\n")
    elif format == "gpt":
        payload = [
            {"model": model or "gpt-4o", "messages": [{"role": "user", "content": p}]}
            for p in prompts
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    else:
        raise ValueError("Unsupported format")

    for p in prompts:
        save_prompt_hash(p)
    return filepath
