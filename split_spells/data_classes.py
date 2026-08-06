from dataclasses import dataclass, field
from typing import Literal, get_args
import re
from constants import TABLE_OUTPUT_DIR, SPELL_FILES_OUTPUT_DIR
from convenience_functions import write_file

SpellLevel = Literal["cantrip", 1, 2, 3, 4, 5, 6, 7, 8, 9]

from typing import Literal

SpellSchool = Literal[
	"Abjuration",
	"Conjuration",
	"Divination",
	"Enchantment",
	"Evocation",
	"Illusion",
	"Necromancy",
	"Transmutation",
]

SpellClass = Literal[
    "Artificer",
    "Bard",
    "Cleric",
    "Druid",
    "Paladin",
    "Ranger",
    "Sorcerer",
    "Warlock",
    "Wizard",
]
@dataclass(slots=True)
class Spell:
    name:          str              | None = None
    spell_body:    list[str] = field(default_factory=list)

    level:         SpellLevel       | None = None
    concentration: bool             | None = None
    school:        SpellSchool      | None = None
    classes:       list[SpellClass] = field(default_factory=list)

    # TODO: Add Duration, casting time, ritual casting option, components, range, material cost, damage type

    def parse_spell_body(self):
        if self.spell_body is None:
            print(f"Error: Spell {self.name} has an empty body and cannot be parsed.")
            return

        if len(self.spell_body) < 2:
            print(f"Error: Spell {self.name} has insufficient spell body lines to parse.")
            return

        # Parse values in fixed positions in the spell body
        level_and_school_line = self.spell_body[1]
        # Determine the spell level
        # TODO: Check if this should be a string
        if level_and_school_line.startswith("*Level"):
            self.level = level_and_school_line.split()[1]
        elif level_and_school_line.endswith("Cantrip*"):
            self.level = "cantrip"

        # Determine the spell school
        for school in get_args(SpellSchool):
            if school in level_and_school_line:
                self.school = school

        # Parse the rest of the body to find the other attributes
        for line in self.spell_body:
            # Determine if a spell requires concentration
            if line.startswith("- **Duration:**"):
                if "Concentration" in line:
                    self.concentration = True
                else:
                    self.concentration = False

            # Determine which classes can use the spell
            if line.startswith("**Classes:**"):
                for class_name in get_args(SpellClass):
                    if class_name in line:
                        self.classes.append(class_name)

        # TODO: Check if all attributes have been filled in

    def add_linking(self):
        if self.spell_body is None:
            print(f"Error: Spell {self.name} has an empty body and cannot be linked.")
            return

        new_body: list[str] = []
        for line in self.spell_body:
            new_line = line
            for pattern in PATTERN_LIST:
                new_line = re.sub(pattern, f"[[{pattern}]]", new_line)
            new_body.append(new_line)
        self.spell_body = new_body

    def print_attributes(self):
        print(f"Spell name: {self.name}")
        print(f"Spell level: {self.level}")
        print(f"Spell concentration: {self.concentration}")
        print(f"Spell school: {self.school}")
        print(f"Spell classes: {self.classes}")

@dataclass(slots=True)
class SpellBook:
    # TODO: Add name so spellbooks sorted in certain ways can be created. Perhaps add metadata of how it is sorted
    spells: dict[str, Spell] = field(default_factory=dict)

    def add(self, spell: Spell) -> None:
        if spell.name is not None:
            # Only add the spell if it has a name (i.e., it's not an empty spell)
            self.spells[spell.name] = spell

    def sort_by_level(self) -> None:
        self.spells = dict(sorted(self.spells.items(), key=lambda item: (item[1].level != "cantrip", item[1].level)))

    def parse_all_spells(self):
        for spell in self.spells.values():
            spell.parse_spell_body()

    def add_linking_to_all_spells(self):
        for spell in self.spells.values():
            spell.add_linking()

    def print_all_spell_attributes(self):
        for spell in self.spells.values():
            spell.print_attributes()

    def print_spell_book(self):
        for spell_name, spell_obj in self.spells.items():
            print(f"Spell name: {spell_name}")
            for index, line in enumerate(spell_obj.spell_body):
                print(f"{index}: {line}")

    def write_spell_files(self):
        for spell_name, spell_obj in self.spells.items():
            write_file(spell_name, spell_obj.spell_body, SPELL_FILES_OUTPUT_DIR)

    def print_table_alphabetical(self):
        # Print the table header
        file_body : list[str] = []
        file_body.append("| Spell Name | Level | School | Concentration | Classes |")
        file_body.append("|------------|-------|--------|---------------|---------|")

        for spell in self.spells.values():
            # Change the class formatting from a list to a comma-separated string
            spell_class_line : str = ", ".join(spell.classes)
            # Print the spell attributes in a table row
            file_body.append(f"| [[{spell.name}]] | {spell.level} | {spell.school} | {spell.concentration} | {spell_class_line} |")

        write_file("Spells", file_body, TABLE_OUTPUT_DIR)

    def print_class_table(self, class_name: str):
        # Print the table header
        file_body : list[str] = []
        file_body.append("| Level | Spell Name | School | Concentration |")
        file_body.append("| ----- | ------------ |--------|---------------|")

        for spell in self.spells.values():
            if class_name in spell.classes:
                # Print the spell attributes in a table row
                file_body.append(f"| {spell.level} | [[{spell.name}]] | {spell.school} | {spell.concentration} |")

        write_file(f"{class_name} Spells", file_body, TABLE_OUTPUT_DIR)

    def print_class_tables(self):
        for class_name in get_args(SpellClass):
            self.print_class_table(class_name)

PATTERN_LIST = [
    # TODO: add more patterns
    "Blinded",
    "Charmed",
    "Deafened",
    "Exhaustion",
    "Frightened",
    "Grappled",
    "Incapacitated",
    "Invisible",
    "Paralyzed",
    "Petrified",
    "Poisoned",
    "Prone",
    "Restrained",
    "Stunned",
    "Unconscious",
]
