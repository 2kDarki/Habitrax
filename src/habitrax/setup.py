from .toolbox import warning, timetools, iter_print
from .toolbox import clear, color, center
from . import storage
import time
import os

USER_FILE_PATH = storage.DATA_DIR / storage.USER_FILE

def user_exists():
    return os.path.exists(USER_FILE_PATH)

def commandments():
    print(color("\nEnter commandments one by one. Type 'done' when finished:\n", "yellow"))
    
    decalogue = []
    while True:
        commandment = input(color(
            f"Commandment {len(decalogue)+1}: ",
            "cyan")).strip()
        # Stops input if user types 'done'
        if commandment.lower() == "done":
            break
        elif commandment:
            decalogue.append(commandment)
    
    return decalogue

def setup_user():
    print("\n"+center(" 《 HABITRAX SETUP 》 ", 0, 1))
    print("\nWelcome! Let's get a few details to personalize your experience.\n")

    user_data = {}
    user_data["Name"] = input(color(
        "Your name or nickname: ", "cyan")).strip()
    
    while True:
        try:
            user_data["Birthday"] = timetools.to_iso(
                input(color(
                "Your birthday (YYYY-MM-DD): ", 
                "cyan")).strip())
            if user_data["Birthday"] is None:
                raise ValueError
            break
        except ValueError:
            warning("Invalid format! Try again.")
    
    user_data["Timezone"] = input(color(
        "Your timezone (e.g., CAT): ", "cyan")).strip()

    user_data["Aim"] = input(color("Your chief aim: ", 
        "cyan")).strip()
    
    prompt = input(f"\nDo you want to write your commandments? [y/n]\n{color('>>> ', 'magenta')}")
    if prompt and prompt[0].lower() == "y":
        user_data["Decalogue"] = commandments()
    
    storage.save_data(storage.USER_FILE, user_data)

    footer = center(" Setup complete! ", 1)
    print(f"\n{footer}\n")
    time.sleep(.75)
    print(color("Launching Habitrax", "green"), end="", 
        flush=True)
    time.sleep(1)
    iter_print(color(".", "green"), times=3, end="", 
        delay=.75)
    time.sleep(1)
    clear(print_header=False)

def run_if_needed():
    if not user_exists():
        try:
            setup_user()
        except KeyboardInterrupt:
            print(color(
                "\n\nSetup cancelled by user.\n", 
                "red"
            ))

if __name__ != "__main__":
    run_if_needed()