deck = [
    '2♠️', '2♦️', '2♣️', '2♥️',
    '3♠️', '3♦️', '3♣️', '3♥️',
    '4♠️', '4♦️', '4♣️', '4♥️',
    '5♠️', '5♦️', '5♣️', '5♥️',
    '6♠️', '6♦️', '6♣️', '6♥️',
    '7♠️', '7♦️', '7♣️', '7♥️',
    '8♠️', '8♦️', '8♣️', '8♥️',
    '9♠️', '9♦️', '9♣️', '9♥️',
    '10♠️', '10♦️', '10♣️', '10♥️',
    'J♠️', 'J♦️', 'J♣️', 'J♥️',
    'Q♠️', 'Q♦️', 'Q♣️', 'Q♥️',
    'K♠️', 'K♦️', 'K♣️', 'K♥️',
    'A♠️', 'A♦️', 'A♣️', 'A♥️'
]

def unsort(lst:list):
    '''Randomizes order of elements `in list`'''
    from random import choice
    new = lst.copy()
    lst.clear()
    for _ in range(len(new)):
        el = choice(new)
        lst.append(el)
        new.remove(el)

def count(cards:list):
    '''Counts how many points does deck have'''
    aces = 0
    points = 0
    for i in cards:
        i = i[:-2] #removing suit
        if i in "12345678910": points += int(i)
        elif i != "A": points += 10
        else: aces += 1
    if aces == 0: return points
    for i in range(aces):
        if points + 11 <= 21 - aces + 1:
            points += 11
        else:
            points += 1
    return points