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
    for i in ["Language", "Games to win", "Dealer min ponints", "Max points", "Show points"]:
        a = data[i]
        a = data["Defaults"][i]
except:
    data = {"Language": "en", "Games to win": 3, "Dealer min points": 17, "Max points": 21, "Show points": True, "Defaults": {"Language": "en", "Games to win": 3, "Dealer min points": 17, "Max points": 21, "Show points": True}}
    with open("database.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

L = 0 if data["Language"] == "en" else 1
CODES = {"Language": "language", "Games to win": "win", "Dealer min points": "minimum", "Max points": "maximum", "Show points": "show points"}

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
    if "langua".startswith(setting) or setting.startswith("langua"):
        value = "pl" if input("en/pl: ").lower() == "pl" else "en"
        setting = "Language"
    elif "win".startswith(setting) or setting.startswith("win"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Games to win"
    elif "minim".startswith(setting) or setting.startswith("minim"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Dealer min points"
    elif "maxim".startswith(setting) or setting.startswith("maxim"):
        value = int(input(TEXTS["int value"][L]))
        setting = "Max points"
    elif "show po".startswith(setting) or setting.startswith("show po"):
        value = is_yes(input(TEXTS["bool value"][L]))
        setting = "Show points"
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