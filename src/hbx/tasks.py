"""
Module for managing "missions" (goal/task progress 
tracking)
"""
from .toolbox import list_options, past, color, center
from .toolbox import warning, clear, underline, choose
from .toolbox import no_data, rated_bar, spacer
from .toolbox import wrap_text as wrap
from .toolbox import console, Panel, Text
from . import slight_edge
from . import storage

def menu():
    header = center("《 Mission Center 》", "—")
    print(f"\n{header}\n")
    
    from . import goggins
    options = {
        "Update mission progress": mission_log,
        "Create new mission": create_mission,
        "Initialize 'Can't Hurt Me' Mission": goggins.init_goggins_mission
    }
    list_options(options, "Choose action")
    choose(options, src=menu)

def mission_log():
    """
Allows user to update progress on a mission (task).
If all objectives in a mission are complete, it marks it as 'Complete'.
    """
    data = storage.load_data(storage.TASK_FILE)
    if not data:
        no_data("No missions found")
        underline()
        return
    
    header = center(" Updating Task! ", "—")
    print(f"\n{header}\n")
    
    missions = [m["Mission"] for m in data]        
    
    list_options(missions, "Update mission")    
    choice = choose(missions, 1, mission_log)
    if choice is None: return
        
    current = data[choice]["Current"]      
    try:
        objective = data[choice]["Objectives"][
                    current]
        objective = past(objective)
    except IndexError:
        for mission in data:
           if mission["Mission"] == missions[choice]:
               mission["Status"]  = "Complete"
               storage.save_task(data)
               return

    probe = input(f"\nHave you {objective}? [y/n]: "
            ).lower().strip()
    if probe == "clear":
        clear()
        mission_log()
    elif probe == "y":
        slight_edge.ballot(1)
        for mission in data:
            if mission["Mission"] == missions[choice]:
                mission["Current"] += 1
                storage.save_data(storage.TASK_FILE, 
                    data)                
    print()
    underline()
    
def create_mission():
    print()
    print(center(" Create New Mission ", "—"))

    while True:
        name = input(color("\nMission name: ", 
               "cyan")).strip()
        if name: break
        warning("Mission name cannot be empty.")

    objectives = []
    print(color("\nEnter mission objectives one by "
         +"one. Type 'done' when finished:\n", 
         "yellow"))
    
    while True:
        objective = input(color("Objective "
                  + f"{len(objectives)+1}: ", 
                    "green")).strip()
        if objective.lower() == "done":
            if not objectives:
                warning("At least one objective is "
                       +"required.")
                continue
            break
        elif not objective:
            warning("Objective cannot be empty.")
            continue
        objectives.append(objective)

    mission = {
        "Mission": name,
        "Objectives": objectives,
        "Current": 0,
        "Status": "Incomplete"
    }

    storage.save_entry(storage.TASK_FILE, mission)
    print("\n",center(" ✔ Mission Created! ", "—"))
    
def get_missions() -> list[dict]:
    """
Returns a list of mission summaries (progress, name, current objective).
    """
    data     = storage.load_data(storage.TASK_FILE)
    missions = []
    for mission in data:
        if mission["Status"] != "Complete":
            current = mission["Current"]
            rate = current/len(mission["Objectives"])
            obj  = mission["Objectives"][current]
            info = {
                "Name": mission["Mission"],
                "Progress": round(rate, 4),
                "Objective": obj
            }
            missions.append(info)
            
    return missions[:min(len(missions), 3)]

def render_mission_card(mission: dict, index: int):
    name      = mission["Name"]
    objective = mission["Objective"]
    rate      = mission["Progress"]
    bar       = rated_bar(rate)
    
    content = Text.assemble(
        (f"Mission {index+1}: ", "bold bright_cyan"), (f"{name}\n", "white"),
        (f"Objective: ", "bold cyan"), (f"{objective}\n\n", "white"),
        (f"REALIZATION RATE\n", "bold green"),
        (f"{bar}", "white")
    )

    console.print(Panel(content, border_style="green", expand=False))