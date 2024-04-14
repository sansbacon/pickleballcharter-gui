from .tinydb_adapter import TinyDBAdapter
from .sqlite_adapter import SQLiteAdapter
from .entities import *


def database_factory(db_type, db_path=None, **kwargs):
    if db_type == 'tinydb':
        return TinyDBAdapter(db_path, **kwargs)
    elif db_type == 'sqlite':
        return SQLiteAdapter(db_path, **kwargs)
    else:
        raise ValueError(f"Unknown database type {db_type}")

