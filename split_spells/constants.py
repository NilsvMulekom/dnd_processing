from pathlib import Path

OUTPUT_DIR = "Spells"
# TODO: rename
TABLE_OUTPUT_DIR = Path(OUTPUT_DIR) / "."
SPELL_FILES_OUTPUT_DIR = Path(OUTPUT_DIR) / "Spells"

# TODO: Replace when all content that references these duplicate names has been automated
DUPLICATE_NAME_EXCEPTIONS = {
    "Light",
    "Slow",
    "Test",
}

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
    "Spells Alphabetical",
    "Artificer Spells",
    "Bard Spells",
    "Cleric Spells",
    "Druid Spells",
    "Paladin Spells",
    "Ranger Spells",
    "Sorcerer Spells",
    "Warlock Spells",
    "Wizard Spells",
]

