import datetime
from pathlib import Path

from tinydb.middlewares import CachingMiddleware
from BetterJSONStorage import BetterJSONStorage

from pbcgui.data import database_factory
from pbcgui.data.entities import Game, Player, Rally

from pathlib import Path
import platformdirs

dirs = platformdirs.user_data_dir("pickleballcharter", "truepickle", ensure_exists=True)
user_data_dir = Path(dirs)
user_data_file = "pbc.db"


FAKE_GAMES = [
    {'game_id': '03a4c2b2-4597-4653-8bd2-306bbca637a7', 'game_date': datetime.datetime(2024, 1, 26, 1, 11, 25), 'game_location': 'Lake Edwin, MD', 'teams': {'A': 'Tiffany Reed', 'B': 'Benjamin Flowers'}, 'final_score': (11, 6), 'rallies': []},
    {'game_id': '2cb3025d-2c07-4648-9ccd-91715d023461', 'game_date': datetime.datetime(2024, 1, 17, 19, 7, 19), 'game_location': 'Christineview, PR', 'teams': {'A': 'Jerome Byrd', 'B': 'Veronica Baker'}, 'final_score': (11, 7), 'rallies': []},
    {'game_id': '0a69f9c0-dacb-4e91-bd3c-f49327518642', 'game_date': datetime.datetime(2024, 4, 7, 21, 44, 28), 'game_location': 'North Jeanetteborough, MN', 'teams': {'A': 'Gregory Hoffman', 'B': 'Claudia Chapman'}, 'final_score': (11, 5), 'rallies': []},
]

PLAYERS = [
    {'first_name': 'Eric', 'last_name': 'Truett'},
    {'first_name': 'Bob', 'last_name': 'Hirsch'},
    {'first_name': 'Gordon', 'last_name': 'Elson'},
    {'first_name': 'Carl', 'last_name': 'Lindberg', 'nickname': 'Sam'},
]


if __name__ == '__main__':
    #pth = Path(__file__).resolve().parent / 'test_pbcdatabase.db'
    #if pth.is_file():
    #    pth.unlink()
    #db = database_factory(db_type='tinydb', db_path=pth, storage=CachingMiddleware(BetterJSONStorage))
    #print(db.add_games(FAKE_GAMES))
    #print(db.get_games())
    
    pth = user_data_dir / user_data_file
    db = database_factory(db_type='tinydb', db_path=pth, storage=CachingMiddleware(BetterJSONStorage))
    #db.remove_all_games()
    #db.add_players(PLAYERS)
    #print(db.get_players())
    print(db.get_games())