from contextlib import contextmanager
from typing import List

import sqlite3
from .entities import Game, Player, Rally
from .db_adapter import DatabaseAdapter


@contextmanager
def managed_db(db_path, **kwargs):
    if db_path == ':memory:':
        db = sqlite3.connect(':memory:')
    else:
        db = sqlite3.connect(db_path, **kwargs)
    try:
        yield db
    finally:
        db.close()

def with_db(func):
    def wrapper(self, *args, **kwargs):
        with managed_db(self.db_path) as db:
            return func(self, db, *args, **kwargs)
    return wrapper


class SQLiteAdapter(DatabaseAdapter):
    def __init__(self, db_path=None, storage=None, games_table='games', players_table='players', rallies_table='rallies'):
        self._db_path = db_path
        self.storage = storage
        self.games_table = games_table
        self.players_table = players_table
        self.rallies_table = rallies_table

    @with_db
    def connect(self, db):
        return db

    @with_db
    def add_games(self, db, games: List[Game]) -> List[int]:
        pass
        #table = db.table(self.games_table)
        #return table.insert_multiple(games)

    @with_db
    def get_games(self, db) -> List[Game]:
        pass
        #table = db.table(self.games_table)
        #return table.all()

    @with_db
    def add_players(self, db, players: List[Player]) -> List[int]:
        pass
        #table = db.table(self.players_table)
        #return table.insert_multiple(players)

    @with_db
    def get_players(self, db) -> List[Player]:
        pass
        #table = db.table(self.players_table)
        #return table.all()
    
    @with_db
    def add_rallies(self, db, rallies: List[Rally]) -> List[int]:
        pass
        #table = db.table(self.rallies_table)
        #return table.insert_multiple(rallies)

    @with_db
    def get_rallies(self, db) -> List[Rally]:
        pass
        #table = db.table(self.rallies_table)
        #return table.all()
    
