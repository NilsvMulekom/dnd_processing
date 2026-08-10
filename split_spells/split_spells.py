from data_classes import Spell, SpellBook
from constants import SPELLS_INDEX_FILE, SPELLS_INPUT_FILE, SPELLS_OUTPUT_ROOT
from convenience_functions import create_output_dirs, link_and_write_file

def split_files() -> SpellBook:
    with open(SPELLS_INPUT_FILE, "r", encoding="utf-8") as file:
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

def main():
    create_output_dirs()
    link_and_write_file(SPELLS_INDEX_FILE, SPELLS_OUTPUT_ROOT)

    spell_book: SpellBook = SpellBook()
    spell_book = split_files()

    spell_book.parse_link_and_add_properties()

    spell_book.write_spell_files()
    spell_book.print_table_alphabetical()

    sorted_book: SpellBook = spell_book
    sorted_book.sort_by_level()
    sorted_book.print_class_tables()

main()
