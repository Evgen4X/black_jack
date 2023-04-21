from random import choice

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

class Player:
    '''
    Class of player of the black jack
    Methods
    --------
    - take:
        "hit" - take a random card from the deck
    - is_over:
        check if player lost the game (has more than 21 points)
    '''
    def __init__(self):
        self.deck = list()
        self.lost = False
        self.games_won = 0
        self.games_played = 0
    
    def __gt__(self, other):
        return count(self.deck) > count(other.deck)

    def __lt__(self, other):
        return count(self.deck) < count(other.deck)
    
    def take(self, global_deck:list):
        '''"Hit" - take a random card from the deck'''
        el = choice(global_deck)
        self.deck.append(el)
        global_deck.remove(el)
        if count(self.deck) > 21:
            self.status = True
        
    def new_game(self):
        self.deck.clear()
        self.games_played += 1
        self.lost = False
    
    def get_status(self):
        '''Returns `dict` with:
        - games won - key: `won`
        - games lost - key: `lost`
        - games played - key: `played`
        - win rate - key: `rate`'''
        return {
            'won': self.games_won,
            'lost': self.games_played - self.games_won,
            'played': self.games_played,
            'rate': round(self.games_won / self.games_played * 100, 2)
            }