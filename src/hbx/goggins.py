from .toolbox import console, Panel, Text, center, choose, list_options, color, underline, warning, print_animated
from . import storage
from datetime import datetime
import random

GOGGINS_QUOTES = [
    "Stay hard!",
    "You are in danger of living a life so comfortable and soft, that you will die without ever realizing your true potential.",
    "Don't stop when you're tired. Stop when you're done.",
    "The only person who is going to turn your life around is you.",
    "Everything in life is a mind game!",
    "When you think that you are done, you're only 40% into what your body's capable of doing. That's just the limits that we put on ourselves.",
    "Life is one big tug of war between mediocrity and trying to find your best self.",
    "We're all great. No matter if you think you're dumb, fat, been bullied, we all have greatness. You gotta find the courage. It's going to be hard work, discipline, and the non-cognitive skills—hard work, self-dedication, slogging, sacrifice—will set you apart.",
    "It's so easy to be great nowadays, because everyone else is weak.",
    "If you want to get better, do the things that no one else wants to do.",
    "I don't think about yesterday. I think about today and getting better."
]

CANT_HURT_ME_MISSION = {
    "Mission": "Can't Hurt Me",
    "Objectives": [
        "Challenge 1: Face Your Bad Hand (Write down limiting factors)",
        "Challenge 2: Accountability Mirror (Post goals/insecurities)",
        "Challenge 3: Step Outside Your Comfort Zone (Do something uncomfortable)",
        "Challenge 4: Taking Souls (Outwork your 'opponent')",
        "Challenge 5: Visualization (Visualize success and obstacles)",
        "Challenge 6: Cookie Jar (Document your past wins)",
        "Challenge 7: The 40% Rule (Push past your mental limit)",
        "Challenge 8: Scheduling (The 24-Hour Mission)",
        "Challenge 9: Unusual Effort (Be uncommon amongst uncommon)",
        "Challenge 10: The Aftermath (Empowerment through failure/success)"
    ],
    "Current": 0,
    "Status": "Incomplete"
}

def menu():
    header = center("《 GOGGINS LAB 》", "—", style="bold red")
    console.print(header)

    quote = random.choice(GOGGINS_QUOTES)
    print_animated(f"\n[italic red]\"{quote}\"[/]\n", delay=0.01)

    options = {
        "Accountability Mirror": manage_accountability_mirror,
        "Cookie Jar": manage_cookie_jar,
        "Initialize 'Can't Hurt Me' Mission": init_goggins_mission
    }

    list_options(options)
    choose(options, src=menu)

def manage_accountability_mirror():
    header = center(" Accountability Mirror ", "—", style="bold magenta")
    console.print(header)

    data = storage.load_data(storage.GOGGINS_MIRROR)
    if data:
        content = ""
        for i, entry in enumerate(data):
            content += f"{i+1}. [bold cyan]{entry['Goal']}[/]: {entry['Truth']}\n"
        console.print(Panel(content, title="[bold magenta]Mirror Entries[/]", border_style="magenta"))

    print("\n1. Add Entry")
    print("2. Back")

    choice = input(color(">>> ", "magenta"))
    if choice == "1":
        goal = input(color("Goal/Insecurity: ", "cyan"))
        truth = input(color("The Hard Truth: ", "red"))
        if goal and truth:
            entry = {
                "Goal": goal,
                "Truth": truth,
                "Timestamp": datetime.now().isoformat()
            }
            storage.save_entry(storage.GOGGINS_MIRROR, entry)
            console.print("[green]Entry added to the Mirror.[/]")
        else:
            warning("Fields cannot be empty.")
        manage_accountability_mirror()

def manage_cookie_jar():
    header = center(" Cookie Jar ", "—", style="bold yellow")
    console.print(header)

    data = storage.load_data(storage.GOGGINS_COOKIE_JAR)
    if data:
        content = ""
        for i, entry in enumerate(data):
            content += f"🍪 [bold yellow]{entry['Win']}[/]: {entry['Detail']}\n"
        console.print(Panel(content, title="[bold yellow]Your Cookie Jar[/]", border_style="yellow"))

    print("\n1. Add a Win")
    print("2. Back")

    choice = input(color(">>> ", "magenta"))
    if choice == "1":
        win = input(color("What was the win? ", "yellow"))
        detail = input(color("Remind yourself how hard it was: ", "cyan"))
        if win and detail:
            entry = {
                "Win": win,
                "Detail": detail,
                "Timestamp": datetime.now().isoformat()
            }
            storage.save_entry(storage.GOGGINS_COOKIE_JAR, entry)
            console.print("[green]Cookie added to the Jar.[/]")
        else:
            warning("Fields cannot be empty.")
        manage_cookie_jar()

def init_goggins_mission():
    data = storage.load_data(storage.TASK_FILE)
    if any(m["Mission"] == "Can't Hurt Me" for m in data):
        console.print("[yellow]Can't Hurt Me mission is already initialized.[/]")
        return

    storage.save_entry(storage.TASK_FILE, CANT_HURT_ME_MISSION)
    console.print("[bold green]Can't Hurt Me mission initialized! STAY HARD![/]")
