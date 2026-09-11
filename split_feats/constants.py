from pathlib import Path

OUTPUT_DIR = Path("Feats")
INPUT_DIR  = Path("input_folder")
# INPUT_DIR = Path("diag_input_folder")
DIAGNOSTIC_OUTPUT_DIR = Path("diag/.")
FILE_NAMES_LIST_OUTPUT_DIR = Path("links/.")
FILE_NAMES_LIST            = FILE_NAMES_LIST_OUTPUT_DIR / Path("file_names.md")

LEVEL_1_HEADER = "# "
LEVEL_2_HEADER = "## "
LEVEL_3_HEADER = "### "
LEVEL_4_HEADER = "#### "
LEVEL_5_HEADER = "##### "
BOLD_HEADER    = "***"
HEADER_PREFIXES = (LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_3_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER,)


