from collections import Counter
import json

from .data import Score


class StructuredMessage(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return json.dumps(self.kwargs)

def game_over(score):
    """Checks if the game is over based on the current score."""
    return any((score.server_score >= 11 and score.server_score - score.returner_score >= 2,
                score.returner_score >= 11 and score.returner_score - score.server_score >= 2))


def next_score(score, winner):
    """Calculates the next score based on the current score and the winner of the point."""
    if winner == 'server':
        return Score(score.server_score + 1, score.returner_score, score.server_number, score.serving_team)

    elif all((winner == 'returner', score.server_number == 1)):
        return Score(score.server_score, score.returner_score, 2, score.serving_team)

    else:
        return Score(score.returner_score, score.server_score, 1, 1 if score.serving_team == 0 else 0)

def score_to_string(score):
    """Converts a score tuple to a string."""
    return '-'.join([str(i) for i in score.score_tuple()])


def string_to_score(score_string):
    """Converts a score string to a tuple of integers."""
    return tuple([int(i) for i in score_string.split('-')])


def unique_names(players):
    new_players = []
    for player, cnt in Counter(players).items():
        if cnt == 2:
            new_players.append(f"{player} 1")
            new_players.append(f"{player} 2")
        elif cnt == 3:
            new_players.append(f"{player} 1")
            new_players.append(f"{player} 2")
            new_players.append(f"{player} 3")
        elif cnt == 4:
            new_players.append(f"{player} 1")
            new_players.append(f"{player} 2")
            new_players.append(f"{player} 3")
            new_players.append(f"{player} 4")
        else:
            new_players.append(player)
    return new_players


