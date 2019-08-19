# Pull out sets of rolls into types of game, e.g. 4,4,10,7 => "hit button once"

import logging.config
import yaml
import pytest

from game import GameManager, FixedDice, Game
from bets import PassLineBet, PassLineOdds
from exceptions import InvalidBetAmount, InvalidBetType, InvalidRoll

with open('/craps/test/logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


class Tester:

    def set_default_config(self):
        self.default_bets = None

    def run_game(self, rolls, initial_state=None):
        game = Game()
        self.set_default_config()

        if initial_state:
            game.state = inital_state
        else:
            game.place_bets(self.default_bets)

        for roll in rolls:
            game.update(roll)

        return game.state

    def verify_game(self, rolls, target, initial_state=None):
        """
        Verify a game ends up in expected state after some rolls
        """
        actual = self.run_game(rolls, initial_state)
        for piece_of_state in target:
            assert actual[piece_of_state] == target[piece_of_state]


class TestMainLine(Tester):

    def set_default_config(self):
        self.default_bets = [PassLineBet(10)]

    def test_game_runs(self):
        manager = GameManager()
        manager.play_games(num_games=1, bets=[PassLineBet(10)])

    def test_invalid_roll(self):
        with pytest.raises(InvalidRoll):
            self.run_game(rolls=[13])


class TestPassLineBet(Tester):

    def set_default_config(self):
        self.default_bets = [PassLineBet(10)]

    def test_easy_win_on_comeout_roll(self):
        self.verify_game(rolls=[7, 11, 11, 7],
                         target={
                             "pot": 40, "point": 0, "bets": [PassLineBet(10)]})

    def test_point_hit(self):
        target = {"pot": 10, "point": 0, "bets": [PassLineBet(10)]}
        self.verify_game(rolls=[4, 4], target=target)
        self.verify_game(rolls=[5, 5], target=target)
        self.verify_game(rolls=[6, 6], target=target)
        self.verify_game(rolls=[8, 8], target=target)
        self.verify_game(rolls=[9, 9], target=target)
        self.verify_game(rolls=[10, 10], target=target)

    def test_crap_out(self):
        self.verify_game(rolls=[2], target={"pot": -10, "bets": []})
        self.verify_game(rolls=[3], target={"pot": -10, "bets": []})
        self.verify_game(rolls=[12], target={"pot": -10, "bets": []})
        self.verify_game(
            rolls=[7, 11, 4, 4, 12], target={"pot": 20, "bets": []})

    def test_seven_out(self):
        self.verify_game(rolls=[6, 7], target={"pot": -10, "bets": []})

    def test_inaction_when_point_on(self):
        self.verify_game(rolls=[4, 2, 3, 5, 6, 8, 9, 10, 11, 12],
                         target={
                             "pot": 0, "point": 4, "bets": [PassLineBet(10)]})

    def test_bet_validation(self):
        with pytest.raises(InvalidBetAmount):
            PassLineBet(27)

        with pytest.raises(InvalidBetAmount):
            PassLineBet(-10)

        with pytest.raises(InvalidBetAmount):
            PassLineBet(0)

class TestPassLineOdds(Tester):

    def set_default_config(self):
        pass_line = PassLineBet(10)
        odds = PassLineOdds(amount=20, pass_line_bet=pass_line)
        self.default_bets = [pass_line, odds]

    def test_point_hit(self):
        self.set_default_config()
        bets = self.default_bets

        self.verify_game(rolls=[4, 4], target={"pot": 50, "bets": bets})
        self.verify_game(rolls=[5, 5], target={"pot": 40, "bets": bets})
        self.verify_game(rolls=[6, 6], target={"pot": 34, "bets": bets})
        self.verify_game(rolls=[8, 8], target={"pot": 34, "bets": bets})
        self.verify_game(rolls=[9, 9], target={"pot": 40, "bets": bets})
        self.verify_game(rolls=[10, 10], target={"pot": 50, "bets": bets})

    def test_crap_out(self):
        """
        Odds are only placed when the point goes on, so should only lose the
        PassLineBet
        """
        target_bets = [PassLineOdds(amount=20, pass_line_bet=PassLineBet(10))]
        self.verify_game(rolls=[2], target={"pot": -10, "bets": target_bets})
        self.verify_game(rolls=[3], target={"pot": -10, "bets": target_bets})
        self.verify_game(rolls=[12], target={"pot": -10, "bets": target_bets})

    def test_seven_out(self):
        self.verify_game(rolls=[4, 7], target={"pot": -30, "bets": []})

class TestCombinations(Tester):

    def test_all_bets(self):
        pass_line = PassLineBet(20)
        odds = PassLineOdds(amount=100, pass_line_bet=pass_line)
        initial_bets = [pass_line, odds]
        rolls = [7, 4, 3, 6, 4, 7, 5, 7]

        game = Game()
        game.place_bets(initial_bets)
        for roll in rolls:
            game.update(roll)

        assert game.state["bets"] == []
        assert game.state["pot"] is 140

