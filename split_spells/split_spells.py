from pathlib import Path
from data_classes import Spell, SpellBook
from constants import SPELLS_OUTPUT_ROOT
from convenience_functions import add_linking_to_body, create_output_dirs, write_file

def split_files(input_file) -> SpellBook:
    input_path: Path = Path(input_file)
    
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

def add_index_file():
    # TODO: replace function with a generic "take input file, add linking and output" function
    # TODO: add clean way to set paths
    # TODO: add type hinting
    # TODO: add linking dynamically
    index_file_path = Path("input_folder") / "Spells.md"
    with open(index_file_path, "r", encoding="utf-8") as file:
        index_content = file.read()

    file_body: list[str] = []
    for line in index_content.splitlines():
        file_body.append(line)

    file_body = add_linking_to_body(file_body)

    write_file("Spells", file_body, SPELLS_OUTPUT_ROOT)

def main(input_file):
    create_output_dirs()
    add_index_file()

    spell_book: SpellBook = SpellBook()
    spell_book = split_files(input_file)

    spell_book.parse_all_spells()
    spell_book.add_linking_to_all_spells()
    spell_book.add_properties_to_all_spells()
    # spell_book.print_spell_book()
    # spell_book.print_all_spell_attributes()

    spell_book.write_spell_files()
    spell_book.print_table_alphabetical()

    sorted_book: SpellBook = spell_book
    sorted_book.sort_by_level()
    sorted_book.print_class_tables()

main("input_folder/all_spells.md")
