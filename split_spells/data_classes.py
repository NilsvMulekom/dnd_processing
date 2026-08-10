from dataclasses import dataclass, field
from typing import get_args

from constants import SPELLS_OUTPUT_ROOT, SPELL_FILES_OUTPUT_DIR, DUPLICATE_NAME_EXCEPTIONS
from convenience_functions import add_linking_to_body, write_file
from custom_types import TextBody, SpellLevel, SpellSchool, SpellClass, SpellComponent, DamageType

@dataclass(slots=True)
class Spell:
    name       : str | None = None
    properties : TextBody = field(default_factory=list)
    spell_body : TextBody = field(default_factory=list)

    level:         SpellLevel       | None = None
    concentration: bool             | None = None
    ritual:        bool             | None = None
    school:        SpellSchool      | None = None
    classes:       list[SpellClass] = field(default_factory=list)

    casting_time  : str | None = None
    duration      : str | None = None
    spell_range   : str | None = None
    damage_type   : list[DamageType] = field(default_factory=list)
    material_cost : str | None = None
    components    : list[SpellComponent] = field(default_factory=list)

    def parse_spell_body(self):
        if self.spell_body is None:
            print(f"Error: Spell {self.name} has an empty body and cannot be parsed.")
            return

        if len(self.spell_body) < 2:
            print(f"Error: Spell {self.name} has insufficient spell body lines to parse.")
            return

        ###########################################################
        # Parse values in fixed positions in the spell body       #
        ###########################################################
        level_and_school_line = self.spell_body[1]
        # Determine the spell level
        if level_and_school_line.startswith("*Level"):
            self.level = f"Level {level_and_school_line.split()[1]}"
        elif level_and_school_line.endswith("Cantrip*"):
            self.level = "Cantrip"

        # Determine the spell school
        for school in get_args(SpellSchool):
            if school in level_and_school_line:
                self.school = school

        ###########################################################
        # Parse the rest of the body to find the other attributes #
        ###########################################################
        for line in self.spell_body:
            
            if line.startswith("- **Casting Time:**"):
                # Determine if the spell can be ritual cast
                if "Ritual" in line:
                    self.ritual = True
                else:
                    self.ritual = False
                # Determine the spell's casting time
                if "Action" in line:
                    self.casting_time = "Action"
                elif "Bonus Action" in line:
                    self.casting_time = "Bonus Action"
                elif "Reaction" in line:
                    self.casting_time = "Reaction"
                else:
                    self.casting_time = f"{line.split()[3]} {line.split()[4]}"
            if line.startswith("- **Range:**"):
                # Determine the spell's range
                if len(line.split()) == 3:
                    self.spell_range = line.split()[2]
                else:
                    self.spell_range = f"{line.split()[2]} {line.split()[3]}"
            if line.startswith("- **Components:**"):
                # Determine the spell's components
                for component in get_args(SpellComponent):
                    if component in line:
                        self.components.append(component)
                # Determine the spell's material cost if it has one
                if "GP".casefold() in line.casefold():
                    words = line.split()
                    for i, word in enumerate(words):
                        if "GP".casefold() in word.casefold():
                            if self.material_cost is not None:
                                # If the spell already has a material cost, set it to "Special" since it has multiple costs
                                self.material_cost = "Special"
                            elif "(" in words[i-1]:
                                # Strip away the leading "(" from the material cost if it is present
                                self.material_cost = f"{words[i-1].lstrip('(')} GP"
                            else:
                                self.material_cost = f"{words[i-1]} GP"
            if line.startswith("- **Duration:**"):
                # Determine if the spell requires concentration and the duration of the spell
                if "Concentration" in line:
                    self.concentration = True
                    # Line is structured in such a way that the lines selected are: up to <duration> <time unit>
                    self.duration = f"{line.split()[3]} {line.split()[4]} {line.split()[5]} {line.split()[6]}"
                else:
                    self.concentration = False
                    if "Instantaneous" in line:
                        self.duration = "Instantaneous"
                    elif "Special" in line:
                        self.duration = "Special"
                    elif "Until dispelled" in line:
                        self.duration = "Until dispelled"
                    else:
                        # Line is structured in such a way that the lines selected are: <duration> <time unit>
                        self.duration = f"{line.split()[2]} {line.split()[3]}"
            # Determine which classes can use the spell
            if line.startswith("**Classes:**"):
                for class_name in get_args(SpellClass):
                    if class_name in line:
                        self.classes.append(class_name)
            # Determine the spell's damage types
            for damage_type in get_args(DamageType):
                new_damage_type : str = ""
                if f"{damage_type},".casefold() in line.casefold():
                    new_damage_type = damage_type
                if f"{damage_type}.".casefold() in line.casefold():
                    new_damage_type = damage_type
                if f"{damage_type} damage".casefold() in line.casefold():
                    new_damage_type = damage_type
                if new_damage_type != "" and new_damage_type not in self.damage_type:
                    self.damage_type.append(new_damage_type)

        # Check if all attributes that should have values have been filled in
        if self.level is None:
            print(f"Warning: Spell {self.name} has no level parsed.")
        if self.school is None:
            print(f"Warning: Spell {self.name} has no school parsed.")
        if self.casting_time is None:
            print(f"Warning: Spell {self.name} has no casting time parsed.")
        if self.spell_range is None:
            print(f"Warning: Spell {self.name} has no range parsed.")
        if self.duration is None:
            print(f"Warning: Spell {self.name} has no duration parsed.")
        if self.concentration is None:
            print(f"Warning: Spell {self.name} has no concentration parsed.")
        if self.ritual is None:
            print(f"Warning: Spell {self.name} has no ritual parsed.")
        if len(self.components) == 0:
            print(f"Warning: Spell {self.name} has no components parsed.")

    def add_linking(self):
        self.spell_body = add_linking_to_body(self.spell_body)

    def add_properties(self):
        if self.spell_body is None:
            print(f"Error: Spell {self.name} has an empty body and cannot have properties added.")
            return

        properties_body: TextBody = []
        properties_body.append(f"---")
        properties_body.append(f"aliases: {self.name}")
        properties_body.append(f"level: {self.level}")
        properties_body.append(f"school: {self.school}")
        properties_body.append(f"concentration: {self.concentration}")
        properties_body.append(f"ritual: {self.ritual}")
        properties_body.append(f"casting_time: {self.casting_time}")
        properties_body.append(f"duration: {self.duration}")
        properties_body.append(f"range: {self.spell_range}")
        properties_body.append(f"material_cost: {self.material_cost}")

        properties_body.append(f"components:")
        for component in self.components:
            properties_body.append(f"  - {component}")
        properties_body.append(f"damage_types:")
        for damage_type in self.damage_type:
            properties_body.append(f"  - {damage_type}")
        properties_body.append(f"classes:")
        for class_name in self.classes:
            properties_body.append(f"  - {class_name}")
        properties_body.append(f"---")

        self.properties = properties_body

    def print_attributes(self):
        print(f"Spell name: {self.name}")
        print(f"Spell level: {self.level}")
        print(f"Spell concentration: {self.concentration}")
        print(f"Spell ritual: {self.ritual}")
        print(f"Spell school: {self.school}")
        print(f"Spell classes: {self.classes}")

        print(f"Spell casting time: {self.casting_time}")
        print(f"Spell duration: {self.duration}")
        print(f"Spell range: {self.spell_range}")
        print(f"Spell damage type: {self.damage_type}")
        print(f"Spell material cost: {self.material_cost}")
        print(f"Spell components: {self.components}")

@dataclass(slots=True)
class SpellBook:
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

    def add_properties_to_all_spells(self):
        for spell in self.spells.values():
            spell.add_properties()

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
            file_body : TextBody = []
            file_body.extend(spell_obj.properties)
            file_body.extend(spell_obj.spell_body)
            if spell_name in DUPLICATE_NAME_EXCEPTIONS:
                new_name = f"{spell_name} (Spell)"
                write_file(new_name, file_body, SPELL_FILES_OUTPUT_DIR)
            else:
                write_file(spell_name, file_body, SPELL_FILES_OUTPUT_DIR)

    def print_table_alphabetical(self):
        # Print the table header
        file_body : TextBody = []
        file_body.append("| Spell Name | Level | School | Concentration | Ritual | Components | Material Cost | Classes | Damage Type | Casting time | Duration | Range |")
        file_body.append("|------------|-------|--------|---------------|--------|------------|---------------|---------|-------------|--------------|----------|-------|")

        for spell in self.spells.values():
            # Change the class formatting from a list to a comma-separated string
            spell_class_line : str = ", ".join(spell.classes)
            spell_component_line : str = ", ".join(spell.components)
            damage_type_line : str = ", ".join(spell.damage_type)
            # Print the spell attributes in a table row
            if spell.name in DUPLICATE_NAME_EXCEPTIONS:
                file_body.append(f"| [[{spell.name} (Spell)\\|{spell.name}]] | {spell.level} | {spell.school} | {spell.concentration} | {spell.ritual} | {spell_component_line} | {spell.material_cost} | {spell_class_line} | {damage_type_line} | {spell.casting_time} | {spell.duration} | {spell.spell_range} |")
            else:
                file_body.append(f"| [[{spell.name}]] | {spell.level} | {spell.school} | {spell.concentration} | {spell.ritual} | {spell_component_line} | {spell.material_cost} | {spell_class_line} | {damage_type_line} | {spell.casting_time} | {spell.duration} | {spell.spell_range} |")

        write_file("Spells Alphabetical", file_body, SPELLS_OUTPUT_ROOT)

    def print_class_table(self, class_name: str):
        # Print the table header
        file_body : TextBody = []
        file_body.append("| Level | Spell Name | School | Concentration | Ritual | Components | Material Cost | Damage Type | Casting time | Duration | Range |")
        file_body.append("| ----- | ---------- |--------|---------------|--------|------------|---------------|-------------|--------------|----------|-------|")

        for spell in self.spells.values():
            spell_component_line : str = ", ".join(spell.components)
            damage_type_line : str = ", ".join(spell.damage_type)
            if class_name in spell.classes:
                # Print the spell attributes in a table row
                if spell.name in DUPLICATE_NAME_EXCEPTIONS:
                    file_body.append(f"| {spell.level} | [[{spell.name} (Spell)\\|{spell.name}]] | {spell.school} | {spell.concentration} | {spell.ritual} | {spell_component_line} | {spell.material_cost} | {damage_type_line} | {spell.casting_time} | {spell.duration} | {spell.spell_range} |")
                else:
                    file_body.append(f"| {spell.level} | [[{spell.name}]] | {spell.school} | {spell.concentration} | {spell.ritual} | {spell_component_line} | {spell.material_cost} | {damage_type_line} | {spell.casting_time} | {spell.duration} | {spell.spell_range} |")

        write_file(f"{class_name} Spells", file_body, SPELLS_OUTPUT_ROOT)

    def print_class_tables(self):
        for class_name in get_args(SpellClass):
            self.print_class_table(class_name)