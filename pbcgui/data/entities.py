from dataclasses import dataclass, fields, _MISSING_TYPE, asdict
import datetime
from enum import Enum
import json
from typing import List
from uuid import uuid4


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def find(cls, to_find):
        for item in cls:
            if item.value == to_find:
                return item.name, item.value
        return None


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class ShotOutcomes(ExtendedEnum):
    WINNER = 1
    CONTINUE = 2
    ERROR_UNFORCED = 3
    ERROR_FORCED = 4


class ShotSides(ExtendedEnum):
    FOREHAND = 1
    BACKHAND = 2


class ShotTypes(ExtendedEnum):
    SERVE = 1
    RETURN = 2
    DROP = 3
    DRIVE = 4
    ROLL_VOLLEY = 5
    PUNCH_VOLLEY = 6
    DINK_AIR = 7
    DINK_BOUNCE = 8
    ATTACK_AIR = 9
    ATTACK_BOUNCE = 10
    RESET = 11
    COUNTER = 12
    ERNE = 13
    LOB = 14
    PUTAWAY = 15


@dataclass
class Player:
    """Data class for a player"""
    player_name: str
    player_guid: str = str(uuid4())

    def to_dict(self):
        return asdict(self)


@dataclass
class Shot:
    """Data class for a shot"""
    player_guid: str
    shot_type: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Rally:
    """Data class for a rally
    Score is when the rally starts"""
    rally_score: tuple
    shots: List[Shot]
    rally_winner: str
    stack: List[str]

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

    def to_dict(self):
        return {
            "rally_score": self.rally_score,
            "shots": [shot.to_dict() for shot in self.shots],
            "rally_winner": self.rally_winner,
            "stack": self.stack
        }


@dataclass
class Game:
    """Data class for a game"""
    game_guid: str = str(uuid4())
    game_date: datetime = None
    game_location: str = None
    players: List[Player] = None
    rallies: List[Rally] = None
    final_score: tuple = None # always team 1 then team 2

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

    def to_dict(self):
        return {
            "game_guid": self.game_guid,
            "game_date": self.game_date,
            "game_location": self.game_location,
            "players": [player.to_dict() for player in self.players],
            "rallies": [rally.to_dict() for rally in self.rallies],
            "final_score": self.final_score
        }
