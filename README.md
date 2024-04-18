# pickleballcharter-gui
GUI desktop application for pickleball charting

# Data Model

```
class Player:
    """Data class for a player"""
    first_name: str
    last_name: str
    nickname: str = None
    gender: str = None
    full_name: str = None
    player_guid: str = str(uuid4())
```

```
class Team:
    """Data class for a team"""
    players: List[Player] = field(default_factory=list)
    score: int = None
    opp_score: int = None
    win: bool = None
```

```
class Shot:
    """Data class for a shot"""
    player_guid: str = None
    shot_type: str = None
    shot_side: str = None
    shot_outcome: str = None
```

```
class Rally:
    """Data class for a rally
    Score is when the rally starts"""
    rally_score: tuple
    rally_winner: str = None
    shots: List[Shot] = field(default_factory=list)
    stack: List[str] = field(default_factory=list)
```

```
class Game:
    """Data class for a game"""
    game_guid: str = str(uuid4())
    game_date: datetime = None
    game_location: str = None
    teams: List[Team] = field(default_factory=list)
    rallies: List[Rally] = field(default_factory=list)
    final_score: tuple = None # always team 1 then team 2
```

# Signals and Slots

* newGameRequested
- member of:
- description: