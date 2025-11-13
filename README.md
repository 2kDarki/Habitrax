# Habitrax

*A terminal-based personal development tracker combining habit building, productivity, and introspection into one unified system.*

 --- 

## What is Habitrax? 

Habitrax is a CLI app designed to help you:

- Track your tasks, productivity, and self-discipline
- Reflect daily with randomized deep questions 
- Monitor progress using gamified stats and leveling 
- Build powerful habits using philosophies from: 
 - Deep Work
 - Atomic Habits
 - Slight Edge
 - Think & Grow Rich
 - Shadow Work Journal 

> You don't just live life — you *level through it*. 

--- 

## Quickstart

```
git clone https://github.com/2kDarki/Habitrax.git 
cd Habitrax 
python run.py
```

> Requires Python 3.10+. 

That's it — Habitrax runs out-of-the-box.

---

## Core Modules

- Session Logging – Track tasks, time, focus, and productivity quality
- Debrief – Daily introspection with randomized deep questions
- Soul Work – Gratitude, philosophy, and "Slight Edge" voting
- Status Window – Gamified dashboard for categories and missions
- Notebook – Store insights, mantras, or journal entries
- Statistics – Filter and visualize productivity trends
- Missions – Self-defined goals with tracked completion
- Coffer – Manually track your finances
- Almanack – Define your chief aim and personal commandments

---

## Folder Structure
```
Habitrax/ 
        ├── src/ 
        │   └── habitrax/    ← App source code
        ├── data/            ← Stored user data (JSON) 
        ├── pyproject.toml   ← Packaging configuration 
        ├── requirements.txt ← Empty (0 dependencies) 
        ├── run.py           ← Entry point 
        ├── README.md        ← You are here
        ├── LICENSE 
        └── .gitignore 
```

---

## Contributing

Want to improve Habitrax? Here's how:
- Fork the repo
- Create a branch: git checkout -b feat/my-feature or git checkout -b fix/bug
- Make your changes in src/habitrax/ or data/
- Stage and commit: git add . git commit -m "Short, clear message describing your change" 
- Push your branch: git push origin feat/my-feature
- Open a Pull Request — describe your change clearly
- Optional: add a minimal test in tests/

---

## Realistic First Tasks
Even if you've never seen the code before, here are 3 tasks anyone can try:
- Improve Debrief Randomization – Add optional filters for categories or difficulty of questions
- Add a CLI Shortcut – For example, a quick command to show today's top task

These tasks are small, self-contained, and won't break the core functionality.

---

## Data & Privacy

- All user data is stored locally in JSON files
- You can back up or migrate manually
- Future versions may support encryption or SQLite (if you can, you may work on this)

---

## Limitations

- Minimal CLI interface — designed for speed and simplicity
- No undo or in-app editing (by design)
- Manual testing only — no automated tests yet

---

## License

MIT License — Free to use, modify, or build upon. Mention appreciated if published or monetized.

---

## About the Author

Self-taught dev passionate about programming and philosophy. Built this to not just track productivity — but to master the self.