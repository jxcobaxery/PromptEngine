import json
import hashlib
from datetime import datetime
from pathlib import Path


def save_prompt_hash(prompt: str, log_path: Path = Path("logs/prompt_hashes.txt")) -> None:
    """Persist a hash of the prompt for traceability."""
    hash_val = hashlib.sha256(prompt.encode()).hexdigest()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {hash_val} | {prompt}\n")


def save_prompts(
    prompts,
    format: str = "json",
    out_dir: str = "outputs",
    tag: str = "default",
    model: str | None = None,
) -> Path:
    """Save prompts in various formats with optional model metadata."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tag}.{format}"
    filepath = out_path / filename

    if format == "json":
        payload = {"prompts": prompts}
        if model:
            payload["model"] = model
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    elif format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            if model:
                f.write(f"# model: {model}\n")
            for p in prompts:
                f.write(p + "\n")
    elif format == "csv":
        with open(filepath, "w", encoding="utf-8") as f:
            if model:
                f.write("model,prompt\n")
                for p in prompts:
                    f.write(f"{model},\"{p}\"\n")
            else:
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
