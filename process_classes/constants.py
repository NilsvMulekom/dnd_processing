from pathlib import Path

OUTPUT_DIR = "Classes"
INPUT_DIR  = "input_folder"
CLASSES_OUTPUT_ROOT        = Path(OUTPUT_DIR) / "."
CLASSES_FILES_OUTPUT_DIR   = Path(OUTPUT_DIR) / "Classes"
CLASS_ABILITIES_OUTPUT_DIR = Path(CLASSES_FILES_OUTPUT_DIR) / "Class abilities"

INPUT_FILE = Path(INPUT_DIR) / "Paladin.md"

PATTERN_LIST = [
    # TODO: add more patterns
    # TODO: make centralized list
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
