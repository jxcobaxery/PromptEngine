import tkinter as tk
from tkinter import scrolledtext
from core.prompt_engine import PromptEngine

class PromptPreview:
    def __init__(self, master, vocab_path):
        self.frame = tk.Frame(master)
        self.engine = PromptEngine(vocab_path)

        self.label = tk.Label(self.frame, text="Prompt Preview")
        self.label.pack()

        self.textbox = scrolledtext.ScrolledText(self.frame, height=10, width=80, wrap=tk.WORD)
        self.textbox.pack(pady=10)

        self.generate_button = tk.Button(self.frame, text="Preview Prompt", command=self.preview)
        self.generate_button.pack()

    def preview(self):
        prompt = self.engine.generate_prompt(diff_level=5)
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, prompt)

    def get_frame(self):
        return self.frame
