# [My](https://github.com/SimonB97) Open Scripts

This is a collection of (mainly Python-) scripts that I have written (or modified) for a number of different tasks. I have made them available here in the hope that they may be useful to others.

These scripts are designed to be run from the command line with minimal friction and in multiple environments.

This is why the Python-scripts include a special frontmatter which allows the **awesome** [uv](https://docs.astral.sh/uv/) Python package manager to run them 'instantly', that is, without the need to install any dependencies manually first because `uv` will take care of that (by installing them **very fast** in a temporary environment). (Inspired by Simon Willison's [blog post](https://simonwillison.net/2024/Dec/19/one-shot-python-tools/))


## How To Use

### Python scripts

1. Install `uv` by following their [Instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
2. Run the script:
```bash
# a) running a script directly (from this repository, without downloading it first)
uv run https://raw.githubusercontent.com/SimonB97/MOS/main/<path-to-script> <args>

# b) running a script after downloading it
uv run <path-to-script> <args>

# c) or using pip
pip install <dependencies-in-frontmatter>
python <path-to-script> <args>
```

Replace `<path-to-script>` with the path to the script you want to run, and `<args>` with the arguments you want to pass to the script.


**Example:**

Running the [Audio Converter Script](https://github.com/SimonB97/my-open-scripts/tree/main/ConvertAudioToMp3) 
```bash
uv run https://raw.githubusercontent.com/SimonB97/my-open-scripts/main/ConvertAudioToMp3/mp3.py input_folder -o output_folder
```
