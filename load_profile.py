import json
from pathlib import Path

def load_profile(profile_name, profile_path="profiles/prompt_profiles.json"):
    profile_path = Path(profile_path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile config not found: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    profile = profiles.get(profile_name)
    if not profile:
        raise ValueError(f"Profile '{profile_name}' not found in {profile_path}")

    return profile
