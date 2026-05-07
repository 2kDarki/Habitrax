from .toolbox import center, choose, list_options, color, console, Panel
from . import stat_logic
from . import about
from . import storage

def menu():
    header = center("《 Settings 》", line="—", style="bold green")
    console.print(header)
    
    options = {
        "Stats": stat_logic.menu,
        "AI Accountability": ai_config_menu,
        "About": about.menu
    }
    
    list_options(options)
    choose(options, src=menu)

def ai_config_menu():
    header = center(" AI Accountability Settings ", "—", style="bold yellow")
    console.print(header)

    config = storage.load_data(storage.AI_CONFIG)
    if not isinstance(config, dict):
        config = {"provider": "None", "api_key": ""}

    current_provider = config.get("provider", "None")
    console.print(f"Current Provider: [bold green]{current_provider}[/]")

    options = {
        "Choose Provider": lambda: set_provider(config),
        "Set API Key": lambda: set_api_key(config),
        "Back": menu
    }

    list_options(options)
    choose(options, src=ai_config_menu)

def set_provider(config):
    providers = ["OpenAI", "Anthropic", "OpenRouter"]
    list_options(providers, "Select Provider")
    choice = input(color(">>> ", "magenta")).strip()

    if choice in ["1", "2", "3"]:
        config["provider"] = providers[int(choice)-1]
        storage.save_data(storage.AI_CONFIG, config)
        console.print(f"[green]Provider set to {config['provider']}[/]")
    else:
        console.print("[red]Invalid choice.[/]")
    ai_config_menu()

def set_api_key(config):
    key = input(color("Enter API Key: ", "yellow")).strip()
    if key:
        config["api_key"] = key
        storage.save_data(storage.AI_CONFIG, config)
        console.print("[green]API Key saved.[/]")
    else:
        console.print("[red]Key cannot be empty.[/]")
    ai_config_menu()