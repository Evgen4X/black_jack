from random import choice
from colorama import Fore
from os import system

def print_screen(screen):
    system("cls")
    for line in screen:
        print(line, end='')

def printc(*args, sep=" ", end="\n", color="white"):
    end = Fore.RESET + end
    if color == "red":
        print(Fore.RED, end="")
    elif color == "blue":
        print(Fore.BLUE, end="")
    elif color == "green":
        print(Fore.GREEN, end="")
    elif color == "white":
        print(Fore.WHITE, end="")
    elif color == "gray":
        print(Fore.LIGHTBLACK_EX, end="")
    elif color == "yellow":
        print(Fore.YELLOW, end="")
    elif color == "cyan":
        print(Fore.CYAN, end="")
    elif color == "magenta":
        print(Fore.MAGENTA, end="")
    print(*args, sep=sep, end=end)

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
    def __init__(self, name, bot=True):
        self.deck = list()
        self._games_won = 0
        self._games_played = 0
        self.name = name
        self.bot = bot
    
    def __gt__(self, other):
        return count(self.deck) > count(other.deck)
    
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

class Table:
    def __init__(self, columns:list[any], rows:list[any], values:list[list], length, title):
        self.cols = self._tostr(list(columns))
        self.rows = self._tostr(list(rows))
        self.vals = [self._tostr(i) for i in values]
        self.length = length
        self.title = title
        self.n = len(self.cols) * (self.length + 1)

    def _tostr(self, lst:list):
        for i in range(len(lst)):
            lst[i] = str(lst[i])
        return lst

    def _hor(self):
        printc("|", "─"*(self.n-1), "|", sep="", color="white")
    
    def print_(self):
        spaces = (self.n - len(self.title)) // 2
        printc(" "*spaces + self.title, color="cyan")
        self._hor()
        print("|", end="")
        for col in self.cols:
            printc(f"{col:<{self.length}s}", end="|", color="yellow")
        print()
        self._hor()
        for n in range(len(self.rows)):
            print("|", end="")
            printc(f"{self.rows[n]:<{self.length}s}", end="|", color="green")
            for cell in self.vals[n]:
                printc(f"{cell:<{self.length}s}", end="|", color="blue")
            print()
            self._hor()
            self._hor

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
    "play": ["Play/settings: ", "Graj/Ustawienia: "],
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
    "scoreboard": ["     SCOREBOARD\n", "       WYNIKI\n"],
    "exit": ["Press ESC to exit", "Naciśnij ESC, aby zamknąć"],
    "settings": ["To open settings, press SHIFT + CTRL", "Aby otworzyć ustawienia, naciśnij SHIFT + CTRL"],
    "reset": ['Enter setting code to change it\nTo reset settings to defaults, type "reset"', 'Wpisz kod ustawienia, żeby go zmienić\nAby przywrócić do domyślnych ustawień, napisz "reset"'],
    "int value": ["Enter an integer: ", "Podaj liczbę: "],
    "bool value": ["Enter yes/no: ", "Wpisz tak/nie: "],
    "confirm": ['Type "yes" to confirm: ', 'Napisz "tak", aby podtwierdzić: '],
    "code": ["code", "kod"],
    "setting": ["setting", "ustawienie"],
    "value": ["value", "wartość"],
    "default": ["default", "domyślne"],
    "Language": ["Language", "Język"],
    "Games to win": ["Games to win", "Gry do końca"],
    "Dealer min points": ["Dealer min points", "Minimum krupiera"],
    "Max points": ["Max points", "Maximum punktów"],
    "Show points": ["Show points", "Pokazywać punkty"]

}

NAMES = {"Bot 1": 2, "Bot 2": 21, "Bot 3": 19, "Player": 37}
CARDS = {"Bot 1": 6, "Bot 2": 29, "Bot 3": 27, "Player": 40}
SCORES = {"Bot 1": 16, "Bot 2": 24, "Bot 3": 32, "Player": 12}

SCREEN = [
"|                                   BLACK JACK                               |\n",
"|                                  ","Bot 1","                                     |", "     SCOREBOARD\n",
"|                                  ","","                                          |", "   Player  ", "Score\n", 
"|                                                                            |", "   You", "       0", "\n", #set score
"|                                                                            |", "   Bot 1", "     0", "\n", #set score
"|              ","Bot 3","                                      ","Bot 2","              |", "   Bot 2", "     0", "\n", #set score
"|            ","","                                               ","","                 |", "   Bot 3", "     0", "\n", #set score
"|                                                                            |\n",
"|                                                                            |\n",
"|                                 ","Player (you)","                               |\n", 
"|                                 ","","                                           |\n", 
"|                                     ","","                                       |\n", #43
"|                                                                            |\n",
"|                                                                            |\n",
"|____________________________________________________________________________|\n"
]