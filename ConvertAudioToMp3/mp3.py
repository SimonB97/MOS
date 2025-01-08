# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "click",
# ]
# ///

from pathlib import Path
import subprocess
import click

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), required=True)
def convert(input_path: str, output: str) -> None:
    src = Path(input_path)
    dst = Path(output)
    dst.mkdir(exist_ok=True)

    if src.is_file():
        files = [src]
    else:
        files = [f for f in src.rglob('*.*') if f.suffix.lower() in {'.flac', '.wav', '.m4a'}]
        
    for f in files:
        try:
            rel = f.relative_to(src) if src.is_dir() else f.name
            out = dst / rel.with_suffix('.mp3')
            out.parent.mkdir(parents=True, exist_ok=True)
            
            subprocess.run([
                'ffmpeg', '-i', str(f),
                '-codec:a', 'libmp3lame', 
                '-q:a', '2',
                '-hide_banner',
                '-loglevel', 'error',
                str(out)
            ], capture_output=True)
            print(f"Converted: {f.name}")
        except Exception as e:
            print(f"Error converting {f.name}: {e}")

if __name__ == '__main__':
    convert()