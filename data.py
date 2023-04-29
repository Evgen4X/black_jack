from random import choice

DECK = [
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

texts = {
    "1": ["Games to win", "Liczba gier do końca"],
    "take": ["Take a card? ", "Wziąć kartę? "],
    "lost": [["Player", "lost with score: "], ["Gracz", "przegrał mając punktów: "]],
    "end": ["Game ends. Now dealer takes cards", "Koniec. Krupier bierze karty"],
    "won": ["won!", "wygrał(y)!"],
    "bot take": ["took a card", "wziął kartę"],
    "player take": ["You`ve taken", "Wyciągnąłeś"],
    "player score": ["Your score is:", "Masz punktów:"],
    "dealer take": ["Dealer took", "Krupier wyciągnął"],
    "dealer lost": ["Dealer lost with score:", "Krupier przegrał mając punktów:"],
    "dealer score": ["Dealer`s score is:", "Krupier ma punktów:"],
    "win 0": ["No one won!", "Nikt nie wygrał"],
    "win 1": ["won!", "wygrał!"],
    "win 2+": ["won!", "wygrali!"],
    "total score": ["Total score:", "Podsumowanie:"],
    "total winner": ["won the game!", "Wygrał grę!"],
    "statistics": ["Statistics:", "Ststystyka:"]
}

def printc(*args, sep=" ", end="\n", color=(255, 255, 255)): #GPT
    print(f'\033[38;2;{color[0]};{color[1]};{color[2]}m', end="")
    print(*args, end="", sep=sep)
    print("\033[0m", end=end)

def count(cards:list):
    aces = 0
    points = 0
    for i in cards:
        i = i[:-2]
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

def is_yes(a:str):
    a = a.lower()
    for el in ["ye", "ya", "sure", "oc", "ta"]:
        if el in a:
            return True
    return False

class Player:
    def __init__(self):
        self.deck = list()
        self.status = False
        self._games_won = 0
        self._games_played = 0
        self.name = "Player"
    
    def __gt__(self, other):
        return count(self.deck) > count(other.deck)

    def __lt__(self, other):
        return count(self.deck) < count(other.deck)
    
    def won(self):
        self._games_won += 1
    
    def take(self, global_deck:list):
        el = choice(global_deck)
        self.deck.append(el)
        global_deck.remove(el)
        if count(self.deck) > 21:
            self.status = True
        return el
        
    def new_game(self):
        self.deck.clear()
        self._games_played += 1
        self.status = False
    
    def get_status(self):
        '''
        - games won - `won`
        - games lost - `lost`
        - games played - `played`
        - win rate - `rate`'''
        return {
            'won': self._games_won,
            'lost': self._games_played - self._games_won,
            'played': self._games_played,
            'rate': round(self._games_won / (self._games_played if self._games_played != 0 else 1) * 100, 2)
            }

class Bot(Player):
    def __init__(self, name):
        super().__init__()
        self.moves = -1
        self.name = name

    def count_to_think(self):
        points = 0
        for i in self.deck:
            i = i[:-2]
            if i in '12345687910': points += int(i)
            elif i in 'JQK': points += 10
            else: points += 1
        return points

    def think(self):
        #TODO: add logic
        self.moves += 1
        points = self.count_to_think()
        if points >= 18 or count(self.deck) >= 20:
            return None #pass
        danger = points
        for i in self.deck:
            if count([i]) > 8: danger -= count([i]) * (self.moves // 3 + 1) // 2
        if danger <= points * 4 // 3: return True
