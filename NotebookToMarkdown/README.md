# Notebook to Markdown Converter

Simple script to convert Jupyter notebooks (.ipynb) to Markdown (.md) format.

## Requirements

- Python 3.12 or higher
- (optional) [uv](https://github.com/astral-sh/uv) installed for easy script execution

## Usage

Basic usage:
```bash
uv run nb2md.py input_notebook.ipynb
```

Specify output directory:
```bash
uv run nb2md.py input_notebook.ipynb -o output_folder
```

Convert all notebooks in a directory:
```bash
uv run nb2md.py input_folder -o output_folder
```

With custom number of parallel workers:
```bash
uv run nb2md.py input_folder -o output_folder -w 4
```

Show help:
```bash
uv run nb2md.py -h
```

> **Recommended:** When using `uv`, you can replace `nb2md.py` with the path to the script in this repository, so you don't need to save the file first, e.g.: 
> ```bash
> uv run https://raw.githubusercontent.com/SimonB97/my-open-scripts/main/NotebookToMarkdown/nb2md.py input_folder -o output_folder
> ```
> 
> **Alternatively**, you can download the script and **run it directly with Python/pip.**

## Features

- Converts Jupyter notebooks to Markdown
- Preserves folder structure while converting directories recursively
- Parallel processing (default: 50% of CPU cores)
- Maintains original notebook structure and formatting