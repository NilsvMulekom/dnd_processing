from dataclasses import dataclass, field
from typing import Literal, get_args

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
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
]
@dataclass(slots=True)
class Spell:
    # TODO: add the rest of the spell attributes
    # TODO: add convenience features
    name:          str              | None = None
    spell_body:    list[str] = field(default_factory=list)

    level:         SpellLevel       | None = None
    concentration: bool             | None = None
    school:        SpellSchool      | None = None
    classes:       list[SpellClass] = field(default_factory=list)

    def parse_spell_body(self):
        # Determine the spell level
        # The first line of the spell body contains the level of the spell, which is either in the format "*Level X" or "Cantrip*"
        # TODO: Check if this should be a string
        if self.spell_body[1].startswith("*Level"):
            self.level = self.spell_body[1].split()[1]
        elif self.spell_body[1].endswith("Cantrip*"):
            self.level = "cantrip"

        # Determine the spell school
        for school in get_args(SpellSchool):
            # The first line of the spell body contains the school of magic.
            if school in self.spell_body[1]:
                self.school = school


    def print_attributes(self):
        print(f"Spell name: {self.name}")
        print(f"Spell level: {self.level}")
        print(f"Spell concentration: {self.concentration}")
        print(f"Spell school: {self.school}")
        print(f"Spell classes: {self.classes}")

@dataclass(slots=True)
class SpellBook:
    spells: dict[str, Spell] = field(default_factory=dict)

    def add(self, spell: Spell) -> None:
        if spell.name is not None:
            # Only add the spell if it has a name (i.e., it's not an empty spell)
            self.spells[spell.name] = spell

    def parse_all_spells(self):
        for spell in self.spells.values():
            spell.parse_spell_body()

    def print_all_spell_attributes(self):
        for spell in self.spells.values():
            spell.print_attributes()

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
