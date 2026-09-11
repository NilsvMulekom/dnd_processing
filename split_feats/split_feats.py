from pathlib import Path
import re

from file_handling import TextFile, remove_dir, open_file, write_text_file

from constants import OUTPUT_DIR, INPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, FILE_NAMES_LIST_OUTPUT_DIR, PATTERN_LIST

def split_files(input_file : TextFile) -> list[TextFile]:
    feat_list: list[TextFile] = []
    open_feat : TextFile = TextFile(name = "", body = [])

    for line in input_file.body:
        if len(open_feat.body) == 0 and line == "":
            # Remove the first line if it is empty
            pass
        elif open_feat.name != "":
            # End of the feat
            if line.startswith("---"):
                # Close feat and add to list
                feat_list.append(open_feat)
                open_feat : TextFile = TextFile(name = "", body = [])
            else:
                open_feat.body.append(line)
        elif line.startswith("## "):
          # Cut off the first 3 characters to get the feat name
            feat_name: str = line[3:]
            open_feat.name = feat_name

    return feat_list

def add_linking(input_file : TextFile) -> TextFile:

    new_body: list[str] = []

    pattern = re.compile("|".join(re.escape(s) for s in PATTERN_LIST))
    for line in input_file.body:
        new_line = pattern.sub(lambda m: f"[[{m.group(0)}]]", line)
        new_body.append(new_line)

    return TextFile(name = input_file.name, body = new_body)

def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)
    remove_dir(FILE_NAMES_LIST_OUTPUT_DIR)

    input_file : TextFile = open_file(Path(INPUT_DIR / "all_feats.md"))

    feat_list = split_files(input_file)

    for text_file in feat_list:
        linked_file : TextFile = add_linking(text_file)
        write_text_file(linked_file, OUTPUT_DIR)

main()