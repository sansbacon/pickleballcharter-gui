from tinydb import TinyDB, Query


class DatabaseHandler:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def create_new_game(self):
        self.db.insert({'type': 'game', 'status': 'new'})

    def read_existing_game(self):
        Game = Query()
        game = self.db.search(Game.type == 'game')
        return game

    # Add more methods for other database operations as needed

