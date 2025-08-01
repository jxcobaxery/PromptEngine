import json
from pathlib import Path


def load_profiles(profile_path: str = "prompt_profiles.json"):
    path = Path(profile_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_profile(profile_name: str, profile_path: str = "prompt_profiles.json"):
    profiles = load_profiles(profile_path)
    profile = profiles.get(profile_name)
    if not profile:
        raise ValueError(f"Profile '{profile_name}' not found in {profile_path}")
    return profile
