"""
Logs work sessions, calculates quality ranges,
and updates user progress (leveling, trajectory)
"""
from datetime import datetime
from . import slight_edge
from . import toolbox
from . import storage
from . import level
    
def log_session():
    """
Logs a single work session with required metadata:
 - Task description: Describe what you were doing
 - Category: What were you doing? Reading? Studying?
 - Focus level (1–10): Focus level or workout intensity 
 - Fuzziness/Uncertainty (±): How much did focus/intensity flactuate or how unsure are you of the rating you gave 
 - Time spent: How long the session took (in hours)
Then calculates the quality range and stores all this in a JSON entry.
    """
    header = toolbox.center("《 New Session Log 》", 1)
    print(f"\n{header}\n")
    
    var = []
    
    labels = toolbox.label([
        "Task description: ", 
        "Category: ", 
        "Focus level (1–10): ", 
        "Uncertainty in focus (±): ", 
        "Time spent (in hours): "
    ])
    
    for pos, label in enumerate(labels):
        while True:
            try:
                variable = input(label)
                if pos < 2:
                    if variable == "clear":
                        toolbox.clear()
                        log_session()
                    break
                elif pos > 1 and float(variable) >= 0:
                    variable = float(variable)
                    break
            except ValueError:
                if variable == "clear":
                    toolbox.clear()
                    log_session()
            toolbox.warning("Invalid input. Please enter numbers where required.")    
        var.append(variable)

    task, category, focus, fuzziness, time_spent = var

    focus = max(0, min(focus, 10))
    fuzziness = max(0, min(fuzziness, 2))

    # Calculate quality range
    q_min = max(0, (focus - fuzziness) * time_spent)
    q_max = round((focus + fuzziness) * time_spent, 2)

    session = {
        "Timestamp": datetime.now().isoformat(),
        "Task": task,
        "Category": category,
        "Focus": focus,
        "Fuzziness": fuzziness,
        "Time spent": time_spent,
        "Quality range": [round(q_min, 2), q_max]
    }

    storage.save_entry(storage.DATA_FILE, session)
    slight_edge.ballot(1)
    level.Stat(category).level_up()
    footer = toolbox.center(" ✔ Session Logged Successfuly! ", 1)
    print(f"\n{footer}")

if __name__ == "__main__":
    log_session()