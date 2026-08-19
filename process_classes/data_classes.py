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
@dataclass(slots=True)
class SubClass:
    name           : str
    sub_class_file : TextFile
    abilities      : list[TextFile] = field(default_factory=list)

    # A dict that contains all abilities in a string. The bool indicates if the ability is unique
    __ability_names: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self):
        self.__construct_class_abilities_list()
        self.__split_class_abilities()
        self.__replace_unique_abilities_with_links()

    def add_unique_ability(self, ability_file : TextFile):
        if ability_file.name != "":

            if ability_file.name in self.__ability_names.keys():
                if self.__ability_names[ability_file.name]:
                    print(ability_file.name)
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
                self.add_unique_ability(ability_file)
                ability_file : TextFile = TextFile(name = re.sub(r"^## Level \d+:\s*", "", line), body = [])
            elif ability_file.name != "":
                ability_file.body.append(line)
        self.add_unique_ability(ability_file)

    # TODO: write again
    # TODO: (Martials) : Fix Extra attack
    # TODO: (Barbarian): Fix Improved Brutal Strike
    # TODO: (Paladin)  : Fix blessed warrior

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
                if self.__ability_names[ability_name]:
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
        self.split_into_sub_classes()

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
        """
        Cut the file into a file for the base class and each subclass. They are denoted with a level 1 heading in the source file.
        """
        sub_class_file : TextFile = TextFile(name = "", body = [])

        for line in self.class_file.body:
            if line.startswith(f"{LEVEL_1_HEADER}"):
                self.add_sub_class(sub_class_file)
                class_name = line[2:]
                sub_class_file : TextFile = TextFile(name = class_name, body = [])
            if sub_class_file.name != "":
                sub_class_file.body.append(line)

        self.add_sub_class(sub_class_file)

    
