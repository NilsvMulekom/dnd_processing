import shutil
from pathlib import Path

from constants import OUTPUT_DIR, CLASSES_OUTPUT_ROOT, CLASSES_FILES_OUTPUT_DIR, CLASS_ABILITIES_OUTPUT_DIR 

def create_output_dirs():
    output_dir = Path(OUTPUT_DIR)
    # Create output dir, if it already exists delete the old version first
    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(exist_ok=True)
    CLASSES_OUTPUT_ROOT.mkdir(exist_ok=True)
    CLASSES_FILES_OUTPUT_DIR.mkdir(exist_ok=True)
    CLASS_ABILITIES_OUTPUT_DIR.mkdir(exist_ok=True)