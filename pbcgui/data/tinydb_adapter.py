from contextlib import contextmanager
import functools
from typing import List, Union

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from tinydb.middlewares import CachingMiddleware
from BetterJSONStorage import BetterJSONStorage

from .entities import Game, Player, Rally
from .db_adapter import DatabaseAdapter


@contextmanager
def managed_db(db_path, storage):
    if all((db_path, storage)):
        db = TinyDB(db_path, storage=storage, access_mode='r+')
    else:
        db = TinyDB(storage=MemoryStorage)
    try:
        yield db
    finally:
        db.close()

def with_db(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with managed_db(self.db_path, self.storage) as db:
            return func(self, db, *args, **kwargs)
    return wrapper


class TinyDBAdapter(DatabaseAdapter):
    def __init__(self, db_path=None, storage=None, games_table='games', players_table='players', rallies_table='rallies'):
        self.db_path = db_path
        if db_path is None:
            self.storage = MemoryStorage
        else:
            self.storage = storage if storage else CachingMiddleware(BetterJSONStorage)
        self.games_table = games_table
        self.players_table = players_table
        self.rallies_table = rallies_table

    @with_db
    def connect(self, db):
        return db

    @with_db
    def add_games(self, db, games: List[Game]) -> List[int]:
        table = db.table(self.games_table)
        if isinstance(games, list):
            games = [game.to_dict() for game in games]
        else:
            games = [games.to_dict()]
        return table.insert_multiple(games)

    @with_db
    def get_games(self, db) -> List[Game]:
        table = db.table(self.games_table)
        return table.all()

    @with_db
    def remove_games(self, db, game_guids: Union[str, List[str]]) -> List[int]:
        """Function to remove specific games from the games table."""
        if isinstance(game_guids, str):
            game_guids = [game_guids]

        table = db.table(self.games_table)
        G = Query()

        removed_games = []
        for game_guid in game_guids:
            removed_games.append(table.remove(G.game_guid == game_guid))

        return removed_games

    @with_db
    def remove_all_games(self, db) -> List[int]:
        """Function to remove all rows from the games table."""
        table = db.table(self.games_table)
        return table.truncate()

    @with_db
    def add_players(self, db, players) -> List[int]:
        table = db.table(self.players_table)
        if not players:
            print('TinyDBAdapter: No players to add to database')
            return None
        if isinstance(players, Player):
            #raise ValueError(f'TinyDBAdapter: Invalid players format: {type(players)} {players}')
            p = players.to_dict()
            assert isinstance(p, dict), f'TinyDBAdapter: Invalid players format: {type(players)} {type(p)}'
            return table.insert(p)
        elif all((isinstance(players, list), isinstance(players[0], list))):
            return table.insert_multiple([player.to_dict() for player in players])
        raise ValueError(f'TinyDBAdapter: Invalid players format: {type(players)} {players}')

    @with_db
    def get_players(self, db, names=None, guids=None) -> List[Player]:
        """Get players from the database by name or guid. If no names or guids are provided, return all players."""
        table = db.table(self.players_table)
        if all((names, guids is None)):
            players = table.search(Query().name.one_of(names))
        elif all((names is None, guids)):
            players = table.search(Query().name.one_of(guids))
        else:
            players = table.all()
        return [Player(**player) for player in players]

    @with_db
    def remove_players(self, db, player_guids: Union[str, List[str]]) -> List[int]:
        """Function to remove specific players from the players table."""
        if isinstance(player_guids, str):
            player_guids = [player_guids]

        table = db.table(self.players_table)
        P = Query()

        removed_players = []
        for player_guid in player_guids:
            removed_players.append(table.remove(P.player_guid == player_guid))

        return removed_players

    @with_db
    def add_rallies(self, db, rallies: List[Rally]) -> List[int]:
        table = db.table(self.rallies_table)
        return table.insert_multiple(rallies if isinstance(rallies, list) else [rallies])

    @with_db
    def get_rallies(self, db) -> List[Rally]:
        table = db.table(self.rallies_table)
        return table.all()
    

    @with_db
    def remove_rallies(self, db, rally_guids: Union[str, List[str]]) -> List[int]:
        """Function to remove specific rallies from the rallies table."""
        if isinstance(rally_guids, str):
            rally_guids = [rally_guids]

        table = db.table(self.rallies_table)
        R = Query()

        removed_rallies = []
        for rally_guid in rally_guids:
            removed_rallies.append(table.remove(R.rally_guid == rally_guid))

        return removed_rallies