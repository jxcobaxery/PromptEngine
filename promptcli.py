import argparse
from core.prompt_engine import PromptEngine
from core.memory_vault import PromptMemoryVault
from core.recursive_loop import RecursivePromptDaemon
from core.prompt_profiles import load_profile  # assumed loader helper
from core.prompt_engine import save_prompts


def main():
    parser = argparse.ArgumentParser(description="PromptCrafter-X Command Line")
    parser.add_argument("--profile", type=str, help="Profile name (e.g. text_generation)", required=True)
    parser.add_argument("--num", type=int, default=100, help="Number of prompts to generate")
    parser.add_argument("--diff", type=int, help="Differentiation level override")
    parser.add_argument("--recursive", action="store_true", help="Use recursive remix engine")
    parser.add_argument("--tag", type=str, default="cli_batch", help="Output tag")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    vocab_path = profile["vocab_bank"]
    diff_level = args.diff if args.diff else profile["default_diff"]
    output_format = profile["format"]

    if args.recursive:
        daemon = RecursivePromptDaemon(vocab_path)
        prompts = daemon.run_recursive_loop(args.num, diff=diff_level)
    else:
        engine = PromptEngine(vocab_path)
        prompts = engine.generate_batch(args.num, diff_level)

    save_prompts(prompts, format=output_format, tag=args.tag)
    vault = PromptMemoryVault()
    for p in prompts:
        vault.add_entry(p, category=args.profile)
    print(f"✅ Generated {len(prompts)} prompts under profile '{args.profile}'")

if __name__ == "__main__":
    main()
