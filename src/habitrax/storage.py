from pathlib import Path
import json
import os

# Dynamically resolve the main folder
DROOT    = Path(__file__).parent.parent.parent
DATA_DIR = DROOT / "data"

STAT_MAP    = 'stat_map.json'
USER_FILE   = 'user_data.json'
DATA_FILE   = 'log_data.json'
LEVEL_FILE  = 'level_data.json'
S_LVL       = 'stat_levels.json'
TASK_FILE   = 'mission_data.json'
QUESTIONS   = 'questions.json'
REFLECTIONS = 'reflections.json'
JOURNAL     = 'journal.json'
NOTEBOOK    = 'notebook.json'
TRASHCAN    = 'trashcan.json'
SLIGHT_EDGE = 'slight_edge.json'
SERVICES    = 'services_ledger.json'
GRACES      = 'gratitudes.json'
COFFER      = 'coffer.json'

# Load data safely from a file
def load_data(file: str) -> list | dict:
    file_path = DATA_DIR / file
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Load stats map
def load_map() -> dict:
    STAT_MAP_FILE = DATA_DIR / STAT_MAP
    if not STAT_MAP_FILE.exists():
        return {"Renames": {}, "Combinations": {}}
    with open(STAT_MAP_FILE, "r") as f:
        return json.load(f)

# Save data to a file (overwrites)
def save_data(file: str, data: list | dict):
    file_path = DATA_DIR / file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Add one entry to a file (append style)
def save_entry(file: str, entry: dict):
    data = load_data(file)
    data.append(entry)
    save_data(file, data)

def delete(file: str):
    path = DATA_DIR / file
    if os.path.exists(path):
        if   os.path.isfile(path): save_data(file, {})
        elif os.path.isdir( path): shutil.rmtree(path)