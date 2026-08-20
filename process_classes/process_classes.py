from file_handling import TextFile, remove_dir, open_file
from custom_types import ClassTextFile
from data_classes import BaseClass
from constants import OUTPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, TEST_INPUT_FILE, PATTERN_LIST

from pathlib import Path

def process_all():
    class_files : list[ClassTextFile] = []

    for file_path in Path(TEST_INPUT_FILE).parent.glob("*.md"):
        file : TextFile = open_file(file_path)
        class_file : ClassTextFile = ClassTextFile(
            name = file.name,
            body = file.body,
        )
        class_files.append(class_file) 

    base_class_set : list[BaseClass] = []
    for file in class_files:
        base_class : BaseClass = BaseClass(
            name       = file.name,
            class_file = file
        )
        base_class_set.append(base_class)

    for base_class in base_class_set:
        for sub_class in base_class.sub_classes:
            sub_class.sub_class_file.add_linking(PATTERN_LIST)
            for ability in sub_class.abilities:
                ability.add_linking(PATTERN_LIST)
            sub_class.write_to_files()
        

def process_one():
    file : TextFile = open_file(TEST_INPUT_FILE)
    classfile = ClassTextFile(
        name = file.name,
        body = file.body,
    )
    class_file_set : BaseClass = BaseClass(name=classfile.name, class_file=classfile)

    for sub_class in class_file_set.sub_classes:
        sub_class.sub_class_file.add_linking(PATTERN_LIST)
        sub_class.log_unique_ability_names()
        for ability in sub_class.abilities:
            ability.add_linking(PATTERN_LIST)
        sub_class.write_to_files()

def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)

    # process_one()
    process_all()





main()