from data import TEXTS, printc
from json import load
import os

title = '''
  _____   _                   ____   _   __          ___             ____   _   __ 
 |  _  \\ | |          /\\     / ___| | | / /         |_  |    /\\     / ___| | | / / 
 | |_) | | |         /  \\    | |    | |/ /            | |   /  \\    | |    | |/ /  
 |  _ <  | |        / /\\ \\   | |    |   <             | |  / /\\ \\   | |    |   <  
 | |_) | | |____   / ____ \\  | |___ | |\\ \\        /\\__/ / / ____ \\  | |___ | |\\ \\ 
 |_____/ |______| /_/    \_\\ \\____| |_| \\_\\       \____/ /_/    \_\\ \\____| |_| \\_\\
'''

with open("database.json", "r", encoding="utf-8") as file:
    L = 0 if load(file)["Language"] == "en" else 1

while True:
    print('\n\n\n')

    printc(title, color="yellow")

    print('\n\n\n\n')
    action = input(TEXTS["play"][L]).lower()
    if action.startswith("pl") or action.startswith("gr"):
        os.startfile("black_jack.py")
        exit()
    elif action.startswith("se") or action.startswith("us"):
        os.startfile("settings.py")
        exit()
    os.system("cls")