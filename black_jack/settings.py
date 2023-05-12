import json
from data import TEXTS, printc, is_yes, Table
from keyboard import add_hotkey
import os

def exit_():
    os.startfile("start.py")
    exit()

try:
    with open("database.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for i in ["Language", "Games to win", "Dealer min ponints", "Max points", "Show points", "Show bots points"]:
        a = data[i]
        a = data["Defaults"][i]
except:
    data = {"Language": "en", "Games to win": 3, "Dealer min points": 17, "Max points": 21, "Show points": True, "Show bots points": False, "Defaults": {"Language": "en", "Games to win": 3, "Dealer min points": 17, "Max points": 21, "Show points": True, "Show bots points": False}}
    with open("database.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

L = 0 if data["Language"] == "en" else 1
CODES = {"Language": "lang", "Games to win": "win", "Dealer min points": "min", "Max points": "max", "Show points": "show points", "Show bots points": "show bots"}

#hotkeys
add_hotkey("Esc", exit_)
while True:
    with open("database.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    os.system("cls")
    printc(TEXTS["exit"][L])

    a = Table(["Setting", "Value", "Default", "Code"], [i for i in data.keys() if i != "Defaults"], [[data[i], data["Defaults"][i], CODES[i]] for i in data.keys() if i != "Defaults"], 17, "Settings")
    a.print_()

    printc(TEXTS["reset"][L], color="cyan")

    setting = input().lower()
    if "lan".startswith(setting) or setting.startswith("lan"):
        value = "pl" if input("en/pl: ").lower() == "pl" else "en"
        setting = "Language"
    elif "win".startswith(setting) or setting.startswith("win"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Games to win"
    elif "min".startswith(setting) or setting.startswith("min"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Dealer min points"
    elif "max".startswith(setting) or setting.startswith("max"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Max points"
    elif "show points".startswith(setting) or setting.startswith("show points"):
        value = is_yes(input(TEXTS["bool value"][L]))
        setting = "Show points"
    elif "show bots".startswith(setting) or setting.startswith("show bots"):
        value = is_yes(input(TEXTS["bool value"][L]))
        setting = "Show bots points"
    elif "reset".startswith(setting) or setting.startswith("reset"):
        if is_yes(input(TEXTS["confirm"][L])):
            for key in data.keys():
                if key == "Defaults": continue
                data[key] = data["Defaults"][key]
            with open("database.json", "w", encoding="utf-8") as file:
                json.dump(data, file)
            changed = True
        continue
    else:
        continue

    data[setting] = value
    with open("database.json", "w", encoding="utf-8") as file:
        json.dump(data, file)