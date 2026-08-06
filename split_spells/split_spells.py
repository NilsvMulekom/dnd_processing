from pathlib import Path
import re

from data_classes import Spell, SpellBook, PATTERN_LIST
from convenience_functions import print_spell_book, write_spell_files, create_output_dir, write_file

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

    write_file("spell_table", file_body, "table_folder")

def print_class_table(spell_book: SpellBook, class_name: str):
    for spell in spell_book.spells.values():
        if class_name not in spell.classes:
            print(f"Error: Spell {spell.name} does not have class {class_name} in its classes list.")

    # Print the table header
    file_body : list[str] = []
    file_body.append("| Level | Spell Name | School | Concentration |")
    file_body.append("| ----- | ------------ |--------|---------------|")

    for spell in spell_book.spells.values():
        if class_name in spell.classes:
            # Print the spell attributes in a table row
            file_body.append(f"| {spell.level} | [[{spell.name}]] | {spell.school} | {spell.concentration} |")

    write_file(f"{class_name} Spells", file_body, "table_folder")

def main(input_file, output_directory):
    spell_book: SpellBook = SpellBook()
    create_output_dir(output_directory)
    create_output_dir("table_folder")
    spell_book = split_files(input_file)

    spell_book.parse_all_spells()
    spell_book.add_linking_to_all_spells()
    spell_book.print_all_spell_attributes()

    # print_spell_book(spell_book)
    write_spell_files(spell_book, output_directory)
    print_table_alphabetical(spell_book)
    print_class_table(spell_book, "Paladin")

main("input_folder/reduced_spells.md", "spells_folder")
