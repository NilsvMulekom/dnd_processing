from pathlib import Path

OUTPUT_DIR = "Classes"
INPUT_DIR  = "input_folder"
CLASSES_OUTPUT_ROOT        = Path(OUTPUT_DIR) / "."
CLASSES_FILES_OUTPUT_DIR   = Path(OUTPUT_DIR) / "Classes"
CLASS_ABILITIES_OUTPUT_DIR = Path(CLASSES_FILES_OUTPUT_DIR) / "Class abilities"

INPUT_FILE = Path(INPUT_DIR) / "paladin.md"