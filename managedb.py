from pathlib import Path

import click
import platformdirs

from pbcgui.data import database_factory
from pbcgui.data.entities import Game, Player, Rally


dirs = platformdirs.user_data_dir("pickleballcharter", "truepickle", ensure_exists=True)
user_data_dir = Path(dirs)
user_data_file = "pbc.db"
db = database_factory(db_type='tinydb', db_path=user_data_dir / user_data_file)


def _delete_games(game_ids=None):
    if game_ids:
        print(f'Remove_games: {game_ids=}')
        db.remove_games(game_ids)
    else:
        print(f'Remove all games: {game_ids=}')
        db.remove_all_games()


def _dump_games(game_ids=None):
    if game_ids:
        print(f'Dump_games: {game_ids=}')
        print(db.get_games(game_ids))
    else:
        print(f'Dump all games: {game_ids=}')
        print(db.get_games())


def _delete_players(game_ids=None):
    if game_ids:
        print(f'Remove_players: {game_ids=}')
        #db.remove_players(game_ids)
    else:
        print(f'Remove all players: {game_ids=}')
        #db.remove_all_players()


def _dump_players(player_ids=None):
    if player_ids:
        print(f'Dump_players: {player_ids=}')
        print(db.get_players(player_ids))
    else:
        print(f'Dump all players: {player_ids=}')
        print(db.get_players())

@click.group()
def cli():
    pass

@cli.command(help='Delete specific games by game_id')
@click.argument('game_ids', nargs=-1)
def delete_games(game_ids):
    _delete_games(game_ids)


@cli.command(help='Dump games by game_id')
@click.argument('game_ids', nargs=-1)
def dump_games(game_ids):
    _dump_games(game_ids)


@cli.command(help='Delete specific players by player_id')
@click.argument('player_ids', nargs=-1)
def delete_players(player_ids):
    _delete_players(player_ids)


@cli.command(help='Dump players by player_id')
@click.argument('player_ids', nargs=-1)
def dump_players(player_ids):
    _dump_players(player_ids)


if __name__ == '__main__':
    cli()
