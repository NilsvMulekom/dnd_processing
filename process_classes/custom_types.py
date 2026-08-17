import re
from dataclasses import dataclass

from constants import LEVEL_1_HEADER, LEVEL_2_HEADER, LEVEL_4_HEADER, LEVEL_5_HEADER, BOLD_HEADER
from file_handling import TextFile

BOLD_LEVEL_HEADER_PATTERN = re.compile(r"^\*\*\*Level (\d+): (.*?)\.\*\*\*\s*(.*)$")
BOLD_TITLE_PATTERN = re.compile(r"^\*\*\*(.*?)\.\*\*\*\s*(.*)$")
IMPLICIT_LEVEL_HEADER_PATTERN = re.compile(
    r"(?i)^\s*(?:"
    r"\*?([3-9]|1\d|20)(?:st|nd|rd|th)-level\b"
    r"|(?:at|starting at|beginning at)\s+([3-9]|1\d|20)(?:st|nd|rd|th)?\s+level\b"
    r"|(?:starting\s+)?when you (?:choose|reach).*?\bat\s+([3-9]|1\d|20)(?:st|nd|rd|th)?\s+level\b"
    r")"
)

@dataclass(slots=True)
class ClassTextFile(TextFile):
    def reformat_bold_header(self, line: str, previous_heading: str) -> list[str]:
        """
        AI generated regex magic helper function for reformat_title_style
        """
        if previous_heading == LEVEL_2_HEADER:
            level_header_match = BOLD_LEVEL_HEADER_PATTERN.match(line)
            if level_header_match:
                level = int(level_header_match.group(1))
                title = level_header_match.group(2)
                remainder = level_header_match.group(3)

                return [f"## Level {level}: {title}", remainder]

            title_match = BOLD_TITLE_PATTERN.match(line)
            remainder = title_match.group(2) if title_match else ""
            level_match = IMPLICIT_LEVEL_HEADER_PATTERN.search(remainder)
            if title_match and level_match:
                title = title_match.group(1)
                level = int(next(group for group in level_match.groups() if group))

                return [f"## Level {level}: {title}", remainder]

        return [re.sub(r"\*\*\*(.*?)\.\*\*\* ", r"#### \1\n", line)]

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
            new_lines: list[str]
            match True:
                case _ if line.startswith(LEVEL_2_HEADER):
                    new_lines = [line.replace(LEVEL_2_HEADER, LEVEL_1_HEADER)]
                    previous_heading = LEVEL_2_HEADER
                case _ if line.startswith(LEVEL_4_HEADER):
                    new_lines = [line.replace(LEVEL_4_HEADER, LEVEL_2_HEADER)]
                    previous_heading = LEVEL_4_HEADER
                case _ if line.startswith(LEVEL_5_HEADER):
                    new_lines = [line.replace(LEVEL_5_HEADER, LEVEL_4_HEADER)]
                case _ if line.startswith(BOLD_HEADER):
                    new_lines = self.reformat_bold_header(line, previous_heading)
                case _:
                    new_lines = [line]
            new_body.extend(new_lines)

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
