```
class Player:
    """Data class for a player"""
    first_name: str
    last_name: str
    nickname: str 
    gender: str 
    full_name: str 
    player_guid: str = str(uuid4())
```

```
class Team:
    """Data class for a team"""
    players: List[Player] 
    score: int
    opp_score: int
    win: int
```

```
class Shot:
    """Data class for a shot"""
    player_guid: str 
    shot_type: str 
    shot_side: str 
    shot_outcome: str 
```

```
class Rally:
    """Data class for a rally
    Score is when the rally starts"""
    rally_score: tuple
    rally_winner: str 
    shots: List[Shot]
    stack: List[str]
```

```
class Game:
    """Data class for a game"""
    game_guid: str = str(uuid4())
    game_date: datetime 
    game_location: str 
    teams: List[Team]
    rallies: List[Rally]
    final_score: tuple # always team 1 then team 2
```