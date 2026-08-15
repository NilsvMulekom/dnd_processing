from dataclasses import dataclass, field

import logging
logging.basicConfig(level=logging.INFO)

import re
from constants import CLASS_ABILITIES_OUTPUT_DIR, CLASSES_FILES_OUTPUT_DIR, LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER, PATTERN_LIST
from custom_types import raw_file
from convenience_functions import write_file

@dataclass(slots=True)
class SubClassFileSet:
    name : str
    file : raw_file

    abilities : list[raw_file] = field(default_factory=list)

    __unique_ability_names: list[str] = field(default_factory=list)

    # TODO: Do on project level
    def add_linking(self):
        # Replace all instances of patterns in the file body with links to the corresponding files
        new_body: list[str] = []

        pattern_list = [pattern for pattern in PATTERN_LIST if pattern != self.file.name]
        pattern = re.compile("|".join(re.escape(s) for s in pattern_list))
        for line in self.file.body:
            new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
            new_body.append(new_line)

        self.file.body = new_body

    # TODO: Let copilot check for improvements
    def construct_class_abilities_list(self) -> list[str]:
        """
            Run over all headings in the file that contain level and return only the unique ability names.
        """
        
        duplicated_ability_names: list[str] = []

        for line in self.file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                ability_name : str = re.sub(r"^## Level \d+:\s*", "", line)
                if (ability_name in self.__unique_ability_names):
                    if (ability_name not in duplicated_ability_names):
                        duplicated_ability_names.append(ability_name)
                else:
                    self.__unique_ability_names.append(ability_name)
        for name in self.__unique_ability_names:
            if name in duplicated_ability_names:
                self.__unique_ability_names.remove(name)

    def split_class_abilities(self):

        self.construct_class_abilities_list()

        current_file_name: str = ""
        current_file_body: list[str] = []

        for line in self.file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                if current_file_name:
                    if current_file_name in self.__unique_ability_names:
                        self.abilities.append(raw_file(name=current_file_name, body=current_file_body))
                current_file_name = re.sub(r"^## Level \d+:\s*", "", line)
                current_file_body = []
            else:
                current_file_body.append(line)

    # TODO: Strip the two empty lines from abilities that remain
    # TODO: Find a nice way to handle Blessed warrior from Paladin
    # TODO: Find a nice way to handle extra attack
    # TODO: Find a nice way to handle subclasses
    # TODO: Find a nice way to add the basic class info
    def replace_class_abilities_with_links(self):
        # Replace the class abilities in the file body with links to the corresponding files
        new_body: list[str] = []
        ability_content_being_removed : bool = False

        for name in self.__unique_ability_names:
            print(f"name = {name}")

        for line in self.file.body:
            if line.startswith(f"{LEVEL_1_HEADER}") or line.startswith(f"{LEVEL_2_HEADER}"):
                new_body.append(line)
                if line.startswith(f"{LEVEL_2_HEADER}Level"):
                    ability_name = re.sub(r"^## Level \d+:\s*", "", line)
                    ability_content_being_removed = False
                    if ability_name in self.__unique_ability_names:
                        new_body.append(f"![[{ability_name}]]")
                        ability_content_being_removed = True
            elif not ability_content_being_removed:
                new_body.append(line)

        self.file.body = new_body

    def print_to_files(self):
        write_file(self.file.name, self.file.body, CLASSES_FILES_OUTPUT_DIR)
        for file in self.abilities:
            write_file(file.name, file.body, CLASS_ABILITIES_OUTPUT_DIR)

    def print_input_file(self):
        """Diagnostic method to print the processed file"""
        write_file(f"{self.file.name}_input_print", self.file.body, CLASSES_FILES_OUTPUT_DIR)

    def do_all(self):
        self.add_linking()
        self.split_class_abilities()
        self.replace_class_abilities_with_links()
        self.print_to_files()

    def log_class_attributes(self):
        logging.info(f"class name: {self.name}")
        for file in self.subclass_abilities:
            logging.info(f"class ability:{file.name}")

@dataclass(slots=True)
class BaseClassFileSet:
    class_name: str
    input_file  : raw_file
    class_files : list[SubClassFileSet]

    def add_sub_class(self, class_file: raw_file):
        if class_file.name is not None:
            
            self.class_files.append(SubClassFileSet(
                name = class_file.name,
                file = class_file,
            ))

    # TODO: reformat ">" bits
    def reformat_title_stile(self):
        # Reformat the title style of the file body
        new_body: list[str] = []

        # Reformat the title style of the file body
        for line in self.input_file.body:
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

        self.input_file.body = new_body

    def remove_bold(self):
        # Remove bold formatting from the file body
        new_body: list[str] = []

        for line in self.input_file.body:
            new_line = re.sub(r"\*", r"", line)
            new_body.append(new_line)

        self.input_file.body = new_body

    def split_into_sub_classes(self):
        new_file : raw_file = raw_file(name = "", body = [])

        for line in self.input_file.body:
            if line.startswith(f"{LEVEL_1_HEADER}"):
                self.add_sub_class(new_file)
                class_name = line[2:]
                new_file : raw_file = raw_file(name = class_name, body = [])
            if new_file.name != "":
                new_file.body.append(line)

        self.add_sub_class(new_file)

    def print_input_file(self):
        """Diagnostic method to print the processed input_file"""
        write_file(f"{self.input_file.name}_input_print", self.input_file.body, CLASSES_FILES_OUTPUT_DIR)

    # def print_class_files(self):
    #     for class_file in self.class_files:
    #         write_file(class_file.subclass_name, class_file.output_file.body, CLASSES_FILES_OUTPUT_DIR)

    def strip_file_into_subclasses():
        print("henk")

    def do_all(self):
        self.reformat_title_stile()
        self.remove_bold()
        self.print_input_file()
        self.split_into_sub_classes()
        # self.print_class_files()
        for class_file in self.class_files:
            class_file.do_all()