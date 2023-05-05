from data import *
from time import sleep
from random import choice
import os
from keyboard import add_hotkey
from json import load
import subprocess
import sys

def apply(): 
    os.system("cls")
    subprocess.call([sys.executable, "black_jack.py"]) #ChatGPT
    exit() 
'''TODO: interface'''
#settings
with open("database.json", "r", encoding="utf-8") as file:
    SETTINGS = load(file)

#language
L = 0 if SETTINGS["Language"] == "en" else 1

#hotkeys
add_hotkey("shift + ctrl", lambda: os.system(f"start settings.py {L}"))
add_hotkey("ctrl + q", apply)
printc(TEXTS["settings"][L], color=(255, 0, 0))

#player
player = Player()

#bots
p1 = Bot("Bot 1")
p2 = Bot("Bot 2")
p3 = Bot("Bot 3")

#dealer
dealer = Bot("Dealer")

PAUSE = 0.5 #pause
PLAYERS = [player, p1, p2, p3]

#pause before game
sleep(2)
#all games
while all(i.get_status()["won"] < SETTINGS["Games to win"] for i in [player, p1, p2, p3]):
    #score
    printc(TEXTS["total score"][L], color=(127, 0, 0))
    for p in PLAYERS:
        printc(p.name, "-", p.get_status()["won"], color=(255, 0, 0))
    sleep(PAUSE)
    #reset
    for entity in [player, p1, p2, p3, dealer]:
        entity.new_game()
    deck = DECK.copy()
    flag = True
    winners = list()
    #random order of players
    players = PLAYERS.copy()
    order = PLAYERS.copy()
    players.clear()
    for i in range(4):
        el = choice(order)
        order.remove(el)
        players.append(el)
    #a game round
    while flag: #while at least 1 player took a card
        flag = False
        for p in players:
            #bots
            if isinstance(p, Bot):
                if p.think():
                    p.take(deck)
                    flag = True
                    printc(p.name, TEXTS["bot take"][L], color=(0, 255, 0))
                    if SETTINGS["Show bots points"]: printc(p.name, TEXTS["bot score"][L], count(p.deck), color=(127, 0, 127))
                else:
                    printc(f"{p.name}: pass", color=(0, 127, 0))
                sleep(PAUSE)
            #player
            elif isinstance(p, Player):
                turn = input(TEXTS["take"][L])
                if is_yes(turn):
                    printc(TEXTS["player take"][L], p.take(deck), color=(255, 0, 255))
                    if SETTINGS["Show points"]: printc(TEXTS["player score"][L], count(p.deck), color=(127, 0, 127))
                    flag = True
        #check if a player lost
        for p in PLAYERS: 
            if p in players and count(p.deck) > SETTINGS["Max points"]:
                printc(TEXTS["loose"][L][0], p.name, TEXTS["loose"][L][1], count(p.deck), color=(255, 0, 0))
                players.remove(p)
    #if noone won
    printc(TEXTS["end"][L], color=(127, 127, 127))
    if len(players) == 0:
        printc(TEXTS["win 0"][L], color=(255, 215, 0))
        continue
    #dealer takes cards
    while count(dealer.deck) < SETTINGS["Dealer min points"]:
        printc(TEXTS["dealer take"][L], dealer.take(deck), color=(0, 255, 255))
        printc(TEXTS["dealer score"][L], count(dealer.deck), color=(0, 127, 127))
        sleep(PAUSE)
    #getting winner
    dealer_score = count(dealer.deck)
    if dealer_score > SETTINGS["Max points"]:
        printc(TEXTS["dealer lost"][L], dealer_score, color=(127, 0, 0))
        for p in players:
            p.won()
            winners.append(p.name)
    for p in players:
        if p > dealer:
            p.won()
            winners.append(p.name)
    #only 1 player won
    if len(winners) == 0:
        printc(TEXTS["win 0"[L]], color=(255, 215, 0))
    if len(winners) == 1:
        printc(winners[0], TEXTS["win 1"][L], color=(255, 215, 0))
    #2+ winners
    else:
        printc(*winners, sep=", ", end=" ", color=(255, 215, 0))
        printc(TEXTS["win 2+"][L], color=(255, 215, 0))
#final results
total_winner = []
for p in PLAYERS:
    if p.get_status()["won"] == SETTINGS["Games to win"]:
        total_winner.append(p.name)

printc(*total_winner, TEXTS["total winner"][L], color=(225, 215, 0))
#statistic
cols = [TEXTS["player"][L], TEXTS["won"][L], TEXTS["lost"][L], TEXTS["played"][L], TEXTS["rate"][L]]
rows = []
values = []
for p in PLAYERS:
    rows.append(p.name)
    stat = p.get_status()
    values.append([stat["won"], stat["lost"], stat["played"], str(stat["rate"])+"%"])

table = Table(cols, rows, values, len(TEXTS["rate"][L]), TEXTS["statistics"][L], (190, 190, 190), (0, 190, 190), (0, 190, 0), (190, 0, 0), (255, 255, 255))
table.print_()

os.system("pause")