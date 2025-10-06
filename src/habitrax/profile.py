from .toolbox import center, color, clear, underline
from .toolbox import generate_encryption, timetools
from .toolbox import warning, choose, list_options
from .toolbox import no_data, label, iter_print
from .toolbox import wrap_text
from datetime import datetime
from . import storage
import time

def menu():
    header = center(" 《 USER PROFILE 》 ", 1)
    print(f"\n{header}\n")
    
    options = {
        "View profile": show_profile,
        "Edit profile fields": edit_profile,
        "Edit commandments": edit_commandments,
        "Reset profile": reset_profile
    }

    list_options(options, "Choose action")
    choose(options, src=menu)

def show_profile():
    data = storage.load_data(storage.USER_FILE)
    if not data:
        no_data("No user data found")
        underline()
        return

    labels = label([
        "Name:", "Birthday:", 
        "Timezone:", "Chief Aim:"
    ])
    
    print(f"\n{labels[0]} {data.get('Name', 'N/A')}")
    bday = timetools.timestamp(data['Birthday'], 1)
    print(labels[1], bday)
    print(labels[2], data.get('Timezone', 'N/A'))
    print(f"{labels[3]}\n\n{wrap_text(data.get('Aim')) or 'N/A'}\n")

    if "Decalogue" in data:
        list_options(data["Decalogue"], 
            "Commandments", 1)

    underline()

def edit_profile():
    data = storage.load_data(storage.USER_FILE)
    
    fields = ["Name", "Birthday", "Timezone", "Aim"]
    field_names = {
        "Name": "Name",
        "Birthday": "Birthday (YYYY-MM-DD)",
        "Timezone": "Timezone (e.g. CAT)",
        "Aim": "Chief Aim"
    }

    print()
    while True:
        list_options(fields, "Which field do you want to edit?")
        print(f"{len(fields)+1}. Back")
        try:
            choice = int(input(color(">>> ", "magenta")))
            if choice == len(fields)+1:
                print()
                underline()
                break
            field = fields[choice - 1]
            
            print()
            while True:
                new_val = input(color(f"New value for {field_names[field].lower()}: ", "cyan")).strip()
                if choice == 2:
                    new_val = timetools.to_iso(new_val)
                    if new_val == None:
                        warning("Invalid format! Try again.")
                        continue
                break
            
            data[field] = new_val
            storage.save_data(storage.USER_FILE, data)
            footer = center(" Updated Successfully ", 1)
            print(f"\n{footer}\n")
        except (ValueError, IndexError):
            warning("Invalid choice! Try again.")

def edit_commandments():
    data = storage.load_data(storage.USER_FILE)
    
    options = [
        "New commandment list", 
        "Add to existing"
    ]
    
    print()
    list_options(options)
    choice = choose(options, 1, edit_commandments)
    if choice is None:
        return
    
    print(color("\nEnter new commandment(s). Type 'done' when finished:\n", "yellow"))
    
    new_decalogue = []
    if choice == 1:
        new_decalogue = data["Decalogue"]
        
    while True:
        cmd = input(color(f"Commandment {len(new_decalogue)+1}: ", "cyan")).strip()
        if cmd.lower() == "done":
            break
        new_decalogue.append(cmd)
    
    data["Decalogue"] = new_decalogue
    storage.save_data(storage.USER_FILE, data)
    footer = center(" Commandments Updated ", 1)
    print(f"\n{footer}")

def reset_profile():
    otp = generate_encryption()
    confirm = input(color(f"\nThis will erase your profile. Type {otp} to confirm\n>>> ", "red"))
    if confirm == otp:
        storage.save_data(storage.USER_FILE, {})
        time.sleep(1)
        print("\nReseting", end="")
        time.sleep(.5)
        iter_print(".", times=3, end="", delay=.75)
        time.sleep(.75)
        print()
        time.sleep(.5)
        footer = center(" Profile Reset ", 1)
        print(f"\n{footer}")        
    else:
        print("\n"+center(" Cancelled ", 1))
        