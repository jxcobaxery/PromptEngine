import json
import random
import hashlib
from datetime import datetime
from pathlib import Path

from core.prompt_engine import PromptEngine

class RecursivePromptDaemon:
    def __init__(self, vocab_path="data/vocab_bank.json", history_path="logs/prompt_history.json"):
        self.engine = PromptEngine(vocab_path)
        self.history_path = Path(history_path)
        self.prompt_history = self.load_history()

    def load_history(self):
        if self.history_path.exists():
            with open(self.history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.prompt_history, f, indent=2)

    def review_and_remix(self, prompt):
        # Simple recursive evolution: reverse a segment, add a synonym, etc.
        parts = prompt.split(", ")
        if len(parts) > 2:
            parts[random.randint(0, len(parts)-1)] = "evolved " + parts[random.randint(0, len(parts)-1)]
        return ", ".join(parts)

    def run_recursive_loop(self, iterations=5, diff=5):
        new_batch = []
        for _ in range(iterations):
            original = self.engine.generate_prompt(diff)
            remixed = self.review_and_remix(original)
            timestamp = datetime.now().isoformat()
            hashval = hashlib.sha256(remixed.encode()).hexdigest()
            entry = {
                "timestamp": timestamp,
                "original": original,
                "remixed": remixed,
                "hash": hashval
            }
            self.prompt_history.append(entry)
            new_batch.append(remixed)

        self.save_history()
        return new_batch

if __name__ == "__main__":
    daemon = RecursivePromptDaemon()
    evolved = daemon.run_recursive_loop()
    print("Evolved Prompts:")
    for p in evolved:
        print(" -", p)
