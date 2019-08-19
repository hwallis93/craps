# Sort tests into classes for clarity
# Not have to force 7 out at the end of rolls
# Pull out sets of rolls into types of game, e.g. 4,4,10,7 => "hit button once"
import logging.config
import yaml

with open('/craps/test/logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

from game import GameManager, FixedDice, Game
from bets import PassLineBet, PassLineOdds

def run_game(rolls, inital_state=None):
    game=Game()

    if inital_state:
        game.state = inital_state
    else:
        game.place_bets([PassLineBet(10)])

    for roll in rolls:
        game.update(roll)

    return game.state

def verify_bets(test_bets, expected_bets):
    for test_bet, expected_bet in zip(test_bets, expected_bets):
        assert isinstance(test_bet, type(expected_bet))
        assert test_bet.amount == expected_bet.amount


def test_game_runs():
    manager = GameManager()
    manager.play_games(num_games=1, bets=[PassLineBet(10)])


def test_pass_line_bet():
    state = run_game(rolls=[7, 11, 11, 7])

    assert state["pot"] is 40
    assert state["point"].is_off
    verify_bets(state["bets"], [PassLineBet(10)])

