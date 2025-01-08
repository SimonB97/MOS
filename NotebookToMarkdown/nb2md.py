# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "nbconvert",
# ]
# ///

from pathlib import Path
import click
import sys
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from typing import List, Tuple
from nbconvert import MarkdownExporter
import nbformat

def get_default_workers() -> int:
    cpu_count = multiprocessing.cpu_count()
    return max(1, cpu_count // 2)

def convert_notebook(file_data: Tuple[Path, Path]) -> Tuple[str, bool, str]:
    input_file, output_file = file_data
    try:
        with open(input_file) as f:
            nb = nbformat.read(f, as_version=4)
        
        exporter = MarkdownExporter()
        markdown, _ = exporter.from_notebook_node(nb)
        
        output_file.write_text(markdown)
        return (input_file.name, True, "")
    except Exception as e:
        return (input_file.name, False, str(e))

@click.command(help="Convert Jupyter notebooks to Markdown format")
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output directory (default: current directory)")
@click.option('--workers', '-w', type=int, default=None, 
            help="Number of parallel workers (default: 50% of CPU cores)")
def convert(input_path: str, output: str | None, workers: int) -> None:
    max_workers = workers or get_default_workers()
    
    src = Path(input_path)
    dst = Path(output) if output else Path.cwd()
    
    if not src.is_file() and output:
        dst.mkdir(exist_ok=True)

    if src.is_file():
        files = [src]
    else:
        files = [f for f in src.rglob('*.ipynb')]
        
    if not files:
        print(f"No notebook files found in {input_path}")
        sys.exit(1)

    conversion_tasks: List[Tuple[Path, Path]] = []
    for f in files:
        if output or src.is_dir():
            rel = f.relative_to(src) if src.is_dir() else f.name
            out = dst / rel.with_suffix('.md')
        else:
            out = dst / f.with_suffix('.md').name
            
        out.parent.mkdir(parents=True, exist_ok=True)
        conversion_tasks.append((f, out))

    converted = 0
    errors = 0
    
    print(f"Converting {len(files)} notebooks using {max_workers} workers...")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for filename, success, error in executor.map(convert_notebook, conversion_tasks):
            if success:
                print(f"Converted: {filename}")
                converted += 1
            else:
                print(f"Error converting {filename}: {error}")
                errors += 1

    print(f"\nDone! Converted: {converted}, Errors: {errors}")

if __name__ == '__main__':
    convert()