from dataclasses import dataclass, field


#TODO: define
from constants import *
from custom_types import TextFile, ClassTextFile
from file_handling import write_text_file

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
    class_file  : ClassTextFile
    sub_classes : list[SubClass] = field(default_factory=list)
