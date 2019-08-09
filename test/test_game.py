# Sort tests into classes for clarity
# Not have to force 7 out at the end of rolls
# Pull out sets of rolls into types of game, e.g. 4,4,10,7 => "hit button once"


from game import GameManager, FixedDice
from bets import PassLineBet, PassLineOdds


def verify_games(test_games):
    for rolls, bets, expected_pot in test_games:
        verify_game(rolls, bets, expected_pot)


def verify_game(rolls, bets, expected_pot):
    pot = play_game(bets, forced_rolls=rolls)
    assert(pot == expected_pot)


def test_game_runs():
    play_game([PassLineBet(10)])


def test_easy_win():
    test_games = (
        ([7, 11, 7, 10, 7], [PassLineBet(10)], 20),
    )
    dice = FixedDice([7, 11, 7, 10, 7])
    manager = GameManager(dice)
    manager.play_games(1, [PassLineBet(10)])
    assert(manager.game.pot == 20)


def test_button_hit():
    test_games = (
        ([4, 4, 10, 7], [PassLineBet(10)], 0),
        ([5, 5, 10, 7], [PassLineBet(10)], 0),
        ([6, 6, 10, 7], [PassLineBet(10)], 0),
        ([8, 8, 10, 7], [PassLineBet(10)], 0),
        ([9, 9, 10, 7], [PassLineBet(10)], 0),
        ([10, 10, 10, 7], [PassLineBet(10)], 0),
        ([7, 6, 2, 3, 4, 5, 8, 9, 10, 11, 12, 6, 11, 7, 10, 7],
         [PassLineBet(10)], 30),
    )
    verify_games(test_games)

def test_pass_line_odds():
    pass_line = PassLineBet(20)
    odds = PassLineOdds(pass_line, 60)

    test_games = (
        ([4, 4, 10, 7], [pass_line, odds], 60),
    )
    verify_games(test_games)

def test_game_manager():
    manager = GameManager()

    print(manager.play_games(1, [PassLineBet(10)]))
