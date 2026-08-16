from convenience_functions import remove_output_dir, open_file
from custom_types import TextFile
from data_classes import BaseClass

def main():
    remove_output_dir()

    file : TextFile = open_file()
    class_file_set : BaseClass = BaseClass(name=file.name, class_file=file)
    class_file_set.reformat_class_file()
    class_file_set.print_class_file()

main()