import re
from dataclasses import dataclass

from constants import LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER
from constants import DIAGNOSTIC_OUTPUT_DIR
from file_handling import TextFile, write_text_file

@dataclass(slots=True)
class ClassTextFile(TextFile):
    def reformat_title_style(self):
        """
        Reformats the title style of a file.
          - Level 2 headings are changes to level 1 headings
          - Level 4 headings are changed to level 2 headings
          - Level 5 headings are changed to level 3 headings
          - Lines that start bold (***tile***) are changed to level 5 headings
        """
        new_body: list[str] = []
        for line in self.body:
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

        self.body = new_body

    def remove_bold(self):
        """
        Reformat file to remove any bold (*words*) text
        """
        new_body: list[str] = []
        for line in self.body:
            new_line = re.sub(r"\*", r"", line)
            new_body.append(new_line)

        self.body = new_body

    def reformat_file(self):
        self.reformat_title_style()
        self.remove_bold()
