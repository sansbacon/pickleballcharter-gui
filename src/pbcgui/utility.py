def next_possible_scores(score):
    server_score, returner_score, server_number = score

    # If the server wins the rally, they score a point
    server_wins = (server_score + 1, returner_score, server_number)

    # If the returner wins the rally, they become the server, but don't score a point
    # The server number switches between 1 and 2
    returner_wins = (server_score, returner_score, 2 if server_number == 1 else 1)

    return [server_wins, returner_wins]

