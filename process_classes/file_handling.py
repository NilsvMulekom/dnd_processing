import shutil
import re
import logging
from pathlib import Path
from dataclasses import dataclass
from constants import DIAGNOSTIC_OUTPUT_DIR, FILE_NAMES_LIST, ABILITY_NAMES_BLACKLIST, HEADER_PREFIXES

@dataclass(slots=True)
class TextFile:
    """
    Class to contain the contents of a text file, includes some methods commonly needed for text files.
    """
    name: str
    body: list[str]

    diagnostic_print_output_dir = DIAGNOSTIC_OUTPUT_DIR

    def diagnostic_print_to_file(self):
        """
        Write the TextFil to a file in a diagnostic folder.
        """
        write_text_file(self, self.diagnostic_print_output_dir)

    def add_linking(self, pattern_list : list[str]):
        """
        Replaces any strings found in self.body that match a string in pattern_list with [[string]]
        If multiple strings in pattern_list match a string found in self.body, it takes the longest match.
        If self.name also occurs in pattern_list, it is not replaced.
        Only whole words will be replaced.
        Text in headings (a line starting with any amount of #) will not be replaced
        """
        link_patterns = sorted(
            (pattern for pattern in pattern_list if pattern != self.name),
            key=len,
            reverse=True,
        )

        if not link_patterns:
            return

        pattern = re.compile(r"(?<!\w)(" + "|".join(re.escape(s) for s in link_patterns) + r")(?!\w)")

        new_body: list[str] = []
        for line in self.body:
            linked_lines = []
            for line in line.splitlines(keepends=True):
                if line.startswith(HEADER_PREFIXES):
                    linked_lines.append(line)
                else:
                    linked_lines.append(pattern.sub(lambda match: f"[[{match.group(0)}]]", line))

            new_body.append("".join(linked_lines))

        self.body = new_body

def remove_dir(folder : Path):
    """
    Remove the folder in the supplied path if it exists.
    """
    if folder.exists():
        shutil.rmtree(folder)

def open_file(input_file : Path) -> TextFile:
    """
    Opens the file in the supplies path and returns it as a TextFile.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    file_body: list[str] = content.splitlines()
    file_name: str = input_file.stem

    return TextFile(name=file_name, body=file_body)

def log_file_name(file_name : str):
    """
    Add the name of this file to a list of filenames.
    This list can be used for linking.
    This function reports an error if a filename already exists to avoid duplicates.
    """
    # Create missing directories
    FILE_NAMES_LIST.parent.mkdir(parents=True, exist_ok=True)
    # Create file if it doesn't exist
    FILE_NAMES_LIST.touch(exist_ok=True)

    with FILE_NAMES_LIST.open("r", encoding="utf-8") as file:
        for line in file:
            if line.rstrip("\n") == file_name:
                logging.error(f"TextFile.__log_file_name: filename {file_name} already present in list")

    with open(FILE_NAMES_LIST, "a", encoding="utf-8") as file:
        file.write(file_name + "\n")

def write_text_file(file : TextFile, output_folder : Path):
    """
    Writes a TextFile to a file and creates any required folders.
    """
    file_name: str = f"{file.name}.md"

    if file.name not in ABILITY_NAMES_BLACKLIST:
        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / file_name
        with open(output_file, "w", encoding="utf-8") as output_file:
                for line in file.body:
                    output_file.write(f"{line}\n")

        log_file_name(file_name)
