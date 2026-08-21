from file_handling import TextFile, remove_dir, open_file, write_text_file
from custom_types import ClassTextFile
from data_classes import BaseClass, ClassSet
from constants import OUTPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, TEST_INPUT_FILE, PATTERN_LIST

from pathlib import Path

def process_class_list():
    class_files : list[ClassTextFile] = []
    class_set : ClassSet

    # TODO: open_files?
    # TODO: TextFile to ClassTextFile function
    for file_path in Path(TEST_INPUT_FILE).parent.glob("*.md"):
        file : TextFile = open_file(file_path)
        class_file : ClassTextFile = ClassTextFile(
            name = file.name,
            body = file.body,
        )
        class_files.append(class_file)

    class_set = ClassSet(class_files = class_files)
    class_set.add_linking(PATTERN_LIST)
    class_set.print_to_file()
    class_set.create_index()

def process_one():
    file : TextFile = open_file(TEST_INPUT_FILE)
    classfile = ClassTextFile(
        name = file.name,
        body = file.body,
    )
    class_file_set : BaseClass = BaseClass(name=classfile.name, class_file=classfile)

    for sub_class in class_file_set.sub_classes:
        sub_class.sub_class_file.add_linking(PATTERN_LIST)
        for ability in sub_class.abilities:
            ability.add_linking(PATTERN_LIST)

    class_file_set.print_to_file()

def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)

    # process_one()
    # process_all()
    process_class_list()


main()