import random
import pytest

from pbcgui.data import *
from pbcgui.utility import score_to_string, string_to_score

@pytest.fixture
def get_players():
    return [
        Player(player_guid='p1', first_name='Carl', last_name='Lindberg', nickname='JimBob'),
        Player(player_guid='p2', first_name='Eric', last_name='Truett', nickname=''),
        Player(player_guid='p3', first_name='Rich', last_name='Swanson', nickname='Tricky Ricky'),
        Player(player_guid='p4', first_name='Gordon', last_name='Elson', nickname='')
    ]


@pytest.fixture
def get_shots(get_players):
    return [
        Shot(player_guid=get_players[random.randint(0, 3)].player_guid,
             shot_type=random.choice(list(ShotTypes)).value,
             shot_side=random.choice(list(ShotSides)).value,
             shot_outcome=random.choice(list(ShotOutcomes)).value)
        for _ in range(10)
    ]


## player
def test_player_full_name():
    p = Player(first_name='Eric', last_name='Truett')
    assert p.full_name == 'Eric Truett'
    p = Player(first_name='Eric', last_name='Truett', nickname='JimBob')
    assert p.full_name == 'Eric Truett (JimBob)'

def test_player_to_dict():
    p = Player(first_name='Eric', last_name='Truett', nickname='JimBob')
    player_dict = p.to_dict()
    assert isinstance(player_dict, dict), 'Player.to_dict() should return a dict'
    assert player_dict['first_name'] == 'Eric'
    assert player_dict['last_name'] == 'Truett'
    assert player_dict['nickname'] == 'JimBob'

## team
def test_team_to_dict(get_players):
    """Test the Team.to_dict() method"""
    t = Team(players=random.sample(get_players, 2))
    team_dict = t.to_dict()
    assert isinstance(team_dict, dict), 'Team.to_dict() should return a dict'
    assert len(team_dict['players']) == 2

def test_team_methods(get_players):
    """Test the Team properties"""
    t = Team(players=random.sample(get_players, 2), score=9, opp_score=11)
    assert len(t.players) == 2
    assert t.score == 9
    assert t.opp_score == 11
    assert t.win == 0

    t = Team(players=random.sample(get_players, 2), score=11, opp_score=9)
    assert len(t.players) == 2
    assert t.score == 11
    assert t.opp_score == 9
    assert t.win == 1

## shots

def test_shot_to_dict():
    s = Shot(
        player_guid='p1', 
        shot_type='SERVE', 
        shot_side='Forehand', 
        shot_outcome='Continue'
    )
    
    shot_dict = s.to_dict()
    assert isinstance(shot_dict, dict), 'Shot.to_dict() should return a dict'
    assert shot_dict['player_guid'] == 'p1'
    assert shot_dict['shot_type'] == 'SERVE'
    assert shot_dict['shot_side'] == 'Forehand'
    assert shot_dict['shot_outcome'] == 'Continue'


## rally
def test_rally_to_dict(get_shots):
    """"Tests the Rally.to_dict() method"""
    r = Rally(rally_score=(0, 0), shots=get_shots)
    rally_dict = r.to_dict()
    assert isinstance(rally_dict, dict), 'Rally.to_dict() should return a dict'
    assert len(rally_dict['shots']) == 10


## game
def test_game_to_dict(get_players, get_shots):
    team1 = Team(players=get_players[0:2])
    team2 = Team(players=get_players[2:4])
    rally = Rally(shots=get_shots, rally_score=(0, 0, 2))
    g = Game(game_guid='game1', game_date='2022-01-01', game_location='location1', teams=[team1, team2], rallies=[rally], final_score=(9, 11))
    game_dict = g.to_dict()
    assert isinstance(game_dict, dict), 'Game.to_dict() should return a dict'
    assert game_dict['game_guid'] == 'game1'
    assert game_dict['game_date'] == '2022-01-01'
    assert game_dict['game_location'] == 'location1'
    assert len(game_dict['teams']) == 2
    assert len(game_dict['rallies']) == 1
    assert game_dict['final_score'] == (9, 11)

def test_game_methods(get_players, get_shots):
    team1 = Team(players=get_players[0:2])
    team2 = Team(players=get_players[2:4])
    rally = Rally(shots=get_shots, rally_score=(0, 0, 2))
    g = Game(game_guid='game1', game_date='2022-01-01', game_location='location1', teams=[team1, team2], rallies=[rally], final_score=(9, 11))
    assert len(g.players()) == 4
    assert [p.player_guid for p in g.players()] == list(g.player_shots().keys())
    assert g.rally_count() == 1
    assert len(g.score_states()) == 1
    assert g.shot_count() == 10
    assert len(g.shots()) == 10
    assert g.winner() == 1
    assert g.winning_team() == team2

# score
def test_score():
    s = Score(*[0, 0, 2, 0])
    assert s.server_score == 0
    assert s.returner_score == 0
    assert s.server_number == 2
    assert s.serving_team == 0

def test_score_to_string():
    s = Score(*[0, 0, 2, 0])
    assert score_to_string(s) == '0-0-2'
