from data import *
from time import sleep
from random import choice
import os
from keyboard import add_hotkey
from json import load

def exit_():
    os.startfile("start.py")
    exit()

'''TODO: interface'''
#settings
with open("database.json", "r", encoding="utf-8") as file:
    SETTINGS = load(file)

#language
L = 0 if SETTINGS["Language"] == "en" else 1

#hotkeys
add_hotkey("Esc", exit_)

#player
player = Player("Player", False)

#bots
p1 = Player("Bot 1")
p2 = Player("Bot 2")
p3 = Player("Bot 3")

#dealer
dealer = Player("Dealer")

PAUSE = 0.44 #pause
PLAYERS = [p1, p2, player, p3]
scr = SCREEN.copy()

#all games
while all(i.get_status()["won"] < SETTINGS["Games to win"] for i in [player, p1, p2, p3]):
    #reset
    for p in PLAYERS:
        p.new_game()
        scr[SCORES[p.name]] = scr[SCORES[p.name]][:-1] + str(p.get_status()["won"])
    scr[4] = TEXTS["scoreboard"][L]
    dealer.new_game()
    screen = scr.copy()
    deck = DECK.copy()
    flag = True
    winners = list()
    players = PLAYERS.copy()
    #a game round
    while flag and players:
        os.system("cls")
        flag = False
        for p in players:
            print_screen(screen)
            #bots
            if p.bot:
                if count(p.deck) < 18:
                    p.take(deck)
                    flag = True
                    screen[CARDS[p.name]] = "█ " * len(p.deck)
                    screen[CARDS[p.name] + 1] = screen[CARDS[p.name] + 1][2:]
                else:
                    screen[NAMES[p.name]] = Fore.LIGHTBLACK_EX + screen[NAMES[p.name]] + Fore.RESET
                sleep(PAUSE)
            #player
            else:
                turn = input(TEXTS["take"][L])
                if is_yes(turn):
                    card = p.take(deck)
                    screen[CARDS["Player"]] = screen[CARDS["Player"]] + card
                    screen[CARDS["Player"] + 1] = screen[CARDS["Player"] + 1][len(card):]
                    flag = True
                    if SETTINGS["Show points"]:
                        screen[43] = count(p.deck)
                        screen[44] = SCREEN[44][len(str(count(p.deck))):]

        #check if a player lost
        for p in PLAYERS: 
            if p in players and count(p.deck) > SETTINGS["Max points"]:
                printc(TEXTS["loose"][L][0], p.name, TEXTS["loose"][L][1], count(p.deck), color="red")
                screen[NAMES[p.name]] = Fore.RED + screen[NAMES[p.name]] + Fore.RESET
                players.remove(p)
    #if noone won
    printc(TEXTS["end"][L])
    if len(players) == 0:
        printc(TEXTS["win 0"][L], color="yellow")
        sleep(PAUSE * 3)
        continue
    #dealer takes cards
    while count(dealer.deck) < SETTINGS["Dealer min points"]:
        printc(TEXTS["dealer take"][L], dealer.take(deck), color="cyan")
        printc(TEXTS["dealer score"][L], count(dealer.deck), color="magenta")
        sleep(PAUSE + 0.2)
    #getting winner
    dealer_score = count(dealer.deck)
    if dealer_score > SETTINGS["Max points"]:
        printc(TEXTS["dealer lost"][L], dealer_score, color="red")
        for p in players:
            p.won()
            winners.append(p.name)
    for p in players:
        if p > dealer:
            p.won()
            winners.append(p.name)
    #only 1 player won
    if len(winners) == 0:
        printc(TEXTS["win 0"][L], color="yellow")
    elif len(winners) == 1:
        printc(winners[0], TEXTS["win 1"][L], color="yellow")
    #2+ winners
    else:
        printc(*winners, sep=", ", end=" ", color="yellow")
        printc(TEXTS["win 2+"][L], color="yellow")
    
    sleep(PAUSE * 3)
#final results
total_winner = []
for p in PLAYERS:
    if p.get_status()["won"] == SETTINGS["Games to win"]:
        total_winner.append(p.name)

os.system("cls")
printc(*total_winner, TEXTS["total winner"][L], color="red")
#statistic
cols = [TEXTS["player"][L], TEXTS["won"][L], TEXTS["lost"][L], TEXTS["played"][L], TEXTS["rate"][L]]
rows = []
values = []
for p in PLAYERS:
    rows.append(p.name)
    stat = p.get_status()
    values.append([stat["won"], stat["lost"], stat["played"], str(stat["rate"])+"%"])

table = Table(cols, rows, values, len(TEXTS["rate"][L]), TEXTS["statistics"][L])
table.print_()

os.system("pause")

os.startfile("start.py")
exit()