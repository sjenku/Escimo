import subprocess
import sys

# Path to your Python interpreter, adjust if needed
python_interpreter = sys.executable  # Uses the same Python interpreter as the current script

# Number of times to run the script
NUM_RUNS = 50


for i in range(NUM_RUNS):
    print(f"Running iteration {i + 1}")
    subprocess.run([python_interpreter, 'main.py'])