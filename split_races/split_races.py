from pathlib import Path
import re

from file_handling import TextFile, remove_dir, open_file, write_text_file

from constants import OUTPUT_DIR, INPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, FILE_NAMES_LIST_OUTPUT_DIR, PATTERN_LIST

# TODO: properly make headings
# TODO: no linking in headings

def split_files(input_file : TextFile) -> list[TextFile]:
    race_list: list[TextFile] = []
    open_race : TextFile = TextFile(name = "", body = [])

    for line in input_file.body:
        if len(open_race.body) == 0 and line == "":
            # Remove the first line if it is empty
            pass
        elif open_race.name != "":
            # End of the race
            if line.startswith("---"):
                # Close race and add to list
                race_list.append(open_race)
                open_race : TextFile = TextFile(name = "", body = [])
            else:
                open_race.body.append(line)
        elif line.startswith("## "):
          # Cut off the first 3 characters to get the race name
            race_name: str = line[3:]
            open_race.name = race_name

    return race_list

def add_linking(input_file : TextFile) -> TextFile:

    new_body: list[str] = []

    escaped_patterns = [re.escape(s) for s in sorted(PATTERN_LIST, key=len, reverse=True)]
    pattern = re.compile(rf"(?<!\w)({'|'.join(escaped_patterns)})(?!\w)")
    for line in input_file.body:
        new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
        new_body.append(new_line)

    return TextFile(name = input_file.name, body = new_body)

def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)
    remove_dir(FILE_NAMES_LIST_OUTPUT_DIR)

    input_file : TextFile = open_file(Path(INPUT_DIR / "all_races.md"))

    race_list = split_files(input_file)

    for text_file in race_list:
        linked_file : TextFile = add_linking(text_file)
        write_text_file(linked_file, OUTPUT_DIR)

main()