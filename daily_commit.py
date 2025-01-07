import os
import random
import subprocess
from datetime import datetime

# Generate a random commit number between 100 and 200 (or adjust as needed)
commit_number = random.randint(100, 200)  # You can change the range here

# Get the current date and time for the commit message
commit_message = f"Commit {commit_number} on {datetime.now().strftime('%Y-%m-%d')}"

# Path to your repository (change if necessary)
repo_path = "/Users/nitinmaharaj/Jarvis"  # Adjust this to the actual path of your repo

# Change directory to the repository
os.chdir(repo_path)

# Ensure the repository is up-to-date
subprocess.run(["git", "pull"])

# Stage all changes
subprocess.run(["git", "add", "."])

# Commit with the generated message
subprocess.run(["git", "commit", "-m", commit_message])

# Push the commit to the GitHub repository
subprocess.run(["git", "push"])

print(f"Commit successful: {commit_message}")
