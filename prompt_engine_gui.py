import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import random
from datetime import datetime
from pathlib import Path
import os
import hashlib

# === CORE MODULES ===
class PromptEngine:
    def __init__(self, vocab_path="data/vocab_bank.json"):
        self.vocab_path = vocab_path
        self.vocab = self.load_vocab(vocab_path)

    def load_vocab(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_prompt(self, diff_level=5):
        prompt_parts = []
        for cat, words in self.vocab.items():
            sample = random.sample(words, min(diff_level, len(words)))
            prompt_parts.append(random.choice(sample))
        return ", ".join(prompt_parts)

    def generate_batch(self, n=100, diff_level=5):
        return [self.generate_prompt(diff_level) for _ in range(n)]

# === MEMORY VAULT ===
def save_prompt_hash(prompt):
    hash_val = hashlib.sha256(prompt.encode()).hexdigest()
    with open("logs/prompt_hashes.txt", "a") as f:
        f.write(f"{datetime.now().isoformat()} | {hash_val} | {prompt}\n")

# === FILE WRITERS ===
def save_prompts(prompts, format="json", out_dir="outputs", tag="default"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tag}"
    filepath = Path(out_dir) / f"{filename}.{format}"

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
    else:
        raise ValueError("Unsupported format")

    for p in prompts:
        save_prompt_hash(p)

    return filepath

# === GUI ===
class PromptGUI:
    def __init__(self, root):
        self.engine = PromptEngine()
        self.root = root
        self.root.title("PromptCrafter-X :: Neural Forge")
        self.root.geometry("700x500")

        ttk.Label(root, text="Number of Prompts").pack(pady=5)
        self.num_entry = ttk.Entry(root)
        self.num_entry.insert(0, "100")
        self.num_entry.pack()

        ttk.Label(root, text="Differentiation Level (1-10)").pack(pady=5)
        self.diff_slider = ttk.Scale(root, from_=1, to=10, orient="horizontal")
        self.diff_slider.set(5)
        self.diff_slider.pack()

        self.output_format = tk.StringVar(value="json")
        ttk.Label(root, text="Output Format").pack(pady=5)
        ttk.OptionMenu(root, self.output_format, "json", "json", "txt", "csv").pack()

        self.tag_entry = ttk.Entry(root)
        self.tag_entry.insert(0, "default")
        ttk.Label(root, text="Output Tag (for folder naming)").pack(pady=5)
        self.tag_entry.pack()

        ttk.Button(root, text="Generate Prompts", command=self.generate).pack(pady=20)

        self.status = ttk.Label(root, text="Ready.")
        self.status.pack()

    def generate(self):
        try:
            num = int(self.num_entry.get())
            diff = int(self.diff_slider.get())
            tag = self.tag_entry.get().strip().replace(" ", "_")
            prompts = self.engine.generate_batch(num, diff)
            path = save_prompts(prompts, self.output_format.get(), tag=tag)
            self.status.config(text=f"Saved: {path}")
            messagebox.showinfo("Success", f"Saved {len(prompts)} prompts to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error.")

# === ENTRY POINT ===
def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    root = tk.Tk()
    app = PromptGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()