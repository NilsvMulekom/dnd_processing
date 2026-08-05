from pathlib import Path
import re

from data_classes import Spell, SpellBook, PATTERN_LIST
from convenience_functions import print_spell_book, write_spell_files, create_output_dir

# TODO: Automatic table forming
# TODO: add metadata as obsidian metadata
# TODO: Add scripts for dnd classes and potentially other things

def split_files(input_file) -> SpellBook:
    input_path  = Path(input_file)
    
    with open(input_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    spell_book: SpellBook = SpellBook()
    open_spell: Spell = Spell()
    
    for line in file_content.splitlines():
        if line.startswith("#### "):
            spell_book.add(open_spell)
            # Cut off the first 5 characters to get the spell name
            spell_name: str = line[5:]
            open_spell: Spell = Spell(name=spell_name, spell_body=[])
        open_spell.spell_body.append(line)

    # Add the last spell to the spell_book if there is one open
    spell_book.add(open_spell)

    return spell_book

def add_linking(spell_book: SpellBook) -> SpellBook:
    linked_book: SpellBook = SpellBook()

    for spell_name, spell_obj in spell_book.spells.items():
        spell_body: list[str] = []
        for line in spell_obj.spell_body:
            new_line = line
            for pattern in PATTERN_LIST:
                new_line=re.sub(pattern, f"[[{pattern}]]",new_line)
            spell_body.append(new_line)
        linked_book.spells[spell_name] = Spell(name=spell_name, spell_body=spell_body)

    return linked_book
    
def main(input_file, output_directory):
    spell_book: SpellBook = SpellBook()
    create_output_dir(output_directory)
    spell_book = split_files(input_file)
    spell_book = add_linking(spell_book)
    print_spell_book(spell_book)
    write_spell_files(spell_book, output_directory)

main("input_folder/reduced_spells.md", "spells_folder")
