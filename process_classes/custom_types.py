import re
from dataclasses import dataclass

from constants import LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER
from file_handling import TextFile
@dataclass(slots=True)
class ClassTextFile(TextFile):
    def reformat_title_style(self):
        """
        Reformats the title style of a file.
          - Level 2 headings are changes to level 1 headings.
          - Level 4 headings are changed to level 2 headings.
          - Level 5 headings are changed to level 3 headings.
          - Lines that start bold (***tile***) are changed depending on the context:
            - If the bold header is inside a section with a level 4 heading, the header is swapped to a Level 4 heading.
            - if the bold header is inside a section with a level 2 heading and starts with Level N:, the header is swapped to a level 2 heading.
            - If the bold header is inside a section with a level 2 heading and contains mention of a level somewhere else in the line, the header is swapped to a level 2 heading.
            - If the bold header is inside a section with a level 2 heading and does not contain mention of a level somewhere in the line, the header is swapped with a level 4 heading.
            - In all cases the line is reformatted to fit the right heading type
        """
        new_body: list[str] = []
        previous_heading : str = ""
        for line in self.body:
            match True:
                case _ if line.startswith(LEVEL_2_HEADER):
                    new_line = line.replace(LEVEL_2_HEADER, LEVEL_1_HEADER)
                    previous_heading = LEVEL_2_HEADER
                case _ if line.startswith(LEVEL_4_HEADER):
                    new_line = line.replace(LEVEL_4_HEADER, LEVEL_2_HEADER)
                    previous_heading = LEVEL_4_HEADER
                case _ if line.startswith(LEVEL_5_HEADER):
                    new_line = line.replace(LEVEL_5_HEADER, LEVEL_4_HEADER)
                case _ if line.startswith(BOLD_HEADER):
                    if previous_heading == LEVEL_2_HEADER:
                        match = re.match(
                            r"^\*\*\*Level (\d+): (.*?)\.\*\*\*\s*(.*)$",
                            line,
                        )
                        if match:
                            level = int(match.group(1))
                            title = match.group(2)
                            remainder = match.group(3)

                            new_line = f"## Level {level}: {title}"
                            new_body.append(new_line)
                            new_line = remainder
                        else:
                            title_match = re.match(r"^\*\*\*(.*?)\.\*\*\*\s*(.*)$", line)
                            level_match = re.search(
                                r"(?i)(?=.*\blevel\b).*?\b([3-9]|1\d|20)(?:st|nd|rd|th)?\b",
                                line
                            )
                            if title_match and level_match:
                                title = title_match.group(1)
                                remainder = title_match.group(2)
                                level = int(level_match.group(1))

                                new_line = f"## Level {level}: {title}"
                                new_body.append(new_line)
                                new_line = remainder
                            else:
                                new_line = re.sub(r"\*\*\*(.*?)\.\*\*\*", r"#### \1\n", line)
                    elif previous_heading == LEVEL_4_HEADER:
                        new_line = re.sub(r"\*\*\*(.*?)\.\*\*\*", r"#### \1\n", line)
                case _:
                    new_line = line
            new_body.append(new_line)

        self.body = new_body

    def remove_bold(self):
        """
        Reformat file to remove any bold (*words*) text.
        """
        new_body: list[str] = []
        for line in self.body:
            new_line = re.sub(r"\*", r"", line)
            new_body.append(new_line)

        self.body = new_body

    def reformat_file(self):
        """
        Call all reformatting functions in the correct order.
        """
        self.reformat_title_style()
        self.remove_bold()
