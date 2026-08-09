from pathlib import Path
import re
import shutil

from constants import OUTPUT_DIR, TABLE_OUTPUT_DIR, SPELL_FILES_OUTPUT_DIR, PATTERN_LIST
from custom_types import TextBody

def write_file(file_title: str, file_body: list[str], output_path: str):
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
    TABLE_OUTPUT_DIR.mkdir(exist_ok=True)
    SPELL_FILES_OUTPUT_DIR.mkdir(exist_ok=True)

def add_linking_to_body(text_body: TextBody) -> TextBody:
    if not text_body:
        print("Error: Spell body is empty and cannot be linked.")

    new_body: TextBody = []
    for line in text_body:
        new_line = line
        for pattern in PATTERN_LIST:
            new_line = re.sub(pattern, f"[[{pattern}]]", new_line)
        new_body.append(new_line)
    return new_body

    