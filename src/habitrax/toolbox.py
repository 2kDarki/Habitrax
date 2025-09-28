from datetime import datetime as dt
from datetime import timedelta as td
from . import storage
import calendar as cl
import unicodedata
import textwrap
import shutil
import random
import time
import os
import re

def recursive_print(text, times, end="\n", delay=0):
    for _ in range(times):
        time.sleep(delay)
        print(text, end=end)

def generate_encryption(enc_type="pin", enc_len=3):
    if enc_type == "pin":
        number = random.randint(0, (10**enc_len)-1)
        otp = zero_int(number, deno=enc_len)
    return str(otp)

def wrap_text(text, indent=0):
    width = shutil.get_terminal_size().columns
    return textwrap.fill(text, width=width, subsequent_indent=' ' * indent)
    
def money(*args):
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
        formatted.append(formats[denomination])
    return formatted

class Percentage_calcs:
    def get_percent(self):
        data = storage.load_data(storage.DATA_FILE)
        prev_total = len(data)-1
        total = len(data)
    
        prev_avg_total_time = sum(entry['Time spent'] for entry in data[:-1]) / prev_total
        avg_total_time = sum(entry['Time spent'] for entry in data) / total
        progress = variance(avg_total_time, prev_avg_total_time)
        if progress >= 0:
            time_pc = f"+{progress:.2f}%"
            time_pc = color(time_pc, fg="green")
        else:
            time_pc = f"{progress:.2f}%"
            time_pc = color(time_pc, fg="red")
    
        prev_avg_focus = sum(entry['Focus'] for entry in data[:-1]) / prev_total
        avg_focus = sum(entry['Focus'] for entry in data) / total
        progress = variance(avg_focus, prev_avg_focus)
        if progress >= 0:
            focus_pc = f"+{progress:.2f}%"
            focus_pc = color(focus_pc, fg="green")
        else:
            focus_pc = f"{progress:.2f}%"
            focus_pc = color(focus_pc, fg="red")
    
        prev_avg_qlty = (sum(entry['Quality range'][0] for entry in data[:-1]) / prev_total)
        avg_qlty = (sum(entry['Quality range'][0] for entry in data) / total)
        progress = variance(avg_qlty, prev_avg_qlty)
        if progress >= 0:
            range_pc = f"+{progress:.2f}%"
            range_pc = color(range_pc, fg="green")
        else:
            range_pc = f"{progress:.2f}%"
            range_pc = color(range_pc, fg="red")
        
        return time_pc, focus_pc, range_pc
    
    def get_grouped_percent(self, data):
        prev_total = len(data)-1
        total = len(data)
    
        if not prev_total:
            prev_avg_total_time = 0
            prev_avg_focus = 0
        else:
            prev_avg_total_time = sum(entry['Time spent'] for entry in data[:-1]) / prev_total
            prev_avg_focus = sum(entry['Focus'] for entry in data[:-1]) / prev_total
            
        avg_total_time = sum(entry['Time spent'] for entry in data) / total
        progress = variance(avg_total_time, prev_avg_total_time)
        if progress >= 0:
            time_pc = f"+{progress:.2f}%"
            time_pc = color(time_pc, fg="green")
        else:
            time_pc = f"{progress:.2f}%"
            time_pc = color(time_pc, fg="red")
        
        avg_focus = sum(entry['Focus'] for entry in data) / total
        progress = variance(avg_focus, prev_avg_focus)
        if progress >= 0:
            focus_pc = f"+{progress:.2f}%"
            focus_pc = color(focus_pc, fg="green")
        else:
            focus_pc = f"{progress:.2f}%"
            focus_pc = color(focus_pc, fg="red")    

        return time_pc, focus_pc

def variables(labels):
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
        except (ValueError, TypeError):
            pass            
        if len(varz) == 0:
            warning("Enter a number between 1 and 10.")
        else:
            warning("Enter a number between 0 and 2.")
    return varz

def choose(options, check=False, src=None, proxy=0):
    """
Custom input menu for choosing an option from a list.
If check=True, returns index.
If proxy=True, passes (proxy=True) to chosen function.
If user inputs 'clear', resets the source screen.
    """
    print(f"{len(options)+1}. Back")
    while True:
        try:
            choice = input(color(">>> ", "magenta"))
            choice = int(choice) - 1
            if 0 <= choice < len(options):
                if check:
                    return choice
                elif proxy:
                    choose_from(options, choice)(1)
                else:
                    choose_from(options, choice)()
                break
        except ValueError:
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
        warning(f"Choose a number between 1 and {len(options)+1}.")

def past(string):
    past = string.split()[0].lower()
    if past.endswith("y"):
        past = past.replace("y", "ied")
    elif past.endswith("r"):
        past += "ed"
    rest = string.split()[1:]
    return f"{past} {' '.join(rest)}"

def choose_from(iterable, choice):
    """
Takes a dictionary and a numeric index,
returns the corresponding value.
    """
    return next((iterable[run] for opt, run in enumerate(iterable) if opt == int(choice)))

def list_options(options, guide=False, spaced=False):
    """
Displays all keys in a dictionary as a numbered list.
 - guide: Optional header for the options
 - spaced: Adds empty lines between options
    """
    if guide:
        print(color(guide, underule=1)+":")
    for opt, option in enumerate(options):
        if spaced:
            print(wrap_text(f"{opt+1}. {option}"))
            print()
            continue
        print(wrap_text(f"{opt+1}. {option}"))

def label(iterable):
    return [color(head, "cyan") for head in iterable]

def no_data(message):
    print()
    print(color(center(message), "gray"))
    print()

def warning(message, inline=False):
    if inline:
        return color(message, "red")
    print()
    print(color(message, "red"))
    print()
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    header = center("《 QUESTLINE 》", 0, 1)
    print(header)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def color(text, fg=None, bg=None, bold=False, underule=False):
    colors = {
        "black": 30, "red": 31, "green": 32, 
        "yellow": 33, "blue": 34, "magenta": 35,
        "cyan": 36, "white": 37,
        "gray": 90, "lightred": 91, "lightgreen": 92,
        "lightyellow": 93, "purple": 94,
        "lightmagenta": 95, "lightcyan": 96
    }

    styles = []
    
    if bold:
        styles.append("1")
    if underule:
        styles.append("4")
    if fg in colors:
        styles.append(str(colors[fg]))
    if bg in colors:
        styles.append(str(colors[bg] + 10))  # background colors start from 40

    if styles:
        return f"\033[{';'.join(styles)}m{text}\033[0m"
    return text    
 
def number_padding(num):
    if len(str(num)) == 1:
        padded = f"  {num}"
    elif len(str(num)) == 2:
        padded = f" {num}"
    else:
        padded = num
    return padded
        
def visual_width(s):
    clean = strip_ansi(s)
    width = 0
    for ch in clean:
        if unicodedata.east_asian_width(ch) in ['F', 'W']:
            width += 2
        else:
            width += 1
    return width

def center(text, lined=False, doubled=False, get=0, fixed=0):
    term_width = shutil.get_terminal_size((80, 20)).columns
    display_len = visual_width(text)
    
    # Centers stats in status window
    if fixed:
        display_len = 41
    total_pad = max(term_width - display_len, 0)
    left_pad = total_pad // 2
    
    # magic number 56 used to fix termux centering
    # alignement
    left_pad -= 1 if ("█" or "▒") and "%" in text and term_width < 56 else 0
    right_pad = total_pad - left_pad
    if get:
        return left_pad, total_pad, right_pad

    if lined or doubled:
        line_char = "—" if lined else "="
        line_color = "magenta" if lined else "green"
        text_color = "green" if lined else "lightgreen"

        left = color(line_char * left_pad, fg=line_color)
        
        right = color(line_char * right_pad, fg=line_color)
        middle = color(text, fg=text_color)
        return f"{left}{middle}{right}"
    else:
        return " " * left_pad + text


def strip_ansi(s):
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '',s)

def underline(dotted=False):
    term_width = shutil.get_terminal_size((80, 20)).columns
    print(color("-"*term_width, "magenta")) if dotted else print(color("—"*term_width, "magenta"))
    
def make_progress_bar(pct, width=20):
    filled = int(pct * width)
    return "█" * filled + "▒" * (width - filled)

def rated_bar(pct, width=20):
    control = int(pct * width)
    filled = min(int(pct * width), 7)
    line = "_" * int(pct * 24)
    first = "█" * filled + "▒" * (7 - filled)
    rate = zero_int(f"{(pct * 100):.2f}")
    last = "▒" * 7
    if pct > 0.6:
        pct -= 0.6
        filled = min(int(pct * width), 7)
        last = "█" * filled + "▒" * (7 - filled)
        
    return line, f"{first}{rate}%{last}"


def get_exp(category):
    data = storage.load_data(storage.DATA_FILE)
    
    exp = 0
    for entry in data:
        if entry["Category"] == category:
            exp += entry["Time spent"]

    return exp
    
def pluralize(n, word):
    if n == 1:
        return word
    else:
        return word + 's'
        
def variance(new, old):
    if old:
        return ((new - old) / old) * 100
    elif not new and not old:
        return 0
    else:
        return 100

def zero_int(number, deno=2):
    length = len(str(int(float(number))))
    if length < deno:
        zeros = (deno - length) * "0"
        number = f"{zeros}{number}"
    return number
    
def format_number(*args):
    formatted = []
    for item in args:
        if int(item) < 10:
            item = f"0{item}"
            formatted.append(item)
        else:
            formatted.append(item)
    return formatted

class Timetools:
    def format_time_passed(self, timestamp):
        before = dt.fromisoformat(timestamp)
        now = dt.now()
        lapsed = (now - before).total_seconds()
        ago = self.get_time_diff(0, lapsed)
        return ago
    
    def format_time(self, total_time, total=None):
        if total:
            hours = int(total_time / total)
            minutes = int(((total_time / total) - hours) * 60)
        else:
            hours = int(total_time)
            minutes = int((total_time - hours) * 60)
        
        hr = pluralize(hours, 'hour')
        mins = pluralize(minutes, 'minute')
    
        if hours < 1:
            return color(f"{minutes} {mins}", fg="yellow")
        else:        
            return color(f"{hours} {hr} and {minutes} {mins}" if minutes else f"{hours} {hr}", fg="yellow")

    def to_iso(self, timestamp):
        try:
            timestamp = dt.fromisoformat(timestamp)
            timestamp = timestamp.date().isoformat()
            return timestamp
        except ValueError:
            return None
    
    def timestamp(self, timestamp, short=0, spec=0):
        """
Converts ISO timestamp into a human-readable string.

Args:
    timestamp (str): ISO 8601 datetime string.
    short (bool): If True, omits time (returns date only).
    spec (bool): If True, returns compact date (e.g., "14 Sep 2025").

Returns:
    str: Formatted timestamp string.
    """
        # Parse ISO datetime string
        parsed = dt.fromisoformat(timestamp)
        year, month, date, hour, minute = parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute

        # Get full month name and weekday index
        month_name = cl.month_name[month]
        weekday = cl.weekday(year, month, date)
        day = cl.day_name[weekday]

        # Format date, hour and minute (adds leading 
        # zero if needed)
        date, hour, minute = format_number(
            date, hour, minute)
        
        if spec:
            return f"{date} {month_name[:3]} {year}"
        return f"{day}, {date} {month_name} {year} • {hour}:{minute}" if not short else f"{day}, {date} {month_name} {year}"
        
    def format_time_string(self, big, small, b, s, smaller=None, ss=None):
        if smaller:
            string = f"{big} {b}, {small} {s} and {smaller} {ss} ago"
        elif small:
            string = f"{big} {b} and {small} {s} ago"
        else:
            string = f"{big} {b} ago"
        return string

    def get_age(self, birthday):
        birthday = dt.fromisoformat(birthday)
        today = dt.now()
        age = int((today - birthday).days / 365.25)
        return age

    def get_lapsed(self, last, now=None):
        lapsed = last
        if now:
            lapsed = now - last
        s = pluralize(lapsed, "second")
        string = f"{int(lapsed)} {s} ago"
        return string, lapsed

    def get_mins(self, lapsed):
        mins = int(lapsed / 60)
        sec = int(lapsed - (mins * 60))
        m = pluralize(mins, "minute")
        s = pluralize(sec, "second")
        string = self.format_time_string(mins, sec, m, s)
        return string, mins

    def get_hrs(self, lapsed):
        hrs = int(lapsed / 60)
        mins = int(lapsed - (hrs * 60))
        h = pluralize(hrs, "hour")
        m = pluralize(mins, "minute")
        string = self.format_time_string(hrs, mins, h, m)
        return string, hrs
        
    def get_days(self, lapsed):
        days = int(lapsed / 24)
        hrs = int(lapsed - (days * 24))
        d = pluralize(days, "day")
        h = pluralize(hrs, "hour")
        string = self.format_time_string(days, hrs, d, h)
        return string, days
    
    def get_weeks(self, lapsed):
        wks = int(lapsed / 7)
        days = int(lapsed - (wks * 7))
        w = pluralize(wks, "week")
        d = pluralize(days, "day")
        string = self.format_time_string(wks, days, w, d)
        return string, lapsed

    def get_months(self, lapsed):
        mon = int(lapsed / 30.417)
        days = int(lapsed - (mon * 30.417))
        m = pluralize(mon, "month")
        d = pluralize(days, "day")
        string = self.format_time_string(mon, days, m, d)
        if days >= 7:
            wks = int(days / 7)
            days = int(days - (wks * 7))
            d = pluralize(days, "day")
            w = pluralize(wks, "week")
            fs = self.format_time_string
            if days:
                string = fs(mon, wks, m, w, days, d)
            else:
                string = fs(mon, wks, m, w)
    
        return string, lapsed
    
    def get_time_diff(self, now, last):
        """
Returns a fuzzy human-readable time difference string (e.g., "3 hours and 12 minutes ago").
        """
        
        string, lapsed = self.get_lapsed(last, now) if now else self.get_lapsed(last)
        
        # Checks if user has tempered with device date
        tempered = True if -5 > lapsed else False
        
        if -5 <= lapsed < 1:
            return "Just now"
            
        # Thresholds for escalation to next unit
        thresholds = [60, 60, 24, 7, 30.417]
        funcs = [
            self.get_mins, self.get_hrs, 
            self.get_days, self.get_weeks, 
            self.get_months
        ]

        for limit, func in zip(thresholds, funcs):
            if lapsed >= limit:
                string, lapsed = func(lapsed)
            else:
                break

        
        return string if not tempered else warning('Tempered with device date', inline=True)
        
def var_per_cat(index=None, grouped=None):
    data = storage.load_data(storage.LEVEL_FILE)
    entry = data[index]
    now = time.time()
    last = entry["Time"]
    lapsed = timetools.get_time_diff(now, last)
    date = timetools.timestamp(entry["Timestamp"])
    level = entry["Level"] * 10
    try:
        exp = get_exp(entry["Category"])
    except KeyError:
        return None
    if grouped:
        level, exp = grouped
        level *= 10
    progress = exp - level
    exp_pc = (progress / 10) * 100 if level < 1000 else 100
    bar = make_progress_bar(exp_pc/100)
    return bar, date, lapsed, exp_pc

timetools = Timetools()
pc = Percentage_calcs()