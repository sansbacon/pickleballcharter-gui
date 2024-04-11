import datetime
from itertools import chain

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from tinydb.middlewares import CachingMiddleware
from BetterJSONStorage import BetterJSONStorage

from .entities import Game


class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self._fake_data = [
            {'game_id': '03a4c2b2-4597-4653-8bd2-306bbca637a7', 'game_date': datetime.datetime(2024, 1, 26, 1, 11, 25), 'game_location': 'Lake Edwin, MD', 'teams': {'A': 'Tiffany Reed', 'B': 'Benjamin Flowers'}, 'final_score': (11, 6), 'rallies': []},
            {'game_id': '2cb3025d-2c07-4648-9ccd-91715d023461', 'game_date': datetime.datetime(2024, 1, 17, 19, 7, 19), 'game_location': 'Christineview, PR', 'teams': {'A': 'Jerome Byrd', 'B': 'Veronica Baker'}, 'final_score': (11, 7), 'rallies': []},
            {'game_id': '0a69f9c0-dacb-4e91-bd3c-f49327518642', 'game_date': datetime.datetime(2024, 4, 7, 21, 44, 28), 'game_location': 'North Jeanetteborough, MN', 'teams': {'A': 'Gregory Hoffman', 'B': 'Claudia Chapman'}, 'final_score': (11, 5), 'rallies': []},
            {'game_id': 'a88732d7-9ba4-4b5a-bce9-138a2dd424fb', 'game_date': datetime.datetime(2024, 3, 5, 5, 48, 50), 'game_location': 'Port Davidberg, AR', 'teams': {'A': 'Samantha Leonard', 'B': 'Rodney Riddle'}, 'final_score': (11, 7), 'rallies': []},
            {'game_id': 'c786c271-442a-4467-a6fb-141d9f0e873d', 'game_date': datetime.datetime(2024, 2, 19, 19, 31, 21), 'game_location': 'Laurahaven, SC', 'teams': {'A': 'Glenda Morrison', 'B': 'Samuel Bennett'}, 'final_score': (11, 5), 'rallies': []},
            {'game_id': '2261e8ab-d819-4901-bc8b-0347f2298c06', 'game_date': datetime.datetime(2024, 2, 20, 14, 30, 3), 'game_location': 'Arroyoside, LA', 'teams': {'A': 'Anita Carr', 'B': 'Thomas Howard'}, 'final_score': (11, 3), 'rallies': []},
            {'game_id': '65c1e74b-89b5-441f-82ed-056020d9bcf3', 'game_date': datetime.datetime(2024, 3, 26, 2, 57, 7), 'game_location': 'New Tyler, UT', 'teams': {'A': 'Chad Robinson', 'B': 'Roy Berry'}, 'final_score': (11, 3), 'rallies': []},
            {'game_id': '2d8c2a06-dcc2-4885-8732-672fcc80d740', 'game_date': datetime.datetime(2024, 1, 3, 21, 29), 'game_location': 'South Sarahshire, OH', 'teams': {'A': 'Frederick Carey', 'B': 'Brad Nelson'}, 'final_score': (11, 2), 'rallies': []},
            {'game_id': '9ebc311f-213a-47c1-8658-bad8fb09002f', 'game_date': datetime.datetime(2024, 2, 5, 3, 21, 50), 'game_location': 'North Carlstad, AR', 'teams': {'A': 'Michael Ramirez', 'B': 'Jerry Strong'}, 'final_score': (11, 6), 'rallies': []},
            {'game_id': '8c98b937-87de-416d-8547-a1293a6f5705', 'game_date': datetime.datetime(2024, 1, 17, 11, 34, 59), 'game_location': 'Jamesburgh, GA', 'teams': {'A': 'Thomas Steele', 'B': 'Amy Mckenzie'}, 'final_score': (11, 1), 'rallies': []},
        ]

    def create_fake_games(self):
        """Creates fake game data for testing purposes"""
        with TinyDB(self.db_path, access_mode="r+", storage=CachingMiddleware(BetterJSONStorage)) as db:
            for item in self._fake_data:
                keys = ['game_id', 'game_date', 'game_location', 'teams']
                db.insert({key: item[key] for key in keys})

    def get_all(self):
        with TinyDB(self.db_path, access_mode="r", storage=CachingMiddleware(BetterJSONStorage)) as db:
            return db.all()


class GamesDb (DatabaseHandler):
    """Database handler for games database"""
    def get_games(self):
        return self.get_all()

    def get_players(self):
        with TinyDB(self.db_path, access_mode="r", storage=CachingMiddleware(BetterJSONStorage)) as db:
            players = chain.from_iterable([game['teams'].values() for game in db.all()])
            return sorted(set(players))

    def insert_game(self, game: Game):
        with TinyDB(self.db_path, access_mode="r+", storage=CachingMiddleware(BetterJSONStorage)) as db:
            db.insert(game.to_dict())
        
    

class ChartDb (DatabaseHandler):
    """Database handler for chart database"""
    def load_rallies(self):
        pass