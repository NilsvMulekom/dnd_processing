from file_handling import TextFile, remove_dir, open_file, write_text_file
from custom_types import ClassTextFile
from data_classes import BaseClass, ClassSet
from constants import OUTPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, TEST_INPUT_FILE, PATTERN_LIST, FILE_NAMES_LIST_OUTPUT_DIR

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

def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)
    remove_dir(FILE_NAMES_LIST_OUTPUT_DIR)

    process_class_list()


main()