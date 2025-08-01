import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from core.prompt_engine import PromptEngine, templates
from core.output import save_prompts
from core.prompt_profiles import load_profiles, load_profile


class PromptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PromptCrafter-X :: Neural Forge")
        self.root.geometry("800x600")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TButton", background="black", foreground="white")
        style.configure("TRadiobutton", background="black", foreground="white")
        style.configure("TEntry", fieldbackground="black", foreground="white")
        style.configure("TMenubutton", background="black", foreground="white")
        self.root.configure(bg="black")

        self.profiles = load_profiles()
        profile_names = list(self.profiles.keys())
        self.profile_var = tk.StringVar(value=profile_names[0])
        ttk.Label(root, text="Profile").pack(pady=5)
        self.profile_menu = ttk.OptionMenu(root, self.profile_var, profile_names[0], *profile_names, command=self.on_profile_change)
        self.profile_menu.pack()

        self.engine = None
        self.current_profile = None
        self.on_profile_change(profile_names[0])

        # Mode selection
        self.mode_var = tk.StringVar(value="single")
        mode_frame = ttk.Frame(root)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Single", variable=self.mode_var, value="single", command=self.on_mode_change).pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Batch", variable=self.mode_var, value="batch", command=self.on_mode_change).pack(side=tk.LEFT)

        # Number of prompts
        ttk.Label(root, text="Number of Prompts").pack(pady=5)
        self.num_entry = ttk.Entry(root)
        self.num_entry.insert(0, "1")
        self.num_entry.configure(state="disabled")
        self.num_entry.pack()

        # Baseline text
        ttk.Label(root, text="Baseline Text").pack(pady=5)
        self.baseline_entry = ttk.Entry(root, width=60)
        self.baseline_entry.pack()

        # Category selection
        ttk.Label(root, text="Category").pack(pady=5)
        self.category_var = tk.StringVar(value="All")
        self.category_menu = ttk.OptionMenu(root, self.category_var, "All", "All")
        self.category_menu.pack()
        self.update_categories()

        # Differentiation slider
        ttk.Label(root, text="Differentiation Level (1-10)").pack(pady=5)
        self.diff_slider = ttk.Scale(root, from_=1, to=10, orient="horizontal")
        self.diff_slider.set(self.current_profile["default_diff"])
        self.diff_slider.pack()

        # Output directory
        dir_frame = ttk.Frame(root)
        dir_frame.pack(pady=5)
        ttk.Label(dir_frame, text="Output Folder").pack(side=tk.LEFT)
        self.out_dir = tk.StringVar(value="outputs")
        ttk.Entry(dir_frame, textvariable=self.out_dir, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.choose_dir).pack(side=tk.LEFT)

        # Output format and model
        self.output_format = tk.StringVar(value=self.current_profile["format"])
        ttk.Label(root, text="Output Format").pack(pady=5)
        self.output_menu = ttk.OptionMenu(
            root,
            self.output_format,
            self.current_profile["format"],
            "json",
            "txt",
            "csv",
            "gpt",
            command=self.on_format_change,
        )
        self.output_menu.pack()

        self.model_var = tk.StringVar()
        self.model_label = ttk.Label(root, text="Model")
        self.model_menu = ttk.OptionMenu(root, self.model_var, "")
        self.update_model_menu()

        # Output tag
        ttk.Label(root, text="Output Tag").pack(pady=5)
        self.tag_entry = ttk.Entry(root)
        self.tag_entry.insert(0, "gui")
        self.tag_entry.pack()

        # Template selection
        ttk.Label(root, text="Template").pack(pady=5)
        self.template_var = tk.StringVar(value="plain")
        self.template_menu = ttk.OptionMenu(root, self.template_var, "plain", *templates())
        self.template_menu.pack()

        ttk.Button(root, text="Generate", command=self.generate).pack(pady=20)
        self.status = ttk.Label(root, text="Ready.")
        self.status.pack()

    def on_profile_change(self, selection):
        self.current_profile = load_profile(selection)
        vocab_path = self.current_profile["vocab_bank"]
        self.engine = PromptEngine(vocab_path)
        self.update_categories()
        self.diff_slider.set(self.current_profile["default_diff"])
        self.output_format.set(self.current_profile["format"])
        self.update_model_menu()

    def on_format_change(self, *_):
        """Callback when output format changes."""
        self.update_model_menu()

    def update_categories(self):
        if not self.engine:
            return
        cats = ["All"] + self.engine.categories()
        menu = self.category_menu["menu"]
        menu.delete(0, "end")
        for c in cats:
            definition = self.engine.category_definition(c)
            label = f"{c} - {definition}" if definition else c
            menu.add_command(label=label, command=lambda v=c: self.category_var.set(v))
        self.category_var.set("All")

    def on_mode_change(self):
        if self.mode_var.get() == "single":
            self.num_entry.configure(state="disabled")
            self.num_entry.delete(0, tk.END)
            self.num_entry.insert(0, "1")
        else:
            self.num_entry.configure(state="normal")
            if not self.num_entry.get() or self.num_entry.get() == "1":
                self.num_entry.delete(0, tk.END)
                self.num_entry.insert(0, "10")

    def choose_dir(self):
        path = filedialog.askdirectory(initialdir=self.out_dir.get() or ".")
        if path:
            self.out_dir.set(path)
    
    def update_model_menu(self):
        models = self.current_profile.get("models", []) if self.current_profile else []
        if self.output_format.get() == "gpt" and models:
            default = self.current_profile.get("default_model", models[0])
            self.model_var.set(default)
            menu = self.model_menu["menu"]
            menu.delete(0, "end")
            for m in models:
                menu.add_command(label=m, command=lambda v=m: self.model_var.set(v))
            self.model_label.pack(pady=5)
            self.model_menu.pack()
        else:
            self.model_label.pack_forget()
            self.model_menu.pack_forget()

    def generate(self):
        try:
            num = 1 if self.mode_var.get() == "single" else int(self.num_entry.get())
            diff = int(self.diff_slider.get())
            tag = self.tag_entry.get().strip().replace(" ", "_")
            baseline = self.baseline_entry.get().strip()
            category = self.category_var.get()
            if category == "All":
                category = None
            template = self.template_var.get()
            prompts = self.engine.generate_batch(
                num, diff, baseline=baseline, category=category, template=template
            )
            fmt = self.output_format.get()
            model = self.model_var.get() or None
            path = save_prompts(
                prompts,
                format=fmt,
                out_dir=self.out_dir.get(),
                tag=tag,
                model=model,
            )
            self.status.config(text=f"Saved: {path} 😺")
            messagebox.showinfo("Success", f"Purrr! Saved {len(prompts)} prompts to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error.")


def main():
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)
    root = tk.Tk()
    app = PromptGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
