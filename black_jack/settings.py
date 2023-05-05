import json
from data import TEXTS, printc, is_yes, Table
from keyboard import add_hotkey
import os

with open("database.json", "r", encoding="utf-8") as file:
    data = json.load(file)

L = 0 if data["Language"] == "en" else 1
CODES = {"Language": "lang", "Games to win": "win", "Dealer min points": "min", "Max points": "max", "Show points": "show points", "Show bots points": "show bots"}
changed = False

#hotkeys
add_hotkey("Esc", exit)

while True:
    with open("database.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    os.system("cls")
    printc(TEXTS["exit"][L], color=(127, 127, 127))

    if changed: printc(TEXTS["changed"][L], color=(255, 0, 0))

    a = Table(["Setting", "Value", "Default", "Code"], [i for i in data.keys() if i != "Defaults"], [[data[i], data["Defaults"][i], CODES[i]] for i in data.keys() if i != "Defaults"], 17, "Settings", (255, 200, 175), (255, 0, 255), (255, 255, 0), (0, 255, 255), (255, 255, 255))
    a.print_()

    printc(TEXTS["reset"][L], color=(200, 150, 140))

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

    changed = True
    data[setting] = value
    with open("database.json", "w", encoding="utf-8") as file:
        json.dump(data, file)