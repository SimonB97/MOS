# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "click",
#     "pydub",
# ]
# ///

from pathlib import Path
from typing import List
import click
from pydub import AudioSegment

def get_audio_files(path: Path) -> List[Path]:
    return [p for p in path.rglob('*') if p.is_file() and p.suffix.lower() in {'.flac', '.wav', '.m4a'}]

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), required=True)
def convert(input_path: str, output: str) -> None:
    input_path, output_path = Path(input_path), Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    for file in get_audio_files(input_path):
        try:
            relative = file.relative_to(input_path)
            out_file = output_path / relative.with_suffix('.mp3')
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            AudioSegment.from_file(str(file)).export(str(out_file), format='mp3')
            print(f"Converted: {file.name}")
        except Exception as e:
            print(f"Error converting {file.name}: {e}")

if __name__ == '__main__':
    convert()