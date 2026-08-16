from file_handling import TextFile, remove_dir, open_file
from custom_types import ClassTextFile
from data_classes import BaseClass
from constants import OUTPUT_DIR, TEST_INPUT_FILE

def main():
    remove_dir(OUTPUT_DIR)

    file : TextFile = open_file(TEST_INPUT_FILE)
    classfile = ClassTextFile(
        name = file.name,
        body = file.body,
    )
    class_file_set : BaseClass = BaseClass(name=classfile.name, class_file=classfile)
    class_file_set.class_file.reformat_file()
    class_file_set.class_file.diagnostic_print_to_file()

main()