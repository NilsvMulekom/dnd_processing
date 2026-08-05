from dataclasses import dataclass, field
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

@dataclass(slots=True)
class SpellBook:
    spells: dict[str, Spell] = field(default_factory=dict)

    def add(self, spell: Spell) -> None:
        if spell.name is not None:
            # Only add the spell if it has a name (i.e., it's not an empty spell)
            self.spells[spell.name] = spell

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
