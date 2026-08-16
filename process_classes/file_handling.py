import shutil
from pathlib import Path
from dataclasses import dataclass

@dataclass(slots=True)
class TextFile:
    name: str
    body: list[str]

def remove_dir(folder : Path):
    if folder.exists():
        shutil.rmtree(folder)

def open_file(input_file : Path) -> TextFile:
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    file_body: list[str] = content.splitlines()
    file_name: str = input_file.stem

    return TextFile(name=file_name, body=file_body)

def write_text_file(file : TextFile, output_folder : Path):
    file_name: str = f"{file.name}.md"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / file_name
    with open(output_file, "w", encoding="utf-8") as output_file:
            for line in file.body:
                output_file.write(f"{line}\n")
