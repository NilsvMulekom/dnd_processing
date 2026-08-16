import re

from dataclasses import dataclass, field


#TODO: define
from constants import *
from custom_types import TextFile
from convenience_functions import write_text_file

# TODO: Find clean way to differentiate between class and subclass.
#       - Only print in BassClass
#       - Output dir as parameter
#       - Separate diag folder
@dataclass(slots=True)
class SubClass:
    name           : str
    sub_class_file : TextFile
    abilities      : list[TextFile] = field(default_factory=list)

    # TODO: Change to diagnostic?
    def print_sub_class_file(self):
        write_text_file(self.sub_class_file, CLASSES_FILES_OUTPUT_DIR)

@dataclass(slots=True)
class BaseClass:
    name        : str
    class_file  : TextFile
    sub_classes : list[SubClass] = field(default_factory=list)

    # TODO: Apply on file class
    def reformat_title_style(self):
        """
        Reformats the title style of a file.
          - Level 2 headings are changes to level 1 headings
          - Level 4 headings are changed to level 2 headings
          - Level 5 headings are changed to level 3 headings
          - Lines that start bold (***tile***) are changed to level 5 headings
        """
        new_body: list[str] = []
        for line in self.class_file.body:
            match True:
                case _ if line.startswith(LEVEL_2_HEADER):
                    new_line = line.replace(LEVEL_2_HEADER, LEVEL_1_HEADER)
                case _ if line.startswith(LEVEL_4_HEADER):
                    new_line = line.replace(LEVEL_4_HEADER, LEVEL_2_HEADER)
                case _ if line.startswith(LEVEL_5_HEADER):
                    new_line = line.replace(LEVEL_5_HEADER, LEVEL_4_HEADER)
                case _ if line.startswith(BOLD_HEADER):
                    new_line = re.sub(r"\*\*\*(.*?)\.\*\*\*", r"#### \1\n", line)
                case _:
                    new_line = line
            new_body.append(new_line)

        self.class_file.body = new_body

    # TODO: Apply on file class
    def remove_bold(self):
        """
        Reformat file to remove any bold (*words*) text
        """
        new_body: list[str] = []
        for line in self.class_file.body:
            new_line = re.sub(r"\*", r"", line)
            new_body.append(new_line)

        self.class_file.body = new_body

    # TODO: Apply on file class
    def reformat_class_file(self):
        self.reformat_title_style()
        self.remove_bold()

    # TODO: Change to diagnostic?
    def print_class_file(self):
        write_text_file(self.class_file, CLASSES_FILES_OUTPUT_DIR)