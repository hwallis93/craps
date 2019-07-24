# TODO
# - Named Tuple of expected pot for a given set of rolls
# - Way to inspect state of Game before sevening out
# - Test case helper classes

from game import Game, play_game
from bets import PassLineBet

def _verify_pot(rolls, bets, expected_pot):
    pot = play_game(bets, forced_rolls = rolls)
    assert(pot == expected_pot)

def test_game_runs():
    play_game([PassLineBet(10)])

def test_easy_win():
    test_games = (
        ([7, 11, 7, 10, 7], [PassLineBet(10)], 1020),
    )

    for rolls, bets, expected_pot in test_games:
        _verify_pot(rolls, bets, expected_pot)

def test_button_hit():
    test_games = (
        ([4, 4, 10, 7], [PassLineBet(10)], 1000),
        ([5, 5, 10, 7], [PassLineBet(10)], 1000),
        ([6, 6, 10, 7], [PassLineBet(10)], 1000),
        ([8, 8, 10, 7], [PassLineBet(10)], 1000),
        ([9, 9, 10, 7], [PassLineBet(10)], 1000),
        ([10, 10, 10, 7], [PassLineBet(10)], 1000),
        ([7, 6, 2, 3, 4, 5, 8, 9, 10, 11, 12, 6, 11, 7, 10, 7],
         [PassLineBet(10)], 1030),
    )

    for rolls, bets, expected_pot in test_games:
        _verify_pot(rolls, bets, expected_pot)
