import argparse
from core.prompt_engine import PromptEngine, save_prompts, templates
from core.memory_vault import PromptMemoryVault
from core.recursive_loop import RecursivePromptDaemon
from core.prompt_profiles import load_profile


def main():
    parser = argparse.ArgumentParser(description="PromptCrafter-X Command Line")
    parser.add_argument("--profile", type=str, required=True, help="Profile name (e.g. text_generation)")
    parser.add_argument("--num", type=int, default=1, help="Number of prompts to generate")
    parser.add_argument("--diff", type=int, help="Differentiation level override")
    parser.add_argument("--category", type=str, help="Restrict generation to a vocabulary category")
    parser.add_argument("--baseline", type=str, default="", help="Baseline text to prepend")
    parser.add_argument("--recursive", action="store_true", help="Use recursive remix engine")
    parser.add_argument("--tag", type=str, default="cli_batch", help="Output tag")
    parser.add_argument("--format", type=str, choices=["json", "txt", "csv", "gpt"], help="Output format override")
    parser.add_argument("--gpt-model", type=str, help="GPT model when using gpt format")
    parser.add_argument("--template", type=str, default="plain", choices=templates(), help="Prompt template to apply")
    parser.add_argument("--out-dir", type=str, default="outputs", help="Output directory")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    vocab_path = profile["vocab_bank"]
    diff_level = args.diff if args.diff else profile["default_diff"]
    output_format = args.format if args.format else profile["format"]
    gpt_model = args.gpt_model if args.gpt_model else profile.get("gpt_model")

    if args.recursive:
        daemon = RecursivePromptDaemon(vocab_path)
        prompts = daemon.run_recursive_loop(args.num, diff=diff_level, template=args.template)
    else:
        engine = PromptEngine(vocab_path)
        prompts = engine.generate_batch(
            args.num,
            diff_level,
            baseline=args.baseline,
            category=args.category,
            template=args.template,
        )

    save_prompts(
        prompts,
        format=output_format,
        tag=args.tag,
        model=gpt_model,
        out_dir=args.out_dir,
    )
    vault = PromptMemoryVault()
    for p in prompts:
        vault.add_entry(p, category=args.profile)
    print(f"✅ Generated {len(prompts)} prompts under profile '{args.profile}'")


if __name__ == "__main__":
    main()
