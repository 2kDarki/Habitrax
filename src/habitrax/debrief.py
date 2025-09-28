from .toolbox import choose_from, warning, no_data
from .toolbox import choose, center, underline
from .toolbox import timetools, label, color
from .toolbox import variables, list_options
from .slight_edge import ballot
from datetime import datetime
from time import time
from . import storage
from . import level
import random

def menu():
    header = center("《 Debrief 》", 1)
    print(f"\n{header}\n")
        
    options = {
        "Daily reflection": reflect,
        "Shadow work journal": shadow_journal,
        "Debrief review": debrief_review
    }
    
    list_options(options)
    choose(options, 0, menu)

def reflect():
    header = center(" Daily Reflection ")
    print(f"\n{color(header, fg='green')}")
    
    # Load the pool of questions from the JSON file
    data = storage.load_data(storage.QUESTIONS)

    start = time()
    
    # Flatten the questions into a single list with 
    # themes
    pool = []
    for theme, questions in data.items():
        for question in questions:
            pool.append({
                "question": question, 
                "theme": theme
            })

    count = random.randint(5, 10)
    selected = random.sample(pool, count)

    for n, item in enumerate(selected):
        print()
        print(f"Q{n+1}. {item['question']}")
        reply = input(color(">>> ", "magenta"))
        timestamp = datetime.now().isoformat()
        
        # Save each reflection as a separate entry
        reflection = {
            "Question": item["question"],
            "Answer": reply,
            "Theme": item["theme"],
            "Timestamp": timestamp,
            "Time": time()
        }        
        storage.save_entry(storage.REFLECTIONS, 
                           reflection)       
    
    end = time()
    
    duration = round((end - start) / 3600, 3)
    
    labels = label([
        "Focus level (1–10): ", 
        "Uncertainty in focus (±): "
    ])    
    focus, fuzziness = variables(labels)
    
    focus = max(0, min(focus, 10))
    fuzziness = max(0, min(fuzziness, 10))

    q_min = max(0, (focus - fuzziness) * duration)
    q_max = round((focus + fuzziness) * duration, 2)

    session = {
        "Timestamp": datetime.now().isoformat(),
        "Task": "Daily reflection session",
        "Category": "Reflection",
        "Focus": focus,
        "Fuzziness": fuzziness,
        "Time spent": duration,
        "Quality range": [round(q_min, 2), q_max]
    }
    
    storage.save_entry(storage.DATA_FILE, session)
    
    ballot(1)
    level.Stat("Reflection").level_up()
    print()
    footer = center(" ✔ Reflection Logged Successfuly! ", 1)
    print(f"{footer}")

def shadow_journal():
    header = center(" Shadow Work Journal ")
    print(f"\n{color(header, fg='green')}")
    prompt = color('>>> ', 'magenta')
    
    start = time()
    
    entry = {
        "Trigger Event": input(f"\nWhat happened?\n{prompt}"),
        "Emotional Response": input(f"\nWhat did you feel?\n{prompt}"),
        "Reaction": input(f"\nHow did you react externally (words, body language, tone)?\n{prompt}"),
        "Deeper Truth": input(f"\nWhy did it affect you so strongly?\n{prompt}"),
        "Past Echo": input(f"\nDoes this remind you of anything from your past?\n{prompt}"),
        "Core Belief": input(f"\nWhat belief about yourself or others was exposed?\n{prompt}"),
        "Need": input(f"\nWhat did you need in that moment but didn’t get?\n{prompt}"),
        "Reframe": input(f"\nHow can you view this situation differently now?\n{prompt}"),
        "Next Time": input(f"\nHow do you want to handle similar moments going forward?\n{prompt}"),
        "Timestamp": datetime.now().isoformat(),
        "Time": time()
    }    
    end = time()
    duration = round((end - start) / 3600, 3)
    
    labels = label([
        "Focus level (1–10): ", 
        "Uncertainty in focus (±): "
    ])
    
    focus, fuzziness = variables(labels)
    
    focus = max(0, min(focus, 10))
    fuzziness = max(0, min(fuzziness, 10))

    q_min = max(0, (focus - fuzziness) * duration)
    q_max = round((focus + fuzziness) * duration, 2)

    session = {
        "Timestamp": datetime.now().isoformat(),
        "Task": "Shadow work",
        "Category": "Reflection",
        "Focus": focus,
        "Fuzziness": fuzziness,
        "Time spent": duration,
        "Quality range": [round(q_min, 2), q_max]
    }
    
    storage.save_entry(storage.JOURNAL, entry)
    storage.save_entry(storage.DATA_FILE, session)
    ballot(1)
    level.Stat("Reflection").level_up()
    footer = center(" ✔ Journal Entry Logged Successfully ", 1)
    print("\n"+footer)

def debrief_review(proxy=False):
    """
Opens the Debrief Review menu.
If proxy=True, it means this was called from another module, so we skip the theme filter to avoid unnecessary nesting.
    """
    if not proxy:
        header = center(' Debrief Review ')
        print(f"\n{color(header, 'green')}\n")
    
    options = {
        "View all entries": view_all_entries,
        "Filter by theme": filter_by_theme,
        "Filter by date": filter_by_date,
        "Search by keyword": search_keyword
    }
    
    if proxy:
        options = {
            "View all entries": view_all_entries,
            "Filter by date": filter_by_date,
            "Search by keyword": search_keyword
        }
            
    list_options(options)
    
    if proxy:
        choose(options, 0, debrief_review, 1)
    else:
        choose(options, 0, debrief_review)
    print()
    underline()

def choose_journal_type():
    """
Prompts the user to choose between viewing Reflections or Shadow Journal entries.
Returns:
 - A string indicating the type ('reflections' or 'shadow')
 - The corresponding loaded data
    """
    print()
    types = ["Reflections", "Shadow Journal"]
    list_options(types, "Choose entry type")
    choice = input(color(">>> ", "magenta")).strip()
    if choice == "1":
        return "reflections", storage.load_data(storage.REFLECTIONS)
    elif choice == "2":
        return "shadow", storage.load_data(storage.JOURNAL)
    else:
        warning("Invalid choice.")
        return None, []

def view_all_entries(proxy=False):
    """
Displays all entries from either reflections or shadow journals.
If proxy=True, it's being called internally (e.g. from another filter), so it skips the journal type selection.
    """
    entries = storage.load_data(storage.SERVICES)
    if not proxy:
        kind, entries = choose_journal_type()
    if not entries:
        no_data("No entries found.")
        return
    
    if not proxy:
        print_entries(entries, kind)
    else:
        print_entries(entries)

def filter_by_theme():
    """
Allows user to filter reflection entries by their associated theme.
Only applies to reflection-type journals (not shadow work).
    """
    kind, entries = choose_journal_type()
    if not entries:
        no_data("No entries found.")
        return

    themes = list({e["Theme"] for e in entries})
    if not themes:
        no_data("No themes found.")
        return

    print()
    list_options(themes, "Choose theme")
    
    try:
        index = int(input(color(">>> ", 'magenta'))) - 1
        if 0 <= index < len(themes):
            selected = [e for e in entries if e["Theme"] == themes[index]]
            print_entries(selected, kind)
        else:
            warning("Invalid choice.")
    except ValueError:
        warning("Invalid input.")

def filter_by_date(proxy=False):
    """
Filters journal entries based on a given date.
If proxy=True, the function is being called internally, so it skips journal type selection.
    """
    print()
    entries = storage.load_data(storage.SERVICES)
    
    if not proxy:
        kind, entries = choose_journal_type()
    if not entries:        
        no_data("No entries found.")
        return

    date_input = input("\nEnter date (YYYY-MM-DD): ").strip()
    selected = [e for e in entries if e["Timestamp"].startswith(date_input)]
    if not selected:
        no_data("No entries found for that date.")
    else:
        if not proxy:
            print_entries(selected, kind)
            return
        print_entries(selected)

def search_keyword(proxy=False):
    """
Searches journal entries for a user-specified keyword.
If proxy=True, the function is being called internally, so it handles data differently.
    """
    print()
    entries = storage.load_data(storage.SERVICES)
    if not proxy:
        kind, entries = choose_journal_type()
    if not entries:        
        no_data("No entries found.")
        return

    prompt = color("Enter keyword to search:", "cyan")
    keyword = input(f"\n{prompt} ").lower()
    
    # Match logic varies based on type and proxy 
    # status
    def match(entry):
        if kind == "reflections":
            return keyword in entry["Answer"].lower() or keyword in entry["Question"].lower()
        elif proxy:
            return keyword in entry["Entry"]["Subject"].lower() or keyword in entry["Entry"]["Service"].lower()
        else:
            return any(keyword in str(v).lower() for k, v in entry.items() if isinstance(v, str))
    
    selected = [e for e in entries if match(e)]
    if not selected:
        no_data("No results found.")
    else:
        if not proxy:
            print_entries(selected, kind)
            return
        print_entries(selected)

def print_entries(entries, kind=None):
    """
Prints journal entries in a readable format based on entry type.
 - kind='reflections': Shows Q&A with theme
 - kind='shadow': Shows shadow work prompts
 - kind=None: Shows service log style entries (used in soul_work.py)
    """
    for e in entries:
        print()
        print()
        stamp = timetools.timestamp(e['Timestamp'])
        ago = timetools.get_time_diff(
            time(), e['Time']
        )
        labels = label([
            "Date:", "Theme:", "Q:", "A:", 
            "Rendered to:", "Service:"
        ])
        print(labels[0], stamp)
        if kind == "reflections":
            print(labels[1], e["Theme"])
            print(labels[2], e["Question"])
            print(labels[3], e["Answer"])
        elif not kind:
            print(labels[4], e["Entry"]["Subject"])
            print(labels[5], e["Entry"]["Service"])
        else:
            for k, tag in {
                "Trigger Event": "Trigger",
                "Emotional Response": "Emotion",
                "Reaction": "Reaction",
                "Deeper Truth": "Truth",
                "Past Echo": "Past",
                "Core Belief": "Belief",
                "Need": "Need",
                "Reframe": "Reframe",
                "Next Time": "Next"
            }.items():
                print(color(f"{tag}:", "cyan"), 
                    e.get(k, "")
                )
        print(color("Logged:", "cyan"), ago)
    
if __name__ == "__main__":    
    menu()