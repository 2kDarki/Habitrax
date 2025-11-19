"""
This module brings philosophy and self-reflection into your system:

- Gratitude: Practicing being thankful
           - To be thankful of what is happening or 
             has happened in ones life
           - To avoid taking the good for granted.
- Extra Services Ledger: Tracks when you go above 
                         and beyond.
- Coffer: Your personal bank — all money movements are 
          logged here.
- Almanack: A personal Bible, containing:
          - Your Chief Aim
          - Your Ten Commandments — principles to 
            abide by for becoming a "definite" person.
These additions make the system not just about productivity, but about transformation.
"""
from .toolbox import timetools, choose_from, main_menu
from .toolbox import color, label, variables, warning
from .toolbox import underline, no_data, list_options
from .toolbox import choose, money, center, ExitError
from .debrief import debrief_review
from operator import itemgetter 
from datetime import datetime
from . import slight_edge
from . import storage
from . import level
import shutil
import time

user = storage.load_data(storage.USER_FILE)
try: user.get("Check")
except AttributeError: user = {}
NAME = user.get("Name") or "Unknown"

def menu():
    header = center("《 Soul Work 》", line="—")
    print(f"\n{header}\n")
    
    options = {
        "Daily gratitude": gratitude,
        "Slight edge": slight_edge.menu,
        "Extra services ledger": extra_service_ledger,
        "Coffer": coffer,
        "Almanack": almanack
    }
    
    list_options(options)    
    choose(options, src=menu)

def gratitude():
    header = center(" Daily Gratitude ")
    print(f"\n{color(header, 'green')}\n")
    
    start = time.time()    
    print(color("I'm grateful for", underule=1)+":")
    try: graces = [input(color(">>> ", "magenta"))
                  for _ in range(5)]
    except (EOFError, KeyboardInterrupt) as e: 
        if isinstance(e, KeyboardInterrupt): print()
        main_menu()
        return
    
    end      = time.time()
    duration = round((end - start) / 3600, 3)
    print()
    
    labels = label([
        "Focus level (1–10): ", 
        "Uncertainty in focus (±): "
    ])
    
    focus, fuzziness = variables(labels)
        
    focus     = max(0, min(focus,     10))
    fuzziness = max(0, min(fuzziness,  2))

    q_min   = max( 0, (focus - fuzziness) * duration)
    q_max   = min(10, (focus + fuzziness) * duration)
    q_range = [q_min, q_max]

    daily_grace = {
        "Timestamp": datetime.now().isoformat(),
           "Graces": graces,
             "Time": time.time()
    }
    
    session = {
            "Timestamp": datetime.now().isoformat()  ,
                 "Task": "Meditation (via gratitude)",
             "Category": "Meditation"                ,
                "Focus": focus                       ,
            "Fuzziness": fuzziness                   ,
           "Time spent": duration                    ,
        "Quality range": [round(q,2) for q in q_range]
    }
    
    storage.save_entry(storage.GRACES, daily_grace)
    storage.save_entry(storage.DATA_FILE, session)
    slight_edge.ballot(1)
    level.Stat("Meditation").level_up()
    footer = center(
        " ✔ Gratitude Session Logged Successfuly! ",
        line="—")
    print(f"\n{footer}\n")

def extra_service_ledger():
    header = center(" Extra Services Ledger ")
    print(f"\n{color(header, 'green')}\n")
    
    labels = label([
        "Service rendered to: ", 
        "Nature of service: "
    ])
    
    options = ["Log entry", "View rendered services"]
    list_options(options, "Choose action")
    choice = choose(options, 1, extra_service_ledger)
    print()
    if choice == 1:
        header = center(" Viewing rendered services ")
        print(f"{color(header, 'green')}\n")
        debrief_review(1)
        return
    elif choice is None: return
    
    list_options(guide="Enter extra service rendered")    
    try:
        service = {
            "Timestamp": datetime.now().isoformat(),
            "Entry": {
                "Subject": input(labels[0]),
                "Service": input(labels[1])
            },
           "Time": time.time()
        }
    except (EOFError, KeyboardInterrupt) as e: 
        if isinstance(e, KeyboardInterrupt): print()
        main_menu()
        return
    
    storage.save_entry(storage.SERVICES, service)
    slight_edge.ballot(1)
    footer = center(
             " ✔ Extra Service Rendered Logged ", 
             line="—")
    print(f"\n{footer}")

def coffer(getter=False, view=False, cashflow=False):
    bank = storage.load_data(storage.COFFER)
    if not bank:
        bank = {
            "Main": {
                "Name": NAME,
                "Amount": 0,
                "Opened": datetime.now().isoformat()
            },
            "History": []
        }
        storage.save_data(storage.COFFER, bank)
      
    coffers = bank["Main"]["Amount"]
    if getter: return coffers
    
    history = bank["History"]
    labels = label([
        "Enter amount to deposit: ", 
        "Enter amount to withdraw: ",
        "Balance:"
    ])
    
    def deposit():
        print()
        try:
            amount = float(input(labels[0]))
            if amount <= 0: raise ValueError
        except Exception as e:
            if isinstance(e, ExitError()):
                if not isinstance(e, EOFError):print()
                main_menu()
                return
            print()
            underline()
            return
            
        bank["Main"]["Amount"] += amount
        entry = {
            "Timestamp": datetime.now().isoformat(),
                 "Type": "Deposit",
               "Amount": amount,
                 "Time": time.time()
        }
        history.append(entry)
        storage.save_data(storage.COFFER, bank)
        footer = center(
           f" ${amount:.2f} Deposited Successfully! ","—")
        print(f"\n{footer}")
    
    def withdraw():
        print()
        try:
            amount = float(input(labels[1]))
            if 0 <= amount > bank["Main"]["Amount"]:
                raise ValueError
        except Exception as e:
            if isinstance(e, ExitError()):
                if not isinstance(e, EOFError):print()
                main_menu()
                return
            print()
            if amount > bank["Main"]["Amount"]:
                warning("Can't withdraw more than "
                       +"you have.\n")
            underline()
            return
            
        bank["Main"]["Amount"] -= amount
        entry = {
            "Timestamp": datetime.now().isoformat(),
            "Type": "Withdrawal",
            "Amount": amount,
            "Time": time.time()
        }
        history.append(entry)
        storage.save_data(storage.COFFER, bank)
        footer = center(
            f" ${amount:.2f} Withdrawn Successfully! ",
            line="—")
        print(f"\n{footer}")
    
    def view_account(from_term=None):
        print()
        if from_term is not None: choice = from_term
        options = [
            "View balance", 
            "View transaction history"
        ]
        
        if from_term is None:
            list_options(options)
            choice = choose(options, 1, view_account)
        
        if choice is None: return
        elif choice == 0:
            if from_term is None: print()
            print(labels[2], f"${coffers:.2f}\n")
            if from_term is None: underline()
            return
            
        # === Terminal width handling ===
        term_width = shutil.get_terminal_size(
            ).columns
        date_col_width = 11  # Fixed: "20 Sep 2025"
        
        # Fix alignment for the withdraw column when
        # text size is 15pt and above
        spacer = 1 if term_width == 46 else (2 if 
                 term_width == 43 else 0)
        
        dynamic_cols  = 3
        padding       = dynamic_cols ** 2
        borders       = dynamic_cols
        usable_width  = (term_width 
                      - date_col_width 
                      - padding 
                      - borders)
        dynamic_width = usable_width // dynamic_cols
        extra_space   = usable_width %  dynamic_cols
        deposit_w     = dynamic_width
        withdraw_w    = dynamic_width
        balance_w     = dynamic_width + extra_space
        
        def fmt(text, width):return f"{text:<{width}}"

        # === Table Header ===
        horizontal_line = color(  "—", "magenta")
        vertical_line   = color(" | ", "magenta")
        
        print("\n"+fmt("Date", date_col_width)
             + vertical_line 
             + fmt("Deposit", deposit_w) 
             + vertical_line 
             + fmt("Withdraw", withdraw_w)
             + vertical_line 
             + fmt("Balance", balance_w))
        print(horizontal_line * term_width)
        
        # Trackers to group entries by date
        track = {
              "Current": None,
            "Deposited": None,
            "Withdrawn": None
        }
        
        balance = 0
        data = sorted(history, key=itemgetter("Time")) 
        for pos, entry in enumerate(data):
            stamp = entry["Timestamp"]
            date  = timetools.timestamp(stamp, 0, 1)
            deposited = entry["Amount"] if (
                entry["Type"] == "Deposit") else 0
            withdrawn = entry["Amount"] if (
                entry["Type"] == "Withdrawal") else 0
            
            # If already tracked, reuses values
            # (avoids duplicates)
            if track["Current"] == stamp:
                deposited = track["Deposited"]
                withdrawn = track["Withdrawn"]
                
            try:
                # Peeks ahead to group entries from
                # the same day
                next_up  = data[pos+1]
                ns       = next_up["Timestamp"]
                nxt_date = timetools.timestamp(ns,0,1)
                
                # Skip printing now — wait until 
                # last entry for the date
                if date == nxt_date:
                    deposited += next_up["Amount"] if(
                        next_up["Type"] == 
                        "Deposit" ) else 0
                    withdrawn += next_up["Amount"] if(
                        next_up["Type"] == 
                        "Withdrawal" ) else 0                   
                    track["Current"]   = ns
                    track["Deposited"] = deposited
                    track["Withdrawn"] = withdrawn
                    continue                 
            except IndexError: pass
            
            # Update running balance
            balance += deposited
            balance -= withdrawn
            
            dol = money(deposited, withdrawn, balance)
            deposited, withdrawn, balance_fmt = dol
            print(fmt(date, date_col_width) 
                 + vertical_line 
                 + fmt(deposited, deposit_w) 
                 + vertical_line 
                 + fmt(withdrawn, withdraw_w+spacer)
                 + vertical_line 
                 + fmt(balance_fmt, balance_w))

        underline()
        if from_term is not None: print() 
    
    header = center(" Coffer ")        
    options = {
        "Account": view_account,
        "Deposit": deposit,
        "Withdraw": withdraw
    }
    
    if ( isinstance(    view, bool)
    and  isinstance(cashflow, bool)):
        print(f"\n{color(header, 'green')}\n")
        list_options(options)
        choose(options, src=coffer)
    elif not isinstance(    view, bool):
        view_account(view)
    elif not isinstance(cashflow, bool):
        if cashflow == 0:withdraw()
        if cashflow == 1: deposit()
        print()

def almanack():
    header = center(f" {NAME}'s Almanack ")
    print(f"\n{color(header, 'green')}\n")
    
    def aim():
        chief_aim = user.get("Aim")
        if chief_aim:
            print(f"\n{chief_aim}\n")
            underline()      
        else: no_data("No Chief Aim Found")
    
    def acts():
        decalogue = user.get("Decalogue")
        if decalogue:
            print()
            list_options(decalogue, 0, 1)
            underline()
        else: no_data("No Commandments Found")
    
    options = {
        "View chief aim": aim,
        "View Decalogue": acts
    }    
    list_options(options)
    choose(options, src=almanack)