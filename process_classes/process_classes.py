import re
import logging
from constants import CLASSES_FILES_OUTPUT_DIR, CLASS_ABILITIES_OUTPUT_DIR
from convenience_functions import open_file, open_all_files, write_file, create_output_dirs
from custom_types import raw_file
from constants import PATTERN_LIST, LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER
from data_classes import ClassFileSet
# TODO: Add core traits
# TODO: add class table

def main():
    create_output_dirs()

    # files : list[raw_file] = open_all_files()
    # for file in files:
    #     file = reformat_title_stile(file)
    #     file = remove_bold(file)
    #     file = add_linking(file)
    #     write_file(file.name, file.body, CLASSES_FILES_OUTPUT_DIR)

    file : raw_file = open_file()
    class_file_set : ClassFileSet = ClassFileSet(class_name=file.name, class_file=file, class_abilities=[])
    class_file_set.do_all()
main()