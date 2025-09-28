"""
Entry point of the Questline CLI application (Habitrax)
Displays the main menu and routes to each core module
"""
from .toolbox import center, color, clear, clear_screen
from .toolbox import warning, choose_from, list_options
from . import status_window
from . import soul_work
from . import notebook
from . import debrief
from . import profile
from . import storage
from . import logger
from . import config
from . import stats
from . import tasks
import os

# Runs the setup menu once or if USER_FILE is missing
USER_FILE = storage.DATA_DIR / storage.USER_FILE
if not os.path.exists(USER_FILE):
    from . import setup

def main():
    header = center("《 QUESTLINE 》", 0, 1)
    print(header)
    
    options = {       
        "Log session": logger.log_session,
        "Mission center": tasks.menu,
        "Debrief": debrief.menu,
        "Soul work": soul_work.menu,
        "View Status Window": status_window.window,
        "Statistics": stats.menu,        
        "Notebook": notebook.menu,
        "Profile": profile.menu,
        "Settings": config.menu
    }

    while True:
        print()
        list_options(options, "Choose action")
        print(f"{len(options)+1}. Exit")
        
        opt = input(color(">>> ", "magenta"))
        try:
            # Convert user input to index, call the 
            # associated function
            choice = int(opt) - 1
            choose_from(options, choice)()
        except (ValueError, StopIteration):
            # Special command to clear screen
            if opt == "clear":
                clear()
                continue
            # Exit condition
            elif opt == str(len(options)+1):
                clear_screen()
                break
            # Invalid input handling
            else:
                warning(f"\nInvalid choice. Choose from 1 to {len(options)+1}.")
                continue

if __name__ == '__main__':
    main()

