# TODO
# - Named Tuple of expected pot for a given set of rolls
# - Way to inspect state of Game before sevening out

import game_control

def test_game_runs():
    game_control.play_game()

def test_easy_win():
    pot = game_control.play_game([7,11,7,10,7])
    assert(pot == 1020)

def test_button_hit():
    expected_pots = (
        ([4, 4, 10, 7], 1000),
        ([5, 5, 10, 7], 1000),
        ([6, 6, 10, 7], 1000),
        ([8, 8, 10, 7], 1000),
        ([9, 9, 10, 7], 1000),
        ([10, 10, 10, 7], 1000),
        ([7, 6, 2, 3, 4, 5, 8, 9, 10, 11, 12, 6, 11, 7, 10, 7], 1030)
    )

    for rolls, expected_pot in expected_pots:
        assert(expected_pot == game_control.play_game(rolls))
