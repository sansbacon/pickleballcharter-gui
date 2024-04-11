from dataclasses import dataclass, fields, _MISSING_TYPE, asdict
import datetime
from enum import Enum
import json
from uuid import uuid4


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class ShotOutcomes(Enum):
    WINNER = 1
    CONTINUE = 2
    ERROR_UNFORCED = 3
    ERROR_FORCED = 4


class ShotSides(Enum):
    FOREHAND = 1
    BACKHAND = 2


class ShotTypes(Enum):
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
    teams: dict = None
    final_score: tuple = None
    rallies: dict = None

    def __post_init__(self):
        # Loop through the fields
        for field in fields(self):
            # If there is a default and the value of the field is none we can assign a value
            if not isinstance(field.default, _MISSING_TYPE) and getattr(self, field.name) is None:
                setattr(self, field.name, field.default)

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


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


