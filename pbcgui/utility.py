from collections import Counter

def next_score(score, winner):
    """Calculates the next score based on the current score and the winner of the point."""
    server_score, returner_score, server_number = score
    if winner == 'server':
        return (server_score + 1, returner_score, server_number)
    elif all((winner == 'returner', server_number == 1)):
        return (server_score, returner_score, 2)
    else:
        return (returner_score, server_score, 1)


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


