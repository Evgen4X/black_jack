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

TEXTS = {
    "take": ["Take a card? ", "Wziąć kartę? "],
    "loose": [["Player", "lost with score: "], ["Gracz", "przegrał mając punktów: "]],
    "end": ["Game ends. Now dealer takes cards", "Koniec. Krupier bierze karty"],
    "won": ["won!", "wygrał(y)!"],
    "bot take": ["took a card", "wziął kartę"],
    "bot score": ["has points:", "ma punktów:"],
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
    "statistics": ["Statistics:", "Ststystyka:"],
    "player": ["Player", "Gracz"],
    "won": ["won", "wygrano"],
    "lost": ["lost", "przegrano"],
    "played": ["played", "zagrane"],
    "rate": ["winning rate", "procent wygranych"],
    "exit": ["Press ESC to exit", "Naciśnij ESC, aby zamknąć"],
    "settings": ["To open settings, press SHIFT + CTRL", "Aby otworzyć ustawienia, naciśnij SHIFT + CTRL"],
    "changed": ["Settings changed. Press CTRL + Q in game file to apply", "Ustawienia zmienione. Naciśnij CTRL + Q w pliku z grą, aby zastosować"],
    "reset": ['Enter setting code to change it\nTo reset settings to defaults, type "reset"', 'Wpisz kod ustawienia, żeby go zmienić\nAby przywrócić do domyślnych ustawień, napisz "reset"'],
    "int value": ["Enter an integer: ", "Podaj liczbę: "],
    "bool value": ["Enter yes/no: ", "Wpisz tak/nie: "],
    "confirm": ['Type "yes" to confirm: ', 'Napisz "tak", aby podtwierdzić: ']
}
#ChatGPT
def printc(*args, sep=" ", end="\n", color=(255, 255, 255)): #ChatGPT
    print(f'\033[38;2;{color[0]};{color[1]};{color[2]}m', end="") #ChatGPT
    print(*args, end="", sep=sep) #ChatGPT
    print("\033[0m", end=end) #ChatGPT

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
    for el in ["ye", "ta", "true", "1"]:
        if el in a:
            return True
    return False

class Player:
    def __init__(self):
        self.deck = list()
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

class Table:
    def __init__(self, columns:list[any], rows:list[any], values:list[list], length, title, titlec, colc, rowc, valc, linec):
        self.cols = self._tostr(list(columns))
        self.rows = self._tostr(list(rows))
        self.vals = [self._tostr(i) for i in values]
        self.length = length
        self.title = title
        self.n = len(self.cols) * (self.length + 1)
        self.titlec = titlec
        self.colc = colc
        self.rowc = rowc
        self.valc = valc
        self.linec = linec

    def _tostr(self, lst:list):
        for i in range(len(lst)):
            lst[i] = str(lst[i])
        return lst

    def _hor(self):
        printc("─"*self.n, color=self.linec)
    
    def print_(self):
        spaces = max(0, (self.n - len(self.title)) // 2)
        printc(" "*spaces + self.title, color=self.titlec)
        self._hor()
        print("|", end="")
        for col in self.cols:
            printc(f"{col:<{self.length}s}", end="|", color=self.colc)
        print()
        self._hor()
        for n in range(len(self.rows)):
            print("|", end="")
            printc(f"{self.rows[n]:<{self.length}s}", end="|", color=self.rowc)
            for cell in self.vals[n]:
                printc(f"{cell:<{self.length}s}", end="|", color=self.valc)
            print()
            self._hor()
            self._hor