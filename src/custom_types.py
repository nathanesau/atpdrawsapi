# hack since pytest doesn't like absolute imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

import datetime
from dataclasses import dataclass, field

@dataclass
class Player:
    id: str # the players id from their ATP page (ex. "r0dg")
    name: str # the players name in the draw (ex. "H. Rune")
    order: int # the players order in the draw (ex. 1)

@dataclass
class Matchup:
    player1: Player # the first player in the matchup
    player2: Player # the second player in the matchup
    winner: Player # the winning player in the matchup
    loser: Player # the losing player in the matchup
    order: int # the matchup order in the round (ex. 1)

@dataclass
class Round:
    number: int # the number for the round (ex. 1)
    description: str # the description for the round (ex. R32)
    matchups: list[Matchup] # the list of matchups for the round

@dataclass
class Tournament:
    name: str # the name of the tournament
    category: str # the category of the tournament (ex. 250)
    location: str # the location of the tournament
    start_date: datetime.date # the start date of the tournament
    end_date: datetime.date # the end date of the tournament

@dataclass
class Draw:
    tournament: Tournament
    players: list[Player] = field(default_factory=list) # the players in the draw
    rounds: list[Round] = field(default_factory=list) # the list of rounds for the draw
