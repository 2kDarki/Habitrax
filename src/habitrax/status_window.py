from .toolbox import timetools, color, number_padding
from . import soul_work
from . import storage
from . import toolbox
from . import level
from . import tasks

def window():
    header = toolbox.center("《 STATUS 》", 1)
    print(f"\n{header}")
    
    user = storage.load_data(storage.USER_FILE)
    
    birthday = user.get("Birthday")
    age = "Unknown"
    if birthday:
        age = timetools.get_age(birthday)
    
    lvl, blocks = level.Stat().get_stat_blocks()
    rank = level.Stat().get_rank(lvl)
    title = level.Stat().get_title(rank)
    name = user.get("Name") or "Unknown"
    money = soul_work.coffer(1)
    
    print()
    print()
    print(f" {color('Name:', 'cyan')} {name}")
    print(f"  {color('Age:', 'cyan')} {age}")
    print(f"{color('Level:', 'cyan')} {lvl}")
    print(f"{color('Title:', 'cyan')} {title}")
    print(f"{color('Money:', 'cyan')} ${money:.2f}")
    
    if not blocks:
        toolbox.no_data("No stats available yet")
        toolbox.underline()
        return
    
    print()
    print()        
    for block in blocks:
        stat = f"{color(block['Short'], 'cyan')}  {block['Weight']}   {block['Bar']}   {block['Rank']}"
        print(toolbox.center(stat, fixed=True))
        print()
    
    missions = tasks.get_missions()
    if not missions:
        toolbox.underline()
        return
    
    print()
    print()        
    MISSIONS = toolbox.center("《 MISSIONS 》")
    print(color(MISSIONS, "green"))
    print()
    for opt, mission in enumerate(missions):
        name = mission["Name"]
        objective = mission["Objective"]
        rate = mission["Progress"]
        bar = toolbox.rated_bar(rate)
        rated_bar = toolbox.center(f'{bar[1]}')
        pad = toolbox.center(f'{bar[1]}', get=1)[0]
        print()
        print()
        print(f"{color(f'Mission {opt+1}:', 'lightcyan')} {name}")
        print(f"{color(f'Objective:', 'cyan')} {objective}")
        print()
        RATE = toolbox.center("  REALIZATION ")
        print(f"{RATE}")
        print(" " * pad + bar[0])
        print(f"{rated_bar}")
        print()
        print()
    
    toolbox.underline()

if __name__ == "__main__":
    window()