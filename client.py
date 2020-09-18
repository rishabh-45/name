import subprocess
import os
GITHUB_REPO_LINK = os.environ.get("GITHUB_REPO_LINK", "https://github.com/justaprudev/The-TG-Bot v3")
repo = GITHUB_REPO_LINK.split()[0]
branch = GITHUB_REPO_LINK.split()[1]
print("Downloading latest version of The-TG-Bot..")
subprocess.run(f"git clone -b {branch} {repo} git && mv git/* . && rm -rf git", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print("Starting The-TG-Bot")
subprocess.run("python3 -m thetgbot", shell=True)
