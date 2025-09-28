from pathlib import Path
from sys import path

path.append(str(Path(__file__).resolve().parent/"src"))

from habitrax.main import main

if __name__ == "__main__":
    main()