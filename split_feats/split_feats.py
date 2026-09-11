from pathlib import Path

from file_handling import TextFile, remove_dir, open_file, write_text_file

from constants import OUTPUT_DIR, INPUT_DIR, DIAGNOSTIC_OUTPUT_DIR, FILE_NAMES_LIST_OUTPUT_DIR

def split_files(input_file : TextFile) -> list[TextFile]:
    feat_list: list[TextFile] = []
    open_feat : TextFile = TextFile(name = "", body = [])

    for line in input_file.body:
        if line.startswith("## "):
            if open_feat.name != "":
                feat_list.append(open_feat)
            # Cut off the first 3 characters to get the feat name
            feat_name: str = line[3:]
            open_feat : TextFile = TextFile(name = feat_name, body = [])
        open_feat.body.append(line)

    if open_feat.name != "":
        feat_list.append(open_feat)

    return feat_list


def main():
    remove_dir(OUTPUT_DIR)
    remove_dir(DIAGNOSTIC_OUTPUT_DIR)
    remove_dir(FILE_NAMES_LIST_OUTPUT_DIR)

    input_file : TextFile = open_file(Path(INPUT_DIR / "all_feats.md"))

    feat_list = split_files(input_file)

    for text_file in feat_list:
        write_text_file(text_file, OUTPUT_DIR)

main()