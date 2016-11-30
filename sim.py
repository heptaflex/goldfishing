from random import shuffle

class Card:
    def __init__(self, name):
        self.name = name
        self.tapped = False
        self.sickness = True

    def mana(self):
        if self.tapped:
            return []

        if self.name == 'Forest':
            return ['G']
        if self.name == 'Pendelhaven':
            return ['G', 'utility']
        if self.name == 'Breeding Pool':
            return ['G', 'U']
        if self.name == 'Inkmoth Nexus':
            return ['1']
        if self.name == 'Noble Hierarch' and not self.sickness:
            return ['U', 'G', 'W']
        if self.name == 'Birds of Paradise' and not self.sickness:
            return ['U', 'G', 'W', 'R', 'B']

        return []

    def has_infect(self):
        return self.name in [ 'Inkmoth Nexus', 'Glistener Elf', 'Blighted Agent']

    def can_produce_mana(self, color=None):
        # FIXME
        if self.name in [ 'Wooded Foothills', 'Windswept Heath', 'Misty Rainforest']:
            return True
        if color is not None:
            return color in self.mana()
        else:
            return self.mana() != []

class Game:
    def __init__(self, deck):
        self.board = []
        self.library = deck[:]
        self.mulligan = 7
        self.hand = []
        self.graveyard = 0
        self.played = []

    def remove_hand(self, name):
        self.hand.remove(name)

    def on_board(self, name):
        for c in self.board:
            if c.name == name:
                return True
        return False

    def get_on_board(self, name):
        for c in self.board:
            if c.name == name:
                return c

    def in_hand(self, name):
        for c in self.hand:
            if c == name:
                return True
        return False

    def play_from_library(self, name):
        self.library.remove(name)
        self.board.append(Card(name))

    def play_spell(self, name):
        self.hand.remove(name)
        self.graveyard += 1
        self.played.append(name)

    def play(self, name):
        self.hand.remove(name)
        self.board.append(Card(name))

    def draw_hand(self):
        self.library = self.hand + self.library
        shuffle(self.library)
        self.hand = self.library[:self.mulligan]
        self.library = self.library[self.mulligan:]
        self.mulligan -= 1
        return self.hand

    def draw(self):
        self.hand.append(self.library[0])
        self.library = self.library[1:]
        return self.hand[-1]

    def untap(self):
        for card in self.board:
            card.tapped = False
            card.sickness = False

    def can_pay(self, cost):
        used = []
        manas = [ c.mana() for c in self.board ]
        manas = [ m for m in manas if m != [] ]
        manas.sort(key=lambda t: len(t))

        colored_cost = []
        colorless_cost = 0
        for elt in cost:
            if elt not in ['G','W','U','B', 'R']:
                if 'delve' in elt:
                    colorless_cost += max(int(elt[:-5]) - self.graveyard, 0)
                else:
                    colorless_cost += int(elt)
            else:
                colored_cost.append(elt)

        for elt in colored_cost:
            found = None
            for i, n in enumerate(manas):
                if elt in n and i not in used:
                    found = i
                    used.append(i)
                    break
            if found is None:
                return False
            
        available = len([ c for i, c in enumerate(manas) if i not in used ])

        return colorless_cost <= available

    def optimal_pay(self, cost):
        used = []
        manas = [ (c,c.mana()) for c in self.board ]
        manas = [ (c,m) for (c,m) in manas if m != [] ]
        manas.sort(key=lambda t: len(t))

        colored_cost = []
        colorless_cost = 0
        to_delve = 0
        for elt in cost:
            if elt not in ['G','W','U','B', 'R']:
                if 'delve' in elt:
                    base_cost = int(elt[:-5])
                    colorless_cost += min(base_cost - self.graveyard, 0)
                    to_delve = min(self.graveyard, base_cost)
                else:
                    colorless_cost += int(elt)
            else:
                colored_cost.append(elt)
        self.graveyard -= to_delve

        for elt in colored_cost:
            found = None
            for i, n in enumerate(manas):
                if elt in n[1] and i not in used:
                    found = i
                    used.append(i)
                    break

        available = [ c for i, c in enumerate(manas) if i not in used ]

        used = [ manas[i][0] for i in used ]

        for c in available:
            if colorless_cost > 0 and '1' in c[1] and c[0] not in used:
                colorless_cost -= 1
                used.append(c[0])

        for c in available:
            if colorless_cost > 0 and c[0] not in used:
                colorless_cost -= 1
                used.append(c[0])

        for c in used:
            c.tapped = True

    def __str__(self):
        s = ''
        for card in self.board:
            s += card.name[:3] + ('- ' if card.tapped else '  ')
        s += '\nGr%d H: ' % self.graveyard
        s += ' '.join([ card[:3] for card in self.hand ])
        return s

def deck_from_decklist(decklist):
    deck = []
    for count, card in decklist:
        deck += [card] * count
    return deck

def sim_heuristic(decklist, deck_heuristic, heuristic_params={}, ntries=10):
    deck = deck_from_decklist(decklist)
    if len(deck) != 60:
        print('ERROR %d' % len(deck))
        return

    kills = {}
    for loop in range(ntries):
        game = Game(deck)
        t = deck_heuristic(game, **heuristic_params)
        if t is not None:
            if t not in kills:
                kills[t] = 0
            kills[t] += 1

    return kills


