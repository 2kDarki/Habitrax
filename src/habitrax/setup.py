from .toolbox import clear, color, center, underline
from .toolbox import warning, timetools, iter_print
from . import storage
import time, os

USER_FILE_PATH = storage.DATA_DIR / storage.USER_FILE

def user_exists():
    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH) as f:
            if len(list(f)) > 1: return True

def commandments():
    print(color("\nEnter commandments one by one. "
         +"Type 'done' when finished:\n", "yellow"))
    
    decalogue = []
    while True:
        commandment = input(color(
            f"Commandment {len(decalogue)+1}: ",
            "cyan")).strip()
        
        # Stops input if user types 'done'
        if commandment.lower() == "done": break
        elif commandment: decalogue.append(commandment)
    
    return decalogue

def setup_user():
    print("\n"+center(" 《 HABITRAX SETUP 》 ", "="))
    print("\nWelcome! Let's get a few details to "
         +"personalize your experience.\n")

    user_data = {}
    user_data["Name"] = input(color(
        "Your name or nickname: ", "cyan")).strip()
    
    name = user_data.get("Name", None)
    while True:
        try: 
            user_data["Birthday"] = timetools.to_iso(
            input(color("Your birthday (YYYY-MM-DD): ", 
            "cyan")).strip())
            if user_data["Birthday"] is None:
                raise ValueError
            break
        except ValueError:
            warning("Invalid format! Try again.")
    
    user_data["Aim"] = input(color("Your chief aim: ", 
                       "cyan")).strip()    
    prompt = input("\nDo you want to write your "
           + "commandments? [y/n]\n"
           + f"{color('>>> ', 'magenta')}")
    
    if prompt and prompt[0].lower() == "y":
        user_data["Decalogue"] = commandments()
    
    if name:
        print("\n"+color(f"Welcome, {name}!", "green"))
    storage.save_data(storage.USER_FILE, user_data)
    footer = center(" Setup complete! ", "—")
    print(f"\n{footer}\n")
    time.sleep(.75)
    print(color("Launching Habitrax", "green"), end="", 
        flush=True)
    time.sleep(1)
    iter_print(color(".", "green"), times=3, end="", 
        delay=.75)
    time.sleep(1)
    clear(print_header=False)

if __name__ != "__main__": 
    if not user_exists():
        try: setup_user()
        except (KeyboardInterrupt, EOFError) as e:
            if not isinstance(e, EOFError): print()
            warning("Setup cancelled by user.")
            underline()
            time.sleep(1)
            clear(print_header=False)
            exit()