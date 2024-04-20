from dataclasses import dataclass, field, asdict
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


class ShotLocations(ExtendedEnum):
    LEFT_OUTER = 1
    LEFT_INNER = 2
    CENTER = 3
    RIGHT_INNER = 4
    RIGHT_OUTER = 5


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
    first_name: str
    last_name: str
    nickname: str = None
    gender: str = None
    full_name: str = None
    player_guid: str = None

    def __post_init__(self):
        if not self.full_name:
            name = f'{self.first_name} {self.last_name}'
            if self.nickname:
                name += f' ({self.nickname})'
            self.full_name = name
        if not self.player_guid:
            self.player_guid = str(uuid4())

    def to_dict(self):
        return asdict(self)
        
@dataclass
class Team:
    """Data class for a team"""
    players: List[Player] = field(default_factory=list)
    score: int = None
    opp_score: int = None
    win: int = None

    def __post_init__(self):
        if not self.win:
            try:
                self.win = int(self.score > self.opp_score)
            except TypeError:
                pass

    def to_dict(self):
        return asdict(self)


@dataclass
class Shot:
    """Data class for a shot"""
    player_guid: str = None
    shot_type: str = None
    shot_side: str = None
    shot_outcome: str = None
    shot_location: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Score:
    """Data class for a score"""
    server_score: int = None
    returner_score: int = None
    server_number: int = None
    serving_team: int = None

    def score_tuple(self):
        return (self.server_score, self.returner_score, self.server_number)

    def to_dict(self):
        return asdict(self)

@dataclass
class Rally:
    """Data class for a rally
    Score is when the rally starts"""
    rally_score: Score = None
    rally_winner: str = None
    shots: List[Shot] = field(default_factory=list)
    stack: List[str] = field(default_factory=list)

    def player_shots(self):
        d = {}
        for shot in self.shots:
            if shot.player_guid not in d:
                d[shot.player_guid] = []
            d[shot.player_guid].append(shot)

    def to_dict(self):
        return {
            "rally_score": self.rally_score.to_dict(),
            "shots": [shot.to_dict() for shot in self.shots],
            "rally_winner": self.rally_winner,
            "stack": self.stack
        }


@dataclass
class Game:
    """Data class for a game"""
    game_guid: str = None
    game_date: str = None
    game_location: str = None
    teams: List[Team] = field(default_factory=list)
    rallies: List[Rally] = field(default_factory=list)
    final_score: tuple = None # always team 1 then team 2

    def __post_init__(self):
        if not self.game_guid:
            self.game_guid = str(uuid4())

    def players(self):
        return [player for team in self.teams for player in team.players]

    def player_shots(self):
        shots = self.shots()
        return {
            player.player_guid: [shot for shot in shots if shot.player_guid == player.player_guid]
            for player in self.players()
        }
    
    def rally_count(self):
        return len(self.rallies)

    def score_states(self):
        return [rally.rally_score for rally in self.rallies]

    def shot_count(self):
        return sum([len(rally.shots) for rally in self.rallies])

    def shots(self):
        l = []
        for rally in self.rallies:
            l.extend(rally.shots)
        return l
    
    def to_dict(self):
        return {
            "game_guid": self.game_guid,
            "game_date": self.game_date,
            "game_location": self.game_location,
            "teams": [team.to_dict() for team in self.teams],
            "rallies": [rally.to_dict() for rally in self.rallies],
            "final_score": self.final_score
        }

    def winner(self):
        if any((not self.final_score, not self.final_score[0], not self.final_score[1])):
            return None
        return int(self.final_score[0] < self.final_score[1])
            
    def winning_team(self):
        if not self.winner():
            return None
        return self.teams[self.winner()]