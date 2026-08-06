from pathlib import Path
import re
from typing import Literal, get_args
from data_classes import Spell, SpellBook, PATTERN_LIST, SpellClass
from constants import OUTPUT_DIR, TABLE_OUTPUT_DIR, SPELL_FILES_OUTPUT_DIR
from convenience_functions import write_file, create_output_dirs, write_spell_files

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

def print_table_alphabetical(spell_book: SpellBook):
    # Print the table header
    file_body : list[str] = []
    file_body.append("| Spell Name | Level | School | Concentration | Classes |")
    file_body.append("|------------|-------|--------|---------------|---------|")

    for spell in spell_book.spells.values():
        # Change the class formatting from a list to a comma-separated string
        spell_class_line : str = ", ".join(spell.classes)
        # Print the spell attributes in a table row
        file_body.append(f"| [[{spell.name}]] | {spell.level} | {spell.school} | {spell.concentration} | {spell_class_line} |")

    write_file("Spells", file_body, TABLE_OUTPUT_DIR)

def print_class_table(spell_book: SpellBook, class_name: str):
    # Print the table header
    file_body : list[str] = []
    file_body.append("| Level | Spell Name | School | Concentration |")
    file_body.append("| ----- | ------------ |--------|---------------|")

    for spell in spell_book.spells.values():
        if class_name in spell.classes:
            # Print the spell attributes in a table row
            file_body.append(f"| {spell.level} | [[{spell.name}]] | {spell.school} | {spell.concentration} |")

    write_file(f"{class_name} Spells", file_body, TABLE_OUTPUT_DIR)

def main(input_file):
    create_output_dirs()

    spell_book: SpellBook = SpellBook()
    spell_book = split_files(input_file)

    spell_book.parse_all_spells()
    spell_book.add_linking_to_all_spells()
    # spell_book.print_spell_book()
    # spell_book.print_all_spell_attributes()

    write_spell_files(spell_book, SPELL_FILES_OUTPUT_DIR)
    print_table_alphabetical(spell_book)

    sorted_book: SpellBook = spell_book
    sorted_book.sort_by_level()
    for class_name in get_args(SpellClass):
        print_class_table(sorted_book, class_name)

main("input_folder/reduced_spells.md")
