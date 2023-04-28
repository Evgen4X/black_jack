from data import *
from time import sleep
from random import randint
'''TODO: interface'''
#language
L = 1 if input("Select language: en / pl") == "pl" else 0

#player
player = Player()

#bots
p1 = Bot("Bot 1")
p2 = Bot("Bot 2")
p3 = Bot("Bot 3")

#dealer
dealer = Bot("Dealer")

TIME = 0.5 #pauze
PLAYERS = [player, p1, p2, p3]
n = int(input(texts["1"][L]))

#all games
while all(i.get_status()["won"] < n for i in [player, p1, p2, p3]):
    #score
    printc(texts["total score"][L], color=(127, 0, 0))
    for p in PLAYERS:
        printc(p.name, "-", p.get_status()["won"], color=(255, 0, 0))
    #resets
    for entity in [player, p1, p2, p3, dealer]:
        entity.deck.clear()
        entity.played()
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
    #one game
    while flag: #while at least 1 player took a card
        #move
        flag = False
        for p in players:
            if isinstance(p, Bot):
                if p.think():
                    p.take(deck)
                    flag = True
                    printc(p.name, texts["bot take"][L], color=(0, 255, 0))
                else:
                    printc(f"{p.name}: pass", color=(0, 127, 0))
                sleep(TIME)
            elif isinstance(p, Player):
                turn = input(texts["take"][L])
                if is_yes(turn):
                    printc(texts["player take"][L], p.take(deck), color=(255, 0, 255))
                    printc(texts["player score"][L], count(p.deck), color=(127, 0, 127))
                    flag = True
            if count(p.deck) > 21:
                players.remove(p)
                printc(texts["lost"][L][0], p.name, texts["lost"][L][1], count(p.deck), color=(255, 0, 0))
    printc(texts["end"][L], color=(127, 127, 127))
    if len(players) == 0:
        printc(texts["win 0"][L], color=(255, 215, 0))
        continue
    while count(dealer.deck) < 17:
        printc(texts["dealer take"][L], dealer.take(deck), color=(0, 255, 255))
        printc(texts["dealer score"][L], count(dealer.deck), color=(0, 127, 127))
        sleep(TIME)
    dealer_score = count(dealer.deck)
    if dealer_score > 21:
        printc(texts["dealer lost"][L], dealer_score, color=(127, 0, 0))
        #TODO: fix loosing
        for p in players:
            p.won()
            winners.append(p.name)

    for p in players:
        if p > dealer:
            p.won()
            winners.append(p.name)
    
    if len(winners) == 0:
        printc(texts["win 0"][L], color=(255, 215, 0))
    elif len(winners) == 1:
        printc(winners[0], texts["win 1"][L], color=(255, 215, 0))
    else:
        printc(*winners, sep=", ", end=" ", color=(255, 215, 0))
        printc(texts["win 2+"][L], color=(255, 215, 0))

for p in PLAYERS:
    if p.get_status()["won"] == n:
        total_winner = p.name

printc(total_winner, texts["total winner"][L], color=(225, 215, 0))

printc(texts["statistics"][L], color=(127, 127, 127))
#TODO: table printing
for p in PLAYERS:
    printc(p.name, ":", p.get_status(), color=[randint(100, 255) for _ in range(3)])