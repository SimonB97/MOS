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
    dst.mkdir(parents=True, exist_ok=True)

    if src.is_file():
        files = [src]
    else:
        files = list(src.rglob('*.*'))

    for f in files:
        if f.suffix.lower() not in {'.flac', '.wav', '.m4a'}:
            continue
        try:
            rel = f.relative_to(src) if src.is_dir() else f.name
            out = dst / rel.with_suffix('.mp3')
            out.parent.mkdir(parents=True, exist_ok=True)
            
            subprocess.run([
                'ffmpeg', '-i', str(f),
                '-codec:a', 'libmp3lame',
                '-q:a', '2',
                str(out)
            ], capture_output=True, check=True)
            print(f"Converted: {f.name}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {f.name}: {e.stderr.decode()}")
        except Exception as e:
            print(f"Error with {f.name}: {e}")

if __name__ == '__main__':
    convert()