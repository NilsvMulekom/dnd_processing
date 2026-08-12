import shutil
from pathlib import Path
from custom_types import raw_file
from constants import INPUT_FILE
from constants import OUTPUT_DIR, CLASSES_OUTPUT_ROOT, CLASSES_FILES_OUTPUT_DIR, CLASS_ABILITIES_OUTPUT_DIR

def open_file() -> raw_file:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    file_body: list[str] = content.splitlines()
    file_name: str = INPUT_FILE.stem

    return raw_file(name=file_name, body=file_body)

def write_file(file_title: str, file_body: list[str], output_path: Path):
    file_name: str = f"{file_title}.md"
    output_file = Path(output_path) / file_name

    with open(output_file, "w", encoding="utf-8") as file:
        for line in file_body:
            file.write(f"{line}\n")

def create_output_dirs():
    output_dir = Path(OUTPUT_DIR)
    # Create output dir, if it already exists delete the old version first
    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(exist_ok=True)
    CLASSES_OUTPUT_ROOT.mkdir(exist_ok=True)
    CLASSES_FILES_OUTPUT_DIR.mkdir(exist_ok=True)
    CLASS_ABILITIES_OUTPUT_DIR.mkdir(exist_ok=True)