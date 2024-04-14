from pbcgui.config import user_data_dir
from pbcgui.data.db import *

def get_games(db_dir):
    """Gets games from the database"""
    db = GamesDb(db_dir)
    return db.get_games()


if __name__ == '__main__':
    gamesdb = 'games.db'
    chartsdb = 'charts.db'
    gamesdb_path = user_data_dir / gamesdb
    with TinyDB(gamesdb_path, access_mode="r", storage=CachingMiddleware(BetterJSONStorage)) as db:
        print(db.get(doc_id=3))
    