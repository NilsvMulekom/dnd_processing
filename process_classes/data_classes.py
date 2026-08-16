import re
import logging
logging.basicConfig(level=logging.INFO)
from dataclasses import dataclass, field

#TODO: define
from constants import *
from custom_types import TextFile, ClassTextFile

# TODO: Find clean way to differentiate between class and subclass.
#       - Only print in BassClass
#       - Output dir as parameter
#       - Separate diag folder
@dataclass(slots=True)
class SubClass:
    name           : str
    sub_class_file : TextFile
    abilities      : list[TextFile] = field(default_factory=list)

    # A dict that contains all abilities in a string. The bool indicates if the ability is unique
    __ability_names: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self):
        self.__construct_class_abilities_list()

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

    def log_unique_ability_names(self):
        for ability, is_unique in self.__ability_names.items():
            logging.info(f"Ability: {ability}. unique: {is_unique}")

@dataclass(slots=True)
class BaseClass:
    name        : str
    class_file  : ClassTextFile
    sub_classes : list[SubClass] = field(default_factory=list)

    def add_sub_class(self, sub_class_file: TextFile):
        """
        Add Textfile containing subclass body to sub_classes list
        """
        if sub_class_file.name != "":
            self.sub_classes.append(SubClass(
                name           = sub_class_file.name, 
                sub_class_file = sub_class_file
            ))

    def split_into_sub_classes(self):
        sub_class_file : TextFile = TextFile(name = "", body = [])

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_1_HEADER}"):
                self.add_sub_class(sub_class_file)
                class_name = line[2:]
                sub_class_file : TextFile = TextFile(name = class_name, body = [])
            if sub_class_file.name != "":
                sub_class_file.body.append(line)

        self.add_sub_class(sub_class_file)

    
