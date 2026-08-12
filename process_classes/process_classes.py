import re

from constants import CLASSES_FILES_OUTPUT_DIR
from convenience_functions import open_file, write_file, create_output_dirs
from custom_types import raw_file
from constants import PATTERN_LIST

# TODO: Add core traits
# TODO: add class table

LEVEL_1_HEADER = "# "
LEVEL_2_HEADER = "## "
LEVEL_3_HEADER = "### "
LEVEL_4_HEADER = "#### "
LEVEL_5_HEADER = "##### "
BOLD_HEADER    = "***"

# TODO: reformat ">" bits
def reformat_title_stile(file : raw_file) -> raw_file:
    # Reformat the title style of the file body
    new_body: list[str] = []

    # Reformat the title style of the file body
    for line in file.body:
        if line.startswith(LEVEL_2_HEADER):
            new_line = line.replace(LEVEL_2_HEADER, LEVEL_1_HEADER)
            new_body.append(new_line)
        elif line.startswith(LEVEL_4_HEADER):
            new_line = line.replace(LEVEL_4_HEADER, LEVEL_2_HEADER)
            new_body.append(new_line)
        elif line.startswith(BOLD_HEADER):
            # TODO: Clean up?
            # TODO: Make a separate regex for titles containing level N
            new_line = re.sub(r"\*\*\*(.*?)\.\*\*\*", r"#### \1\n", line)
            new_body.append(new_line)
        elif line.startswith(LEVEL_5_HEADER):
            new_line = line.replace(LEVEL_5_HEADER, LEVEL_4_HEADER)
            new_body.append(new_line)
        else:
            new_body.append(line)

    return raw_file(name=file.name, body=new_body)

def remove_bold(file : raw_file) -> raw_file:
    # Remove bold formatting from the file body
    new_body: list[str] = []

    for line in file.body:
        new_line = re.sub(r"\*", r"", line)
        new_body.append(new_line)

    return raw_file(name=file.name, body=new_body)

def add_linking(file : raw_file) -> raw_file:
    new_body: list[str] = []

    # TODO: Do not link the title of the file, or any other titles in the body
    pattern = re.compile("|".join(re.escape(s) for s in PATTERN_LIST))
    for line in file.body:
        new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
        new_body.append(new_line)

    return raw_file(name=file.name, body=new_body)

def main():
    create_output_dirs()

    file : raw_file = open_file()
    file = reformat_title_stile(file)
    file = remove_bold(file)
    file = add_linking(file)
    write_file(file.name, file.body, CLASSES_FILES_OUTPUT_DIR)
main()