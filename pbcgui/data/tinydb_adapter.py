from contextlib import contextmanager
import functools
from typing import List

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
        self.storage = storage
        self.games_table = games_table
        self.players_table = players_table
        self.rallies_table = rallies_table

    @with_db
    def connect(self, db):
        return db

    @with_db
    def add_games(self, db, games: List[Game]) -> List[int]:
        table = db.table(self.games_table)
        return table.insert_multiple(games)

    @with_db
    def get_games(self, db) -> List[Game]:
        table = db.table(self.games_table)
        return table.all()

    @with_db
    def add_players(self, db, players: List[Player]) -> List[int]:
        table = db.table(self.players_table)
        return table.insert_multiple(players)

    @with_db
    def get_players(self, db) -> List[Player]:
        table = db.table(self.players_table)
        return table.all()
    
    @with_db
    def add_rallies(self, db, rallies: List[Rally]) -> List[int]:
        table = db.table(self.rallies_table)
        return table.insert_multiple(rallies)

    @with_db
    def get_rallies(self, db) -> List[Rally]:
        table = db.table(self.rallies_table)
        return table.all()
    