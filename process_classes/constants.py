from pathlib import Path

OUTPUT_DIR = Path("Classes")
INPUT_DIR  = Path("input_folder")
# INPUT_DIR = Path("diag_input_folder")
SUBCLASSES_DIR = Path("SubClasses")
CLASS_ABILITIES_DIR = Path("ClassAbilities")
DIAGNOSTIC_OUTPUT_DIR = Path("diag/.")
# TODO: rename
FILE_NAMES_LIST_OUTPUT_DIR = Path("links/.")
FILE_NAMES_LIST            = FILE_NAMES_LIST_OUTPUT_DIR / Path("file_names.md")

TEST_INPUT_FILE = Path(INPUT_DIR) / "Barbarian.md"

LEVEL_1_HEADER = "# "
LEVEL_2_HEADER = "## "
LEVEL_3_HEADER = "### "
LEVEL_4_HEADER = "#### "
LEVEL_5_HEADER = "##### "
BOLD_HEADER    = "***"

# Ability names that are also in other classes
ABILITY_NAMES_BLACKLIST = [
    "Bonus Proficiencies",
    "Bonus Proficiency",
    "Channel Divinity",
    "Epic Boon",
    "Evasion",
    "Extra Attack",
    "Fighting Style",
    "Psionic Power",
    "Spell Breaker",
    "Spellcasting",
    "Tools of the Trade",
    "War Magic",
    "Unarmored Defense",
    "Weapon Mastery",
]

PATTERN_LIST = [
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
