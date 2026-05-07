"""
Entry point of the Questline CLI application (Habitrax)
Displays the main menu and routes to each core module
"""
from .toolbox import warning, choose_from, list_options, choose
from .toolbox import center, color, clear, underline
from .toolbox import console, Panel, print_animated
from . import status_window
from . import soul_work
from . import notebook
from . import debrief
from . import profile
from . import config
from . import logger
from . import setup
from . import stats
from . import tasks
from . import goggins

def main():
    header = center("《 QUESTLINE 》", line="=", style="bold green")
    print_animated(header, delay=0.005)
    
    options = {       
               "Log session": logger.log_session  ,
            "Mission center": tasks.menu          ,
                   "Debrief": debrief.menu        ,
                 "Soul work": soul_work.menu      ,
     "Goggins Accountability": goggins.menu        ,
        "View Status Window": status_window.window,
                "Statistics": stats.menu          ,        
                  "Notebook": notebook.menu       ,
                   "Profile": profile.menu        ,
                  "Settings": config.menu,
                   "Exit": lambda: clear(terminate=True)
    }
    while True:
        print()
        # Use Rich Panel for the menu
        menu_text = ""
        for i, opt in enumerate(options):
            style = "cyan" if opt != "Exit" else "red"
            menu_text += f"[bold magenta]{i+1}.[/] [{style}]{opt}[/]\n"

        console.print(Panel(menu_text.strip(), title="[bold green]Main Menu[/]", border_style="green"))
        
        choose(options, src=main)