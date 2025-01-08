# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "click",
# ]
# ///

from pathlib import Path
import subprocess
import click
import sys
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from typing import List, Tuple

def get_default_workers() -> int:
    cpu_count = multiprocessing.cpu_count()
    return max(1, cpu_count // 2)  # Use 50% of CPUs by default

def check_ffmpeg() -> bool:
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def convert_file(file_data: Tuple[Path, Path]) -> Tuple[str, bool, str]:
    input_file, output_file = file_data
    try:
        result = subprocess.run([
            'ffmpeg', '-i', str(input_file),
            '-codec:a', 'libmp3lame', 
            '-q:a', '2',
            '-hide_banner',
            '-loglevel', 'error',
            str(output_file)
        ], capture_output=True)
        
        if result.returncode == 0:
            return (input_file.name, True, "")
        return (input_file.name, False, result.stderr.decode())
    except Exception as e:
        return (input_file.name, False, str(e))

@click.command(help="Convert audio files to MP3 format using ffmpeg")
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), required=True, help="Output directory")
@click.option('--workers', '-w', type=int, default=None, 
            help="Number of parallel workers (default: 50% of CPU cores)")
def convert(input_path: str, output: str, workers: int) -> None:
    if not check_ffmpeg():
        print("Error: ffmpeg not found. Please install ffmpeg first.")
        print("Windows: winget install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Linux: sudo apt install ffmpeg")
        sys.exit(1)

    max_workers = workers or get_default_workers()
    
    src = Path(input_path)
    dst = Path(output)
    dst.mkdir(exist_ok=True)

    if src.is_file():
        files = [src]
    else:
        files = [f for f in src.rglob('*.*') if f.suffix.lower() in {'.flac', '.wav', '.m4a'}]
        
    if not files:
        print(f"No audio files found in {input_path}")
        sys.exit(1)

    conversion_tasks: List[Tuple[Path, Path]] = []
    for f in files:
        rel = f.relative_to(src) if src.is_dir() else f.name
        out = dst / rel.with_suffix('.mp3')
        out.parent.mkdir(parents=True, exist_ok=True)
        conversion_tasks.append((f, out))

    converted = 0
    errors = 0
    
    print(f"Converting {len(files)} files using {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filename, success, error in executor.map(convert_file, conversion_tasks):
            if success:
                print(f"Converted: {filename}")
                converted += 1
            else:
                print(f"Error converting {filename}: {error}")
                errors += 1

    print(f"\nDone! Converted: {converted}, Errors: {errors}")

if __name__ == '__main__':
    convert()