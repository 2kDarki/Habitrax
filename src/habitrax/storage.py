from pathlib import Path
import json
import os

# Dynamically resolve the main folder
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
if not os.path.isdir(DATA_DIR):
    DATA_DIR.mkdir()
    
# File name constants
STAT_MAP = 'stat_map.json'
USER_FILE = 'user_data.json'
DATA_FILE = 'log_data.json'
LEVEL_FILE = 'level_data.json'
TASK_FILE = 'mission_data.json'
QUESTIONS = 'questions.json'
REFLECTIONS = 'reflections.json'
JOURNAL = 'journal.json'
NOTEBOOK = 'notebook.json'
TRASHCAN = 'trashcan.json'
SLIGHT_EDGE = 'slight_edge.json'
SERVICES = 'services_ledger.json'
GRACES = 'gratitudes.json'
COFFER = 'coffer.json'

# Load data safely from a file
def load_data(file):
    file_path = DATA_DIR / file
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Load stats map
def load_map():
    STAT_MAP_FILE = DATA_DIR / STAT_MAP
    if not STAT_MAP_FILE.exists():
        return {"Renames": {}, "Combinations": {}}
    with open(STAT_MAP_FILE, "r") as f:
        return json.load(f)

# Save data to a file (overwrites)
def save_data(file, data):
    file_path = DATA_DIR / file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Add one entry to a file (append style)
def save_entry(file, entry):
    data = load_data(file)
    data.append(entry)
    save_data(file, data)