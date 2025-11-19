from datetime import timedelta as td
from datetime import datetime as dt
from math import floor, ceil, sqrt
from . import storage
import calendar as cl
import unicodedata
import textwrap
import shutil
import random
import time
import sys
import os
import re

def lvl_up_msg(cat):
    msg, cap = "", ""
    tense = [["are", "is"], ["have", "has"]]
    for i, [f, s] in zip([0, 1], tense):
        text = f"skills {f}" if (cat.endswith("ion")
            or cat.endswith("ing")) else s
        if i == 0: msg += text
        else     : cap += text
    return msg, cap

def ExitError(): return (KeyboardInterrupt, EOFError)

def print_help(at: int = 0, option: str | None = None):
    print()
    if option: print(f"Invalid option: {option!r}\n")
    if not at: 
        print("        Task: use -t or --task")
        print("  Reflection: use -r or --reflect")
        print("Shadow entry: use -s or --shadow")
    elif at == 1:
        print("  Reflections: use -d or --debrief")
        print("Status window: use -w or --status")
        print("   Statistics: use -s or --stats")
        print("      Balance: use -b or --balance")
        print(" Transactions: use -t or --transactions")
    else:
        print(" Deposit: use -d or --deposit ")
        print("Withdraw: use -w or --withdraw")
    print()

def help_msg(found: bool = False):
    args = {
        "log": ["-t", "--task", "-r", "--reflect", "-s", 
               "--shadow"],
        "view": ["-d", "--debrief", "-w", "--status", "-s", 
                "--stats", "-b", "--balance", "-t",
                "--transactions"],
        "coffer": ["-d", "--deposit", "-w", "--withdraw"]
    }
    header   = center("《 HABITRAX HELP 》", line="—")
    h        = ["-h", "--h","-help", "--help"]
    commands = ["log", "view", "coffer"]
    if len(sys.argv) == 2:
        if sys.argv[1] in commands: return
    elif len(sys.argv) > 2:
        for i, command in enumerate(commands):
            if command == sys.argv[1]:
                arg = sys.argv[2]
                if arg in args[command]: return
                print(f"\n{header}")
                print_help(i, None if arg in h else arg)
                underline()
                print()
                exit()
    
    for arg in h:
        if arg in sys.argv: found = True
    if not found: return
    
    print(f"\n{header}\n")
    print("Usage:")
    print("      habitrax")
    print("      habitrax command option\n")
    print("Commands:")
    print("      log                Log an activity")
    print("      view               View information")
    print("      coffer             Personal bank\n")
    print("Options:\n")
    
    for i, command in enumerate(commands):
        print(f"for command {command!r}:", end="")
        print_help(i)
        
    underline()
    print()
    exit()

def main_menu():
    print(end="\n\n")
    underline()

def spacer(times: int):
    for _ in range(times): print()

def iter_print(text, times: int, end: str = "\n", 
               delay: int | float = 0):
    for _ in range(times):
        time.sleep(delay)
        print(text, end=end, flush=True)

def generate_otp() -> str:
    number = random.randint(0, 999)
    return str(format_int(number, deno=3))

def wrap_text(text, indent: int = 0, pad: int = 0,
             inline: bool = False, 
             list_order: str = '') -> str:
    width = shutil.get_terminal_size().columns or 80
    styled_words = text.split()
    
    # Adjust margin based on length of list_order
    # List_order is a tag for an ordered list (e.g.,
    # 1., a., IV., 10. etc)
    length   = len(list_order) if inline else 0
    trailing = length / (10**len(str(length))
               ) if not inline else 0
    edge     = 1 + trailing
    if length > 9 and not inline:
        trailing = length * 2 / 10
    margin = 1 + trailing if length > 9 else edge
    
    # Insert line breaks
    line_len = len(list_order)
    result   = list_order if not inline else ""
    if pad:
        result   = " " * (pad-1)
        line_len = pad
    for i, word in enumerate(styled_words):
        used = line_len + visual_width(word)
        if used + margin > width:
            result += '\n' + ' ' * indent + word
            line_len = indent + visual_width(word)
        else:
            result += (' ' if result else '') + word
            line_len += visual_width(word) + (margin
                    ) / (2 if margin >= 2 else 1)
    
    return result
    
def money(*args) -> list[str]:
    formatted = []
    for amount in args:
        denomination = len(str(int(amount))) - 1
        formats = [
            f"  {amount:.2f} ",
            f" {amount:.2f} ",
            f"{amount:.2f} ",
            f"  {amount/1e3:.2f}K",
            f" {amount/1e3:.2f}K",
            f"{amount/1e3:.2f}K",
            f"  {amount/1e6:.2f}M",
            f" {amount/1e6:.2f}M",
            f"{amount/1e6:.2f}M"
            f"  {amount/1e9:.2f}B",
            f" {amount/1e9:.2f}B",
            f"{amount/1e9:.2f}B"
        ]
        try: formatted.append(formats[denomination])
        except IndexError: formatted.append("Really?")
    return formatted

def variables(labels: list) -> list[str]:
    print()
    varz = []
    while True:
        try:
            var = int(input(labels[len(varz)]))
            if len(varz) == 0 and 1 <= var <= 10:
                varz.append(var)
                continue
            elif len(varz) == 1 and 0 <= var <= 2:
                varz.append(var)
                break
        except Exception as e:
            if isinstance(e, ExitError()):
                if not isinstance(e, EOFError):print()
                main_menu()
                return
                
        if len(varz) == 0:
           warning("Enter a number between 1 and 10.")
        else: warning("Enter a number between 0 and 2.")
    return varz

def choose(options: list | dict, check: bool = False, 
           src=None, proxy: bool = False):
    """
Custom input menu for choosing an option from a list.
If check=True, returns index.
If proxy=True, passes (proxy=True) to chosen function.
If user inputs 'clear', resets the source screen.
    """
    print(f"{format_int(len(options)+1, form=' ')}. Back")
    while True:
        try:
            choice = input(color(">>> ", "magenta"))
            choice = int(choice) - 1
            if 0 <= choice < len(options):
                if check: return choice
                elif proxy:
                    choose_from(options, choice)(1)
                else: choose_from(options, choice)()
                break
        except Exception as e:
           if isinstance(e, ExitError()): 
                if isinstance(e, EOFError): print()
                main_menu()
                return                
           if choice == "clear" and src:
                if proxy:
                    clear()
                    src(1)
                    return
                clear()
                src()
                return
        if choice == len(options):
            if src:
                print()
                underline()
            return
        warning("Choose a number between 1 and "
               +f"{len(options)+1}.")

def past(string: str) -> str:
    past = string.split()[0].lower()
    if past.endswith("y"):
        past = past.replace("y", "ied")
    elif past.endswith("r"): past += "ed"
    rest = string.split()[1:]
    return f"{past} {' '.join(rest)}"

def choose_from(dictionary: dict, index: str | int):
    """
Takes a dictionary and a numeric index
Returns the corresponding value
    """
    return next((dictionary[opt] for pos, opt in 
        enumerate(dictionary) if pos == int(index)))

def list_options(options: list|dict|None = None, 
        guide: str | None = None, spaced: bool = False):
    """
Displays all keys in a dictionary or values in a list as
a numbered list.
 -  guide: Optional header for the options
 - spaced: Adds empty lines between options
    """
    if guide: print(color(guide, underule=1)+":")
    if options is None: return
    for opt, option in enumerate(options):
        order = format_int(opt+1, form=" ")
        print(wrap_text(option, 4, list_order=f"{order}."))
        if spaced: print()

def label(iterable: list | dict) -> list[str]:
    return [color(head, "cyan") for head in iterable]

def no_data(message: str):
    print(f"\n{color(center(message), 'gray')}\n")

def warning(message:str, inline:bool=False) -> str|None:
    if inline: return color(message, "red")
    print(f"\n{color(message, 'red')}\n")
    
def clear(print_header:bool=True, terminate:bool=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    if terminate: exit()
    header = center("《 QUESTLINE 》", line="=")
    if print_header: print(header)

def color(text,fg: str|None = None, bg: str|None = None,
          bold:bool = False, underule:bool = False) -> str:
    colors = {
        "black": 30, "red": 31, "green": 32, 
        "yellow": 33, "blue": 34, "magenta": 35,
        "cyan": 36, "white": 37,
        "gray": 90, "lightred": 91, "lightgreen": 92,
        "lightyellow": 93, "purple": 94,
        "lightmagenta": 95, "lightcyan": 96
    }

    styles = []
    
    if bold: styles.append("1")
    if underule: styles.append("4")
    if fg in colors: styles.append(str(colors[fg]))
    if bg in colors: styles.append(str(colors[bg]+10))

    if styles: return (f"\033[{';'.join(styles)}m{text}"
               +"\033[0m")
    return text    
 
def number_padding(num: int, pad: int = 3) -> str:
    return str(num).rjust(pad)
        
def visual_width(s: str) -> int:
    clean = strip_ansi(s)
    width = 0
    for ch in clean:
        if unicodedata.east_asian_width(ch) in ['F', 'W']: 
            width += 2
        else: width += 1
    return width

def center(text: str, line: str | None = None, 
           get: bool = False, fixed: int | None = None):
    term_width = shutil.get_terminal_size((80, 
        20)).columns
    display_len = visual_width(text)
    
    # Centers stats in status window
    if fixed: display_len = fixed
    total_pad = max(term_width - display_len, 0)
    left_pad = total_pad // 2
        
    # magic number 56 used to fix termux centering
    # alignement
    left_pad -= 1 if any(char in text for char in 
        ("█", "▒")) and "%" in text and (term_width 
        < 56) else 0
    right_pad = total_pad - left_pad
    if get: return left_pad, total_pad, right_pad

    if line:
        line_color = "magenta" if line == "—" else "green"
        text_color = "magenta" if line != "—" else "green"
        left   = color(line *  left_pad, line_color)   
        right  = color(line * right_pad, line_color)
        middle = color(text, fg=text_color)
        return f"{left}{middle}{right}"
        
    return " " * left_pad + text

def strip_ansi(s: str) -> str:
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)

def underline():
    term_width = shutil.get_terminal_size((80, 20)).columns
    print(color("—"*term_width, "magenta")) 
    
def make_progress_bar(pct:float, width:int = 20) -> str:
    filled = int(pct * width)
    return "█" * filled + "▒" * (width - filled)

def rated_bar(pct: float, width: int = 20) -> str:
    control = int(pct * width)
    filled = min(int(pct * width), 7)
    first = "█" * filled + "▒" * (7 - filled)
    rate = format_int(f"{(pct * 100):.2f}")
    last = "▒" * 7
    if pct > 0.6:
        pct -= 0.6
        filled = min(int(pct * width), 7)
        last = "█" * filled + "▒" * (7 - filled)
        
    return f"{first}{rate}%{last}"

def pluralize(n: int, word: str) -> str:
    if n == 1: return word
    else: return word + 's'
        
def variance(new: int | float | None, 
             old: int | float | None) -> int | float:
    if old: return ((new - old) / old) * 100
    elif not new and not old: return 0
    return 100

def format_int(number, deno: int = 2, form: str = "0"):
    length = len(str(int(float(number))))
    if length < deno:
        fill = (deno - length) * form
        number = f"{fill}{number}"
    return number
    
def format_number(*args) -> list[str]:
    return [str(n).zfill(2) for n in args]

def get_exp(category: str) -> float:
    data = storage.load_data(storage.DATA_FILE)
    
    exp = 0
    for entry in data:
        if entry["Category"] == category:
            exp += entry["Time spent"]

    return exp
    
def var_per_cat(index: int | None = None, 
             grouped: list | None = None):
    data     = storage.load_data(storage.LEVEL_FILE)
    entry    = data[index]
    now      = time.time()
    last     = entry["Time"]
    lapsed   = timetools.get_time_diff(now, last)
    date     = timetools.timestamp(entry["Timestamp"])
    level    = entry["Level"] * 10
    try: exp = get_exp(entry["Category"])
    except KeyError: return None
    if grouped:
        level, exp = grouped
        level *= 10
    progress = exp - level
    exp_pc   = (progress/10) * 100 if level < 1000 else 100
    bar      = make_progress_bar(exp_pc / 100)
    return bar, date, lapsed, exp_pc

def percent_colored(progress: int | float) -> str:
    sign = "+" if progress >= 0 else ""
    hue  = "green" if progress >= 0 else "red"
    return color(f"{sign}{progress:.2f}%", fg=hue)

class PercentageCalcs:
    def __init__(self):
        self.data = storage.load_data(storage.DATA_FILE)
    
    def get_percent(self):
        prev_total = len(self.data) - 1
        total      = len(self.data)
        
        if prev_total == 0: return tuple(percent_colored
                            (100) for _ in range(3))
        
        time_pc    = percent_colored(variance(self.avg
                     ('Time spent'), self.avg
                     ('Time spent', prev_total)))
        focus_pc   = percent_colored(variance(self.avg
                     ('Focus'), self.avg('Focus', 
                     prev_total)))
        quality_pc = percent_colored(variance(
                     sum(entry['Quality range'][0] for 
                        entry in self.data) / total,
                     sum(entry['Quality range'][0] for 
                        entry in self.data[:prev_total
                        ]) / prev_total
        ))
        return time_pc, focus_pc, quality_pc
    
    def get_grouped_percent(self, data):
        prev_total = len(data)-1
        
        if not prev_total: return 100, 100
        
        time_pc  = percent_colored(variance(self.avg(
                   'Time spent', data=data), self.avg(
                   'Time spent', prev_total, 
                   data=data)))
        focus_pc = percent_colored(variance(self.avg(
                   'Focus', data=data), self.avg(
                   'Focus', prev_total, data=data)))
        
        return time_pc, focus_pc
    
    def avg(self, field, upto=None, data=None):
        data   = self.data if not data else data
        subset = data if upto is None else data[:upto]
        return sum(entry[field] for entry in subset
               ) / len(subset)

class Timetools:
    def format_time_passed(self, timestamp):
        before = dt.fromisoformat(timestamp)
        now    = dt.now()
        lapsed = (now - before).total_seconds()
        return self.get_time_diff(0, lapsed)
    
    @staticmethod  
    def format_time(total_time, total=None):
        if total:
            hours   = int(total_time / total)
            minutes = int(round(((total_time / total) 
                    - hours) * 60, 7))
        else:
            hours   = int(total_time)
            minutes = int(round((total_time - hours)
                    * 60, 7))
        
        hr   = pluralize(hours, 'hour')
        mins = pluralize(minutes, 'minute')
    
        if hours < 1:
           return color(f"{minutes} {mins}", "yellow")
        else:        
           return color(f"{hours} {hr} and {minutes} "
                + f"{mins}" if minutes else f"{hours}"
                + f" {hr}", fg="yellow")

    @staticmethod  
    def to_iso(timestamp):
        try:
            timestamp = dt.fromisoformat(timestamp)
            timestamp = timestamp.date().isoformat()
            return timestamp
        except ValueError: return None
    
    @staticmethod  
    def timestamp(iso_str, short=0, spec=0):
        """
Converts ISO timestamp into a human-readable string.

Args:
    timestamp (str): ISO 8601 datetime string.
    short (bool): If True, omits time (returns date only).
    spec (bool): If True, returns compact date (e.g., "14 Sep 2025").

Returns:
    str: Formatted timestamp string.
        """
        dt_obj = dt.fromisoformat(iso_str)
        if spec: return dt_obj.strftime("%d %b %Y")
        elif short: return dt_obj.strftime("%A, %d %B %Y")
        return dt_obj.strftime("%A, %d %B %Y • %H:%M")
        
    @staticmethod  
    def format_time_string(*args):
        parts = [f"{unit[0]} {unit[1]}" for unit in args]
        
        if "0 " in parts[-1]: parts.pop(-1)
        return ', '.join(parts[:-1]) + (
            f" and {parts[-1]} ago" if parts else 
            "just now") if len(parts) > 1 else parts[0
            ]+" ago"

    @staticmethod  
    def get_age(birthday):
        birthday = dt.fromisoformat(birthday)
        today    = dt.now()
        return int((today - birthday).days / 365.25)
    
    @staticmethod  
    def get_lapsed(last, now=None):
        lapsed = last
        if now: lapsed = now - last
        s = pluralize(lapsed, "second")
        string = f"{int(lapsed)} {s} ago"
        return string, lapsed

    def format_unit(self, lapsed, unit, major_label, 
                    minor_label):
        major     = int(lapsed / unit)
        minor     = round((lapsed - (major * unit)))
        major_str = pluralize(major, major_label)
        minor_str = pluralize(minor, minor_label)
        return self.format_time_string([major, major_str], 
               [minor, minor_str]), major
        
    def get_mins(self, lapsed):
        return self.format_unit(lapsed, 60, "minute", 
               "second")  

    def get_hrs(self, lapsed):
        return self.format_unit(lapsed, 60, "hour", 
               "minute")
        
    def get_days(self, lapsed):
        return self.format_unit(lapsed, 24, "day", "hour")
    
    def get_weeks(self, lapsed):
        return self.format_unit(lapsed, 7, "week", "day")

    def get_months(self, lapsed):
        return self.format_unit(lapsed, 4, "month", "week")
    
    def get_years(self, lapsed):
        return self.format_unit(lapsed, 12, 1,  "year", 
               "month")
    
    def get_time_diff(self, now, last):
        """
Returns a fuzzy human-readable time difference string (e.g., "3 hours and 12 minutes ago").
        """
        s, lapsed = self.get_lapsed(last,
                    now) if now else self.get_lapsed(last)
        
        # Checks if user has tempered with device date
        tempered = lapsed < -5
        
        if -5 <= lapsed < 1: return "Just now"
            
        # Thresholds for escalation to next unit
        thresholds = [60, 60, 24, 7, 4.3482, 12]
        funcs = [
            self.get_mins, self.get_hrs, 
            self.get_days, self.get_weeks, 
            self.get_months, self.get_years
        ]

        for limit, func in zip(thresholds, funcs):
            if lapsed>=limit: s, lapsed = func(lapsed)
            else: break
        
        return s if not tempered else warning(
            'Tempered with device date', inline=True)
        
timetools = Timetools()
pc        = PercentageCalcs()