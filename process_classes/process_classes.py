
from constants import CLASSES_FILES_OUTPUT_DIR
from convenience_functions import open_file, write_file, create_output_dirs
from custom_types import raw_file

def main():
    create_output_dirs()

    file : raw_file = open_file()

    write_file(file.name, file.body, CLASSES_FILES_OUTPUT_DIR)
main()