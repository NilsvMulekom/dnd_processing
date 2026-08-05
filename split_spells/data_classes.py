from dataclasses import dataclass
from typing import Literal

SpellLevel = Literal["cantrip", 1, 2, 3, 4, 5, 6, 7, 8, 9]

from typing import Literal

SpellSchool = Literal[
	"abjuration",
	"conjuration",
	"divination",
	"enchantment",
	"evocation",
	"illusion",
	"necromancy",
	"transmutation",
]

SpellClass = Literal[
    "artificer",
    "barbarian",
    "bard",
    "cleric",
    "druid",
    "fighter",
    "monk",
    "paladin",
    "ranger",
    "rogue",
    "sorcerer",
    "warlock",
    "wizard",
]
@dataclass
class Spell:
    # TODO: add the rest of the spell attributes
    name:          str              | None = None
    spell_body:    list[str]        | None = None
    level:         SpellLevel       | None = None
    concentration: bool             | None = None
    classes:       list[SpellClass] | None = None
    school:        SpellSchool      | None = None

# TODO: add convenience features
@dataclass
class SpellBook:
    spells: dict[str, Spell]

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
