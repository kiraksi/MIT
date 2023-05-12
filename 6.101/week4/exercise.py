# Exercise: complete the lose_check function (replace ... below)

CORNERS = [
    ((0, -1), (-1, 0)),  # upper left corner
    ((0, 1), (-1, 0)),  # upper right corner
    ((0, -1), (1, 0)),  # lower left corner
    ((0, 1), (1, 0)),  # lower right corner
]

def lose_check(game):
    """Given a game representation (of the form returned from new_game),
    return a Boolean: True if the given game cannot be won, and False
    otherwise.

    One helpful lose condition is if any computer is in a wall corner
    (and not on a target); there's no way to push it from there so the
    game is a definite lose.

    Assume game["wall"], game["computer"], and game["target"] are sets
    of (row, col) tuples where walls, computers, and targets reside.
    """
    if victory_check(game):
        return False

    for pos in game["computer"] - game["target"]:  # computers not on targets
        for delta_1, delta_2 in CORNERS:
            ...



    return False


def shift(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])
