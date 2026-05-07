from .toolbox import timetools, color, console, Panel, Text
from rich.table import Table
from rich.columns import Columns
from . import soul_work
from . import storage
from . import toolbox
from . import level
from . import tasks


def window(from_term: bool = False):
    header = toolbox.center("《 STATUS 》", "—", style="bold green")
    console.print(header)

    user     = storage.load_data(storage.USER_FILE)
    birthday = user.get("Birthday")
    age      = "Unknown"
    if birthday: age = timetools.get_age(birthday)

    stat        = level.Stat()
    lvl, blocks = stat.get_stat_blocks()
    rank        = stat.get_rank(lvl)
    title       = stat.get_title(rank)
    name        = user.get("Name") or "Unknown"
    money       = soul_work.coffer(getter=True)

    user_info = Text.assemble(
        (f"Name:  ", "bold cyan"), (f"{name}\n", "white"),
        (f"Age:   ", "bold cyan"), (f"{age}\n", "white"),
        (f"Level: ", "bold cyan"), (f"{lvl}\n", "white"),
        (f"Rank:  ", "bold cyan"), (f"{rank}\n", "white"),
        (f"Title: ", "bold cyan"), (f"{title}\n", "white"),
        (f"Money: ", "bold cyan"), (f"${money:.2f}", "white")
    )

    console.print(Panel(user_info, title="[bold green]Profile[/]", border_style="cyan", expand=False))

    if not blocks:
        toolbox.no_data("No stats available yet")
        toolbox.underline()
        if from_term: print()
        return

    stat_table = Table(title="[bold green]Attributes[/]", show_header=True, header_style="bold magenta", border_style="cyan")
    stat_table.add_column("Stat", style="cyan")
    stat_table.add_column("Lvl", justify="right", style="white")
    stat_table.add_column("Progress", style="green")
    stat_table.add_column("Rank", justify="center", style="bold yellow")

    for block in blocks:
        stat_table.add_row(
            block['Short'],
            str(block['Weight']),
            block['Bar'],
            block['Rank']
        )

    console.print(stat_table)

    missions = tasks.get_missions()
    if not missions:
        toolbox.underline()
        return

    toolbox.spacer(1)
    console.print(toolbox.center("《 MISSIONS 》", style="bold green"))

    for index, mission in enumerate(missions):
        tasks.render_mission_card(mission, index)

    toolbox.underline()
    if from_term: print()
