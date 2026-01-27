import curses

class Bug:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

caterpiller = Bug('caterpiller', '\U0001F41B')
ladybug = Bug('ladybug', '\U0001F41E')
scorpion = Bug('scorpion', '\U0001F982')
bat = Bug('bat', '\U0001F987')
mouse = Bug('mouse', '\U0001F42D')
cricket = Bug('cricket', '\U0001F41C')
frog = Bug('frog', '\U0001F438')
spider = Bug('spider', '\U0001F577')
error = Bug('error', 'X')

class Card:
    def __init__(self, bug=error, count=0):
        self.bug = bug
        self.count = count


class Hand:
    def __init__(self, cards=[], hover_idx=0, card_idx=-1, claim_idx=-1):
        self.cards = cards
        self.hover_idx = hover_idx
        self.card_idx = card_idx
        self.claim_idx = claim_idx
    
    def draw(self, stdscr: curses.window):
        for i,card in enumerate(self.cards):
            flags = 0
            if i == self.card_idx == self.claim_idx:
                flags |= curses.color_pair(3)
            elif i == self.card_idx:
                flags |= curses.color_pair(1)
            elif i == self.claim_idx:
                flags |= curses.color_pair(2)
            if i == self.hover_idx:
                flags |= curses.A_REVERSE 
            stdscr.addstr(f' {card.bug.code} ', flags)
        stdscr.addstr(' ', flags)

    def hover_right(self):
        self.hover_idx = (self.hover_idx + 1) % len(self.cards)

    def hover_left(self):
        self.hover_idx = (self.hover_idx - 1) % len(self.cards)

    def select_card(self):
        self.card_idx = self.hover_idx

    def select_claim(self):
        self.claim_idx = self.hover_idx


def main(stdscr: curses.window):
    cards = [Card(caterpiller), Card(ladybug), Card(scorpion), Card(bat), 
                Card(mouse), Card(cricket), Card(frog), Card(spider)]
    hand = Hand(cards)
    debug = False 

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    stdscr.clear()

    while True:
        stdscr.move(0,0)
        hand.draw(stdscr)

        if debug:
            stdscr.addstr(2, 0, f'hoever_idx: {hover_idx} ')
            stdscr.addstr(f'card_idx: {card_idx} ')

        stdscr.refresh()
        ch = stdscr.getch()

        if ch == ord('d'):
            hand.hover_right()
        elif ch == ord('a'):
            hand.hover_left()
        elif ch == ord('w'):
            hand.select_card()
        elif ch == ord('s'):
            hand.select_claim()
        elif ch == ord('q'):
            return

curses.wrapper(main)