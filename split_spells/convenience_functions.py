from pathlib import Path
import shutil

from data_classes import SpellBook
from constants import OUTPUT_DIR, TABLE_OUTPUT_DIR, SPELL_FILES_OUTPUT_DIR

def write_spell_files(spell_book: SpellBook, output_directory: str):
    for spell_name, spell_obj in spell_book.spells.items():
        write_file(spell_name, spell_obj.spell_body, output_directory)

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
    (output_dir / TABLE_OUTPUT_DIR).mkdir(exist_ok=True)
    (output_dir / SPELL_FILES_OUTPUT_DIR).mkdir(exist_ok=True)
    