import socket
import curses
from communication import Socket
from messagetypes import Name, Game, Turn, CardRow, Claim, Guess
from gametypes import Card
from dacite import from_dict, Config
from enum import Enum
from dataclasses import dataclass
from typing import List, Any


checkmark_code = ' OK'


@dataclass
class HandDisplay:
    items: List[str]
    stdscr: curses.window
    hi_idx: int = 0
    row: int = 5
    claim_idx: int = -1
    offer_idx: int = -1


    def __post_init__(self):
        self.items.extend([checkmark_code])
        self.ok_idx = len(self.items) - 1


    def draw(self):
        self.stdscr.addstr(self.row, 0, 'Hand: ')

        for i,item in enumerate(self.items):
            flags = 0

            if i == self.hi_idx:
                flags |= curses.A_REVERSE

            if i == self.claim_idx == self.offer_idx:
                flags |= curses.color_pair(3)
            elif i == self.claim_idx:
                flags |= curses.color_pair(2)
            elif i == self.offer_idx:
                flags |= curses.color_pair(1)

            self.stdscr.addstr(item + ' ', flags)

    def left(self):
        self.hi_idx = (self.hi_idx - 1) % len(self.items)

    def right(self):
        self.hi_idx = (self.hi_idx + 1) % len(self.items)

    def claim(self):
        if self.hi_idx != self.ok_idx:
            self.claim_idx = self.hi_idx

    def offer(self) -> bool:
        if self.hi_idx == self.ok_idx and self.claim_idx != -1 \
                and self.offer_idx != -1:
            return True
        elif self.hi_idx != self.ok_idx:
            self.offer_idx = self.hi_idx
        return False


@dataclass
class Item:
    label: str
    value: Any


@dataclass
class GuessDisplay:
    stdscr: curses.window
    items: List[Item] = (Item('right', Guess(True)), 
                         Item('wrong', Guess(False)))
    row: int = 6
    hi_idx: int = 0

    def draw(self):
        self.stdscr.addstr(self.row, 0, 'Reponse: ')
        
        for i,item in enumerate(self.items):

            flags = 0

            if i == self.hi_idx:
                flags |= curses.A_REVERSE

            self.stdscr.addstr(item.label + ' ', flags)

    def left(self):
        self.hi_idx = (self.hi_idx - 1) % len(self.items)

    def right(self):
        self.hi_idx = (self.hi_idx + 1) % len(self.items)

    def select(self) -> Guess:
        return self.items[self.hi_idx].value  



def format_row(row: CardRow):
    return [f'{card.creature.code} {card.count}' for card in row.cards]


def make_claim(display: HandDisplay, hand: CardRow) -> Claim:
    actual = hand.cards[display.offer_idx].creature
    claim = hand.cards[display.claim_idx].creature

    return Claim(actual, claim)


def claim_loop(stdscr: curses.window, hand_display: HandDisplay, hand: CardRow) -> Claim:
    while True:
        ch = stdscr.getch()

        if ch == ord('a'):
            hand_display.left()
        elif ch == ord('d'):
            hand_display.right()
        elif ch == ord('w'):
            if hand_display.offer():
                return make_claim(hand_display, hand)
        elif ch == ord('s'):
            hand_display.claim()

        hand_display.draw()
        stdscr.refresh()

    return None


def guess_loop(stdscr: curses.window, guess_display: GuessDisplay, claim: Claim) -> Guess:
    ch = -1

    while ch != ord('w'):
        ch = stdscr.getch()

        if ch == ord('a'):
            guess_display.left()
        elif ch == ord('d'):
            guess_display.right()

        guess_display.draw()
        stdscr.refresh()

    return guess_display.select()
    


def main(stdscr: curses.window):
    client = Socket()
    client.connect('localhost', 7778)
    client.send(Name('Jakob'))

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    stdscr.clear()

    while game := client.recv(Game):

        stdscr.addstr(0,0,'Opponent: ')
        for card in game.opp_board.cards:
            stdscr.addstr(f'{card.creature.code} {card.count} ')

        if game.finished:
            if game.won:
                stdscr.addstr(2,0,'Won!')
            else:
                stdscr.addstr(2,0,'Lost.')
            client.close()
            return

        stdscr.addstr(4,0,'Board: ')
        for card in game.board.cards:
            stdscr.addstr(f'{card.creature.code} {card.count} ')

        guess_display = GuessDisplay(stdscr)
        guess_display.draw()

        hand_display = HandDisplay(format_row(game.hand), stdscr)
        hand_display.draw()

        stdscr.refresh()


        if game.turn == Turn.CLAIM:
            claim = claim_loop(stdscr, hand_display, game.hand)
            client.send(claim)
        elif game.turn == Turn.GUESS:
            opp_claim = client.recv(Claim)
            guess = guess_loop(stdscr, guess_display, opp_claim)
            client.send(guess)
        else:
            raise RuntimeError('Unknown turn type')

        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
