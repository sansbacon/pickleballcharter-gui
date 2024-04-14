from dataclasses import dataclass, fields, _MISSING_TYPE, asdict
import datetime
from enum import Enum
import json
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
class Game:
    """Data class for a game"""
    game_id: str = str(uuid4())
    game_date: datetime = None
    game_location: str = None
    players: list = None
    final_score: tuple = None # always team 1 then team 2
    rallies: dict = None
    winner: bool = None

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

    def to_dict(self):
        d = asdict(self)
        d['teams'] = self.teams()
        return d

    def teams(self):
        return {'A': self.players[0:2], 'B': self.players[2:]}

    def winner(self):
        if not self.final_score:
            return None
        return 'A' if self.final_score[0] > self.final_score[1] else 'B'

dataclass
class Player:
    """Data class for a player"""
    player_id: int
    first_name: str
    last_name: str
    nickname: str
    gender: str


    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


@dataclass
class Rally:
    """Data class for a rally"""
    rally_id: int
    rally_score: tuple
    shots: list
    rally_winner: int
    stack: list

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

dataclass
class Shot:
    """Data class for a shot"""
    player_id: int
    team_id: int
    shot_type: str

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)


