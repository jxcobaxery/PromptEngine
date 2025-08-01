import json
from datetime import datetime
from pathlib import Path


class PromptMemoryVault:
    """Simple JSON-backed store for generated prompts."""

    def __init__(self, vault_path: str = "logs/prompt_memory.json"):
        self.vault_path = Path(vault_path)
        self.vault = self._load_vault()

    def _load_vault(self):
        if self.vault_path.exists():
            with open(self.vault_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_vault(self):
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.vault_path, "w", encoding="utf-8") as f:
            json.dump(self.vault, f, indent=2)

    def add_entry(self, prompt: str, category: str = "general", tags=None):
        entry = {
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "tags": tags or []
        }
        self.vault.append(entry)
        self._save_vault()
        return entry

    def search_by_tag(self, tag: str):
        return [p for p in self.vault if tag in p.get("tags", [])]

    def filter_by_category(self, category: str):
        return [p for p in self.vault if p.get("category") == category]
