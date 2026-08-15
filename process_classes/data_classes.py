from dataclasses import dataclass, field

import logging
logging.basicConfig(level=logging.INFO)

import re
from constants import CLASS_ABILITIES_OUTPUT_DIR, CLASSES_FILES_OUTPUT_DIR, LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER, PATTERN_LIST
from custom_types import raw_file
from convenience_functions import write_file

@dataclass(slots=True)
class ClassFileSet:
    class_name: str
    class_file: raw_file
    class_abilities     : list[raw_file]

    # TODO: make private?
    unique_ability_names: list[str] = field(default_factory=list)

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

    # TODO: Let copilot check for improvements
    def construct_class_abilities_list(self) -> list[str]:
        """
            Run over all headings in the file that contain level and return only the unique ability names.
        """
        
        duplicated_ability_names: list[str] = []

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                ability_name : str = re.sub(r"^## Level \d+:\s*", "", line)
                if (ability_name in self.unique_ability_names):
                    if (ability_name not in duplicated_ability_names):
                        duplicated_ability_names.append(ability_name)
                else:
                    self.unique_ability_names.append(ability_name)
        for name in self.unique_ability_names:
            if name in duplicated_ability_names:
                self.unique_ability_names.remove(name)

    def split_class_abilities(self):
        """
        Create 
        """
        self.class_abilities = []

        self.construct_class_abilities_list()

        current_file_name: str = ""
        current_file_body: list[str] = []

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                if current_file_name:
                    if current_file_name in self.unique_ability_names:
                        self.class_abilities.append(raw_file(name=current_file_name, body=current_file_body))
                current_file_name = re.sub(r"^## Level \d+:\s*", "", line)
                current_file_body = []
            else:
                current_file_body.append(line)

        return self.class_abilities

    # TODO: Strip the two empty lines from abilities that remain
    # TODO: Find a nice way to handle Blessed warrior from Paladin
    # TODO: Find a nice way to handle subclasses
    # TODO: Find a nice way to add the basic class info
    def replace_class_abilities_with_links(self):
        # Replace the class abilities in the file body with links to the corresponding files
        new_body: list[str] = []
        ability_content_being_removed : bool = False

        for name in self.unique_ability_names:
            print(f"name = {name}")

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_1_HEADER}") or line.startswith(f"{LEVEL_2_HEADER}"):
                new_body.append(line)
                if line.startswith(f"{LEVEL_2_HEADER}Level"):
                    ability_name = re.sub(r"^## Level \d+:\s*", "", line)
                    ability_content_being_removed = False
                    if ability_name in self.unique_ability_names:
                        print(f"unique: {ability_name}")
                        new_body.append(f"![[{ability_name}]]")
                        ability_content_being_removed = True
                    else:
                        print(f"dupe: {ability_name}")
            elif not ability_content_being_removed:
                new_body.append(line)

        self.class_file.body = new_body

    def print_to_files(self):
        write_file(self.class_file.name, self.class_file.body, CLASSES_FILES_OUTPUT_DIR)
        for file in self.class_abilities:
            write_file(file.name, file.body, CLASS_ABILITIES_OUTPUT_DIR)

    def do_all(self):
        self.reformat_title_stile()
        self.remove_bold()
        self.add_linking()
        self.split_class_abilities()
        self.replace_class_abilities_with_links()
        self.print_to_files()

    def log_class_attributes(self):
        logging.info(f"class name: {self.class_name}")
        for file in self.class_abilities:
            logging.info(f"class ability:{file.name}")