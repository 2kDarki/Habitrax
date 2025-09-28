"""
Introduction
This module contains metadata information about the Habitrax project — also known as 《 QUESTLINE 》 in the UI.

Display Notice
For the CLI version of Habitrax to display output beautifully, it is recommended that you set your console or terminal text size to 16pt.

History
Habitrax first began as a way to measure how deeply I engage during a focused session. The idea came to me while reading Deep Work.

I started the project — then named DeepWork — on 29 July 2025, and finished the first version on that very same day.

As I grew more proficient in programming and more curious about self-development systems, the project evolved with every addition. One major turning point came while reading Atomic Habits. It wasn't a new feature that got added — it was a revamp of my approach to building this project: I started applying the principle of "Make it Easy" to all my code, which, unsurprisingly, had many overlaps with DRY.

To reduce redundancy, I created the toolbox.py module and dumped all reused code there — even one-liners.

Throughout August 2025 and up to 19 September 2025, I kept refining, expanding, and polishing the system. Along the way, it went through many names before finally becoming Habitrax.

Name Evolution

1. DeepWork 
   A simple logger that tracked deep work sessions and helped assess whether my focus was improving.

2. Opsian
   With the integration of habit-building modules like `debrief.py` and `status_window.py`, DeepWork became gamified and more holistic. It transformed from a productivity timer to a personal development *system*. So I renamed it to *Opsian* (from "ops" = operations + "ian" = like/in the manner of).

3. Prodian
   Eventually, I wanted to reserve *Opsian* for a future AI project, so I renamed the system to *Prodian* (Prod = productivity + ian).

4. GoL (Game of Life)  
   As I neared the end of development, I added deeply reflective and philosophical modules inspired by books like Think and Grow Rich and The Slight Edge. This marked a shift from just productivity to self-mastery. Thus the name GoL was born.

5. Habitrax
Finally, for the public CLI release, I chose a name that better communicates what the app does: habit building + progress tracking = Habitrax. Internally, the UI still displays 《 QUESTLINE 》 as a nod to the system’s RPG/gamified structure.

Soul Work Modules
The soul_work.py module brings philosophy and self-reflection into your system:

- Extra Services Ledger: Tracks when you go above and beyond.
- Coffer: Your personal bank — all money movements are logged here.
- Almanack: A personal Bible, containing:
  - Your Chief Aim
  - Your Ten Commandments — principles to abide by for becoming a “definite” person.
These additions make the system not just about productivity, but about *transformation*.

Conclusion
Habitrax has been one of the most rewarding things I’ve built. It taught me more than just programming — it taught me patience, persistence, problem-solving, and how to build systems that evolve with you.

I encountered bugs. I almost gave up a few times. But I pushed through until it became something I’m proud of.

And now? I'm heading back to the project I paused to make Habitrax possible. The backlog is huge, and some projects I don’t even know how to structure yet🥲.

But if Habitrax taught me anything, it’s this:
Build one feature at a time. Do it well. And soon, it will be done.
"""

__version__ = "dw.cli.1.1"

from . import toolbox

def __author__():   
    title = toolbox.label(["Developer:"])[0]    
    text = [
    "Hi, I’m Darki — builder of Habitrax (《 QUESTLINE 》)",
    "I created this project as a personal tool to track, measure, and improve every part of my day — from productivity and habits to finances and self-reflection.",
    "I’m not a professional developer (yet), but I love building systems that solve my own problems. Habitrax started as a quick script to log deep work sessions, but it quickly grew into a full-fledged personal development environment.",
    "Every module, stat, and design decision in this app came from a real need I had. That’s why it works the way it does — not bloated, not perfect, but powerful for anyone who wants to take their self-discipline and growth seriously.",
    "I plan to release mobile versions in the future, learn more about APIs and databases, and hopefully turn this into something more people can use easily.",
    "Until then, feel free to explore, modify, and build your own system from this foundation."
    ]
      
    for paragraph in text:
        print(toolbox.wrap_text(paragraph))
        print()   
    print(f"{toolbox.color('Contact', underule=1)}:")
    print("""    Email: darkian.dev@gmail.com
  GitHub: github.com/2kDarki
  Other platforms: platform.com/2kdarki
  WhatsApp: 078 062 0641
  Timezone: CAT (Central African Time)
""")
    print()
    print(title, "Caleb 'Darki' Sibanda")

def menu():
    header = toolbox.center(" About ")
    print(f"\n{toolbox.color(header, 'green')}\n")
    
    options = [
        "Current version",
        "About Habitrax (Questline)",
        "Developer"
    ]
    
    labels = toolbox.label(
        [opt+":" for opt in options]
    )
    
    toolbox.list_options(options)
    choice = toolbox.choose(options, 1, menu)
    if not choice and choice != 0:
        return
    elif choice == 0:
        print()
        print(labels[choice], __version__)
    elif choice == 1:
        print()
        print(__doc__)
    else:
        __author__()
    
    print()
    toolbox.underline()