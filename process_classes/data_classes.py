from pathlib import Path
import re
import logging
logging.basicConfig(level=logging.INFO)
from dataclasses import dataclass, field

from constants import OUTPUT_DIR, SUBCLASSES_DIR, CLASS_ABILITIES_DIR, LEVEL_1_HEADER, LEVEL_2_HEADER
from custom_types import TextFile, ClassTextFile
from file_handling import write_text_file

# Ability names that are also in other classes
ABILITY_NAMES_BLACKLIST = [
    "Extra Attack",
    "Spellcasting",
]
@dataclass(slots=True)
class SubClass:
    name           : str
    sub_class_file : TextFile
    abilities      : list[TextFile] = field(default_factory=list)

    # A dict that contains all abilities in a string. The bool indicates if the ability is unique
    __ability_names: dict[str, bool] = field(default_factory=dict)

    def write_to_files(self, output_dir : Path = ""):
        if output_dir != "":
            write_text_file(self.sub_class_file, output_dir)
            for ability in self.abilities:
                write_text_file(ability, output_dir / CLASS_ABILITIES_DIR)
        else:
            logging.error("SubClass.write_to_files: output_dir not set")

    def __post_init__(self):
        self.__construct_class_abilities_list()
        self.__split_class_abilities()
        self.__replace_unique_abilities_with_links()

    def __add_unique_ability(self, ability_file : TextFile):
        if ability_file.name != "":

            if ability_file.name in self.__ability_names.keys():
                if self.__ability_names[ability_file.name]:
                    self.abilities.append(ability_file)
            else:
                logging.error(f"split_class_abilities: ability name {ability_file.name} not in ability_names")

    def log_unique_ability_names(self):
        for ability, is_unique in self.__ability_names.items():
            logging.info(f"Ability: {ability}. unique: {is_unique}")

    def __construct_class_abilities_list(self):
        """
        Run over all headings in the file that contain level and construct a list of only the unique ability names.
        """
        ABILITY_HEADER_PATTERN = re.compile(r"^## Level \d+:\s*")
        for line in self.sub_class_file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                ability_name: str = ABILITY_HEADER_PATTERN.sub("", line)
                if ability_name in self.__ability_names:
                    self.__ability_names[ability_name] = False
                else:
                    self.__ability_names[ability_name] = True

    def __split_class_abilities(self):
        """
        Make an ability file for each unique ability, thy are denoted with a level 2 heading in the sub_class_file
        """
        ability_file : TextFile = TextFile(name = "", body = [])

        for line in self.sub_class_file.body:
            if line.startswith(f"{LEVEL_2_HEADER}Level"):
                self.__add_unique_ability(ability_file)
                ability_file : TextFile = TextFile(name = re.sub(r"^## Level \d+:\s*", "", line), body = [])
            elif ability_file.name != "":
                ability_file.body.append(line)
        self.__add_unique_ability(ability_file)

    def __replace_unique_abilities_with_links(self):
        """
        Runs through the sub_class_file, removes any text that is also present in abilities and replaces it with a link to that ability
        """
        new_body: list[str] = []
        ability_content_being_removed = False

        for line in self.sub_class_file.body:
            if line.startswith(LEVEL_1_HEADER):
                # Remove the class/subclass name from the file
                pass
            elif line.startswith(LEVEL_2_HEADER):
                new_body.append(line)
                ability_name = re.sub(r"^## Level \d+:\s*", "", line)
                ability_content_being_removed = False
                if self.__ability_names[ability_name] and ability_name not in ABILITY_NAMES_BLACKLIST:
                    new_body.append(f"![[{ability_name}]]")
                    ability_content_being_removed = True
            elif not ability_content_being_removed:
                new_body.append(line)

        self.sub_class_file.body = new_body

@dataclass(slots=True)
class BaseClass:
    name        : str
    class_file  : ClassTextFile
    sub_classes : list[SubClass] = field(default_factory=list)

    def __post_init__(self):
        self.__split_into_sub_classes()

    def __add_sub_class(self, sub_class_file: TextFile):
        """
        Add Textfile containing subclass body to sub_classes list
        """
        if sub_class_file.name != "":
            self.sub_classes.append(SubClass(
                name           = sub_class_file.name, 
                sub_class_file = sub_class_file
            ))

    def __split_into_sub_classes(self):
        """
        Cut the file into a file for the base class and each subclass. They are denoted with a level 1 heading in the source file.
        """
        sub_class_file : TextFile = TextFile(name = "", body = [])

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_1_HEADER}"):
                self.__add_sub_class(sub_class_file)
                class_name = line[2:]
                sub_class_file : TextFile = TextFile(name = class_name, body = [])
            if sub_class_file.name != "":
                sub_class_file.body.append(line)

        self.__add_sub_class(sub_class_file)

    def __create_index(self) -> list[str]:
        body : list[str] = []
        body.append("")
        body.append("# Sub Classes:")
        for sub_class in self.sub_classes:
            # Only add the true subclasses
            if sub_class.name != self.name:
                body.append(f"[[{sub_class.name}]]")

        return body

    def print_to_file(self):
        for sub_class in self.sub_classes:
            # Find the base class and give it a different destination
            if sub_class.name == self.name:
                sub_class.sub_class_file.body += self.__create_index()
                output_dir : Path = OUTPUT_DIR / Path(self.name)
            else:
                output_dir : Path = OUTPUT_DIR / Path(self.name) / SUBCLASSES_DIR
            sub_class.write_to_files(output_dir)
