from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


class DatabaseHandler:
    def __init__(self, db_path):
        if db_path:
            self.db = TinyDB(db_path)
        else:
            self.db = TinyDB(storage=MemoryStorage)

    def create_new_game(self):
        self.db.insert({'type': 'game', 'status': 'new'})

    def read_existing_game(self):
        Game = Query()
        game = self.db.search(Game.type == 'game')
        return game
