from dataclasses import dataclass

import logging
import re
from constants import CLASS_ABILITIES_OUTPUT_DIR, CLASSES_FILES_OUTPUT_DIR, LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER, PATTERN_LIST
from custom_types import raw_file
from convenience_functions import write_file

@dataclass(slots=True)
class ClassFileSet:
    class_name: str
    class_file: raw_file
    class_abilities: list[raw_file]

    # TODO: reformat ">" bits
    def reformat_title_stile(self):
        # Reformat the title style of the file body
        new_body: list[str] = []

        # Reformat the title style of the file body
        for line in self.class_file.body:
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

        self.class_file.body = new_body

    def remove_bold(self):
        # Remove bold formatting from the file body
        new_body: list[str] = []

        for line in self.class_file.body:
            new_line = re.sub(r"\*", r"", line)
            new_body.append(new_line)

        self.class_file.body = new_body

    # TODO: Do on project level
    def add_linking(self):
        # Replace all instances of patterns in the file body with links to the corresponding files
        new_body: list[str] = []

        pattern_list = [pattern for pattern in PATTERN_LIST if pattern != self.class_file.name]
        pattern = re.compile("|".join(re.escape(s) for s in pattern_list))
        for line in self.class_file.body:
            new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
            new_body.append(new_line)

        self.class_file.body = new_body

    def split_class_abilities(self):
        # Split the file body into separate files for each class ability
        self.class_abilities = []

        current_file_name: str = ""
        current_file_body: list[str] = []

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                if current_file_name:
                    self.class_abilities.append(raw_file(name=current_file_name, body=current_file_body))
                current_file_name = re.sub(r"^## Level \d+:\s*", "", line)
                current_file_body = []
            else:
                current_file_body.append(line)

        if current_file_name:
            self.class_abilities.append(raw_file(name=current_file_name, body=current_file_body))
        else:
            logging.error("No class abilities found in the file.")

        return self.class_abilities

    def print_to_files(self):
        write_file(self.class_file.name, self.class_file.body, CLASSES_FILES_OUTPUT_DIR)
        for file in self.class_abilities:
            write_file(file.name, file.body, CLASS_ABILITIES_OUTPUT_DIR)

    def do_all(self):
        self.reformat_title_stile()
        self.remove_bold()
        self.add_linking()
        self.split_class_abilities()
        self.print_to_files()