# -*- coding: utf-8 -*-
"""
🦊 FOXWIKIBOT 🤖
Maintained by Janorovic Volkov (Indonesian Wikipedia Users)
"""

import os
import sys
import time
import importlib
import subprocess
import requests
from user_and_password import API_URL, USERNAME, PASSWORD, USER_AGENT

# === TERMINAL COLORS ===
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"
BOLD = "\033[1m"

# === CHECKING MODULES ===
REQUIRED_MODULES = ["requests"]

def check_requirements():
    missing = []
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"{YELLOW}[Foxwikibot] Installing module: {', '.join(missing)}...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print(f"{CYAN}[Foxwikibot]: Module installed!{RESET}\n")

check_requirements()

# === SETUP SESSION ===
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def api_get(params):
    params["format"] = "json"
    return session.get(API_URL, params=params).json()

def api_post(data):
    data["format"] = "json"
    return session.post(API_URL, data=data).json()

def login():
    print(f"{CYAN}🔑 Logging in as {USERNAME}...{RESET}")
    token = api_get({"action": "query", "meta": "tokens", "type": "login"})["query"]["tokens"]["logintoken"]
    r = api_post({
        "action": "login",
        "lgname": USERNAME,
        "lgpassword": PASSWORD,
        "lgtoken": token
    })
    if r.get("login", {}).get("result") != "Success":
        print(f"{YELLOW}[Foxwikibot] Failed to login: {r}{RESET}")
        sys.exit(1)

    info = api_get({"action": "query", "meta": "userinfo"})
    username = info["query"]["userinfo"]["name"]
    print(f"{CYAN}[Foxwikibot] Logged in as: {username}{RESET}\n")
    return username

def get_csrf():
    return api_get({"action": "query", "meta": "tokens", "type": "csrf"})["query"]["tokens"]["csrftoken"]

def list_scripts():
    if not os.path.isdir("skrip"):
        os.makedirs("skrip", exist_ok=True)
    scripts = [f for f in os.listdir("skrip") if f.endswith(".py")]
    return scripts

# === UI ===
def banner(username):
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""
{BLUE}{BOLD}-------------------------------------------------------------
🦊 FOXWIKIBOT WIKI BOT OS 🤖
-------------------------------------------------------------
Maintained by Janorovic Volkov (Indonesian Wikipedia Users)
{RESET}
Hello, {BOLD}{username}{RESET}! Where are you going today?
""")

def goodbye(username):
    print(f"\n{BLUE}Goodbye, {username}! Have a great day 😉{RESET}")
    sys.exit(0)

def main():
    username = login()
    while True:
        banner(username)
        scripts = list_scripts()

        print(f"{BOLD}Script list:{RESET}")
        if not scripts:
            print(f"{YELLOW}[Foxwikibot] No scripts found in 'skrip/' folder.{RESET}")
        else:
            for i, s in enumerate(scripts, 1):
                print(f" {BLUE}{i}.{RESET} {s}")

        print(f" {BLUE}{len(scripts)+1}.{RESET} Exit\n")

        choice = input(f"{YELLOW}[Foxwikibot] Select your code you want to operate => {RESET}").strip()
        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice == len(scripts) + 1:
            goodbye(username)
        elif 1 <= choice <= len(scripts):
            script_name = scripts[choice - 1]
            print(f"\n{CYAN}[Foxwikibot] Running {script_name}...{RESET}\n")
            mod = importlib.import_module(f"skrip.{script_name[:-3]}")
            if hasattr(mod, "run"):
                try:
                    mod.run(session, API_URL, get_csrf)
                except Exception as e:
                    print(f"{YELLOW}[Foxwikibot] Error executing script: {e}{RESET}")
            else:
                print(f"{YELLOW}[Foxwikibot] Script {script_name} missing 'run()' function.{RESET}")
            input(f"\n{YELLOW}[Foxwikibot] Press Enter to return to FoxWikiBot OS...{RESET}")
        else:
            continue

# === MAIN ===
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting...")
