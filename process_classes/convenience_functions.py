import shutil
from pathlib import Path
from custom_types import TextFile
from constants import INPUT_FILE
from constants import OUTPUT_DIR

# TODO: Add file path input or change to diagnostic
def open_file() -> TextFile:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    file_body: list[str] = content.splitlines()
    file_name: str = Path(INPUT_FILE).stem

    return TextFile(name=file_name, body=file_body)

def write_text_file(file : TextFile, output_folder : Path):
    file_name: str = f"{file.name}.md"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / file_name
    with open(output_file, "w", encoding="utf-8") as output_file:
            for line in file.body:
                output_file.write(f"{line}\n")

def remove_output_dir():
    folder = Path(OUTPUT_DIR)
    if folder.exists():
        shutil.rmtree(folder)