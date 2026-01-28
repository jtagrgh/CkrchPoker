from dataclasses import dataclass
from typing import List
from enum import IntEnum, auto
from gametypes import Creature, CardRow


class Turn(IntEnum):
    CLAIM = auto()
    GUESS = auto()


@dataclass
class Name:
    name: str


@dataclass
class Claim:
    actual: Creature
    claim: Creature


@dataclass
class Guess:
    guess: bool


@dataclass
class Game:
    turn: Turn
    opp_board: CardRow
    board: CardRow
    hand: CardRow

