from dataclasses import dataclass
from typing import List
from enum import Enum


@dataclass(frozen=True)
class Creature():
    name: str
    code: str


@dataclass
class Card:
    creature: Creature
    count: int = 0


@dataclass
class CardRow:
    cards: List[Card]


@dataclass
class Player:
    board: CardRow
    hand: CardRow


@dataclass
class TotalGame:
    claim_player: int
    player0: Player
    player1: Player

