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

    
