from abc import ABC, abstractmethod
from .tinydb_adapter import TinyDBAdapter
from .sqlite_adapter import SQLiteAdapter


class DatabaseAdapter(ABC):
    def __init__(self, db_path=None, games_table='games', players_table='players', rallies_table='rallies'):
        self._db_path = db_path
        self.games_table = games_table
        self.players_table = players_table
        self.rallies_table = rallies_table

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add_games(self, game):
        pass

    @abstractmethod
    def get_games(self):
        pass

    @abstractmethod
    def add_players(self, game):
        pass

    @abstractmethod
    def get_players(self):
        pass

    @abstractmethod
    def add_rallies(self, rallies):
        pass

    @abstractmethod
    def get_rallies(self):
        pass



def database_factory(db_type, **kwargs):
    if db_type == 'tinydb':
        return TinyDBAdapter(**kwargs)
    elif db_type == 'sqlite':
        return SQLiteAdapter(**kwargs)
    else:
        raise ValueError(f"Unknown database type {db_type}")


