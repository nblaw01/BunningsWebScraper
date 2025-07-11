import os
import sys

"""
- This script checks if the number of allowed runs has been exceeded
- Updates the run count if not exceeded
- Exits the program if MAX_RUNS is reached
"""

RUN_COUNT_FILE = "run_count.txt"
MAX_RUNS = 31

def check_run_count():
    count = 0
    if os.path.exists(RUN_COUNT_FILE):
        try:
            with open(RUN_COUNT_FILE, "r") as f:
                count = int(f.read().strip())
        except ValueError:
            count = 0

    if count >= MAX_RUNS:
        print(f"Max run count ({MAX_RUNS}) reached. Exiting.")
        sys.exit(0)

    count += 1
    with open(RUN_COUNT_FILE, "w") as f:
        f.write(str(count))
    print(f"Run count: {count}")