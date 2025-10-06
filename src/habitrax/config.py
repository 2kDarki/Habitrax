from .toolbox import center, choose, list_options
from . import stat_logic
from . import metadata

def menu():
    header = center("《 Settings 》", 1)
    print(f"\n{header}\n")
    
    options = {
        "Stats": stat_logic.menu,
        "About": metadata.menu
    }
    
    list_options(options)
    choose(options, src=menu)