import shutil
import re
from pathlib import Path
from dataclasses import dataclass
from constants import DIAGNOSTIC_OUTPUT_DIR

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
        Replaces any strings found in the file body that is also in pattern_list with [[string]].
        If strings in pattern_list have overlap it should take the longest one.
        If the name of this file also occurs in pattern_list, it should not be linked.
        """
        new_body: list[str] = []
        pattern_list = [pattern for pattern in pattern_list if pattern != self.name]
        pattern = re.compile("|".join(re.escape(s) for s in pattern_list))
        for line in self.body:
            new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
            new_body.append(new_line)

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

def write_text_file(file : TextFile, output_folder : Path):
    """
    Writes a TextFile to a file and creates any required folders.
    """
    file_name: str = f"{file.name}.md"
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / file_name
    with open(output_file, "w", encoding="utf-8") as output_file:
            for line in file.body:
                output_file.write(f"{line}\n")
