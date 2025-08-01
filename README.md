# PromptCrafter-X

PromptCrafter-X is a modular prompt generation toolkit featuring a black and white GUI and a flexible command line interface. It uses vocabulary banks and templates to craft prompts for text, image, code, video, and agent-oriented tasks.

## Features
- Vocabulary profiles with category definitions and default formatting
- Baseline text and category selection for focused prompt generation
- Template engine supporting plain, instruction, and chain-of-thought styles
- GPT export that emits chat-style payloads with model metadata
- Hash logging and memory vault for traceability
- Modern black-and-white GUI with single or batch modes and export options

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Command Line Usage
Generate two prompts from the text generation profile:
```bash
python promptcli.py --profile text_generation --num 2 --baseline "heroic tale" --category genre --tag demo
```
Export prompts in GPT format for a specific model:
```bash
python promptcli.py --profile text_generation --num 1 --baseline "quick fox" --category tone --format gpt --gpt-model gpt-4o --tag gptdemo
```

## GUI Usage
Start the GUI (requires a system with a display environment):
```bash
python prompt_engine_gui.py
```
Use the interface to choose profiles, categories, templates, output format, and destination folder. Select single or batch mode to generate prompts and save them to disk.

## Data
Vocabulary files live in the `data/` directory and can be extended with additional categories. Prompt profiles are configured in `prompt_profiles.json`.

## License
MIT
