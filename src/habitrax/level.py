from datetime import datetime as dt
from . import toolbox as tb
from . import stat_logic
from . import storage
import time

MAX_LEVEL = 1000

class Stat:
    def __init__(self, name=None):
        if not name:
            return
        self.name = name
        self.exp = tb.get_exp(name)
        self.level = int(self.exp / 10)
        self.rank = self.get_rank(self.level)
        self.title = self.get_title(self.rank)
        self.prv_lvl = self.get_level()

    def level_up(self):
        level_data = storage.load_data(storage.LEVEL_FILE)
        if not level_data:
            level_data = []

        found = False
        for entry in level_data[1:]:
            if entry["Category"] == self.name:
                found = True
                new_level = self.level
                if new_level > entry["Level"] and new_level < MAX_LEVEL:
                    entry["Level"] = new_level
                    entry["Timestamp"] = dt.now().isoformat()
                    entry["Time"] = time.time()
                    print(f"\nStat level up!\n\nYour {self.name.lower()} is now level {new_level}!")
                elif new_level >= MAX_LEVEL:
                    entry["Level"] = new_level
                    entry["Timestamp"] = dt.now().isoformat()
                    entry["Time"] = time.time()
                    print(f"\nCongratulations!\n\nYour {self.name.lower()} has reached max level!")
                break

        if not found:
            level_data.append({
                "Category": self.name,
                "Level": self.level,
                "Timestamp": dt.now().isoformat(),
                "Time": time.time()
            })
            print(f"\nNew category '{self.name}' added at level {self.level}.")
        
        storage.save_data(storage.LEVEL_FILE, 
            level_data)
        
        new_lvl = self.get_stat_blocks()[0]
        if self.prv_lvl < new_lvl:
            print(f"\nLevel up!\n\nYou are now level {new_lvl}!")
            level_data[0]["Level"] = new_lvl
        elif self.prv_lvl > new_lvl:
            print(f"\nLevel re-adjustment!\n\nLevel re-adjusted to {new_lvl} from {self.prv_lvl}")
        storage.save_data(storage.LEVEL_FILE, 
            level_data)

    @staticmethod
    def get_rank(level):
        # F-rank block
        if level < 10: return "FFF"
        if level < 50: return "FF"
        if level < 100: return "F"

        # Tiered ranks
        tiers = [
            ("E", 100), ("D", 200), 
            ("C", 300), ("B", 400)
        ]
        for rank, base in tiers:
            if base <= level < base + 10: return rank
            if base + 10 <= level < base + 50: return rank * 2
            if base + 50 <= level < base + 100: return rank * 3
        # A-rank block
        if 500 <= level < 520: return "A"
        if 520 <= level < 600: return "AA"
        if 600 <= level < 700: return "AAA"

        # S-rank block
        if 700 <= level < 800: return "S"
        if 800 <= level < 900: return "SS"
        if 900 <= level < 1000: return "SSS"

        return "Z"

    @staticmethod
    def get_title(rank):
        titles = {
            "FFF": "Trashiest of Trash",
             "FF": "Wandering Newbie",
              "F": "Curious Fledgling",
              "E": "Focused Novice",         
             "EE": "Intentional Amateur", 
            "EEE": "Consistency Embodiment",            
              "D": "System Crafter",
             "DD": "Growth Enthusiast",
            "DDD": "Structured Mind",
              "C": "Studious Operator",
             "CC": "Tactical Executor",
            "CCC": "Deep Worker",
              "B": "Workflow Architect",
             "BB": "Self-Mastery Adept",
            "BBB": "Mental Mechanic",
              "A": "Focused Virtuoso",
             "AA": "Meta-Thinker",
            "AAA": "Multi-domain Achiever",
              "S": "Discipline Demi-God",
             "SS": "Flow Incarnate",
            "SSS": "Realm Architect",
              "Z": "Transcendental"
        }
        return titles.get(rank)
        
    @staticmethod
    def get_level():
        data = storage.load_data(storage.LEVEL_FILE)
        if not data:
            data = [{
                "Level": 0,
                "Timestamp": dt.now().isoformat(),
                "Time": time.time()
            }]
        if len(data[0]) != 3:
            data.insert(0, {
                "Level": 0,
                "Timestamp": dt.now().isoformat(),
                "Time": time.time()
            }) 
        storage.save_data(storage.LEVEL_FILE, data)
        return data[0]["Level"]

    def get_stat_blocks(self):
        resolved = stat_logic.get_resolved_stats()
        blocks = []

        total_exp = 0
        for index, (name, stats) in enumerate(resolved.items()):
            group_exp = sum(tb.get_exp(stat) for stat in stats)
            total_exp += group_exp        
            level = min(int(group_exp / 10), 1000)
            weigh = level if level != 1000 else "MAX"
            weight = tb.number_padding(weigh)
            bar = tb.var_per_cat(1, [level, group_exp])[0]
            short = name[:3] if name[:3] != "Ope" else "Ops"
            rank = self .get_rank(level)

            blocks.append({
                "Short": short,
                "Rank": rank,
                "Weight": weight,
                "Bar": bar,
                "Index": index
            })
    
        total = len(resolved)
        level = min(int(total_exp / 10 / total), 1000) if total else 0

        return level, blocks