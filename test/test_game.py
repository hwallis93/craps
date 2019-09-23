# Pull out sets of rolls into types of game, e.g. 4,4,10,7 => "hit button once"

import pytest

from game import Game
from bets import PassLineBet, PassLineOdds, Bet, ComeBet, ComeOdds
from exceptions import InvalidBetAmount, InvalidBetType, InvalidRoll


class Tester:
    def verify_game(self, rolls, bets, expected):
        """
        Verify a game ends up in expected state after some rolls
        """
        game = Game(bets=bets)

        for roll in rolls:
            game.update(roll)

        if "pot" in expected:
            assert game.state["pot"] == expected["pot"]
        if "point" in expected:
            assert game.state["point"] == expected["point"]
        if "bets" in expected:
            assert game.state["bets"] == expected["bets"]


class TestPassLineBet(Tester):
    @pytest.fixture
    def bets(self):
        return [PassLineBet(10)]

    @pytest.fixture
    def expected_bets(self):
        return [{"type": "PassLineBet", "amount": 10, "position": "table"}]

    def test_easy_win_on_comeout_roll(self, bets, expected_bets):
        self.verify_game(
            rolls=[7, 11, 11, 7],
            bets=bets,
            expected={"pot": 40, "point": 0, "bets": expected_bets},
        )

    def test_point_hit(self, bets, expected_bets):
        expected = {"pot": 10, "point": 0, "bets": expected_bets}
        self.verify_game(rolls=[4, 4], bets=bets, expected=expected)
        self.verify_game(rolls=[5, 5], bets=bets, expected=expected)
        self.verify_game(rolls=[6, 6], bets=bets, expected=expected)
        self.verify_game(rolls=[8, 8], bets=bets, expected=expected)
        self.verify_game(rolls=[9, 9], bets=bets, expected=expected)
        self.verify_game(rolls=[10, 10], bets=bets, expected=expected)

    def test_crap_out(self, bets, expected_bets):
        expected = {"pot": -10, "point": 0, "bets": expected_bets}
        self.verify_game(rolls=[2], bets=bets, expected=expected)
        self.verify_game(rolls=[3], bets=bets, expected=expected)
        self.verify_game(rolls=[12], bets=bets, expected=expected)

        expected = {"pot": 20, "point": 0, "bets": expected_bets}
        self.verify_game(rolls=[7, 11, 4, 4, 12], bets=bets, expected=expected)

    def test_seven_out(self, bets, expected_bets):
        expected = {"pot": -10, "point": 0, "bets": expected_bets}
        self.verify_game(rolls=[6, 7], bets=bets, expected=expected)

    def test_inaction_when_point_on(self, bets, expected_bets):
        expected = {"pot": 0, "point": 4, "bets": expected_bets}
        self.verify_game(
            rolls=[4, 2, 3, 5, 6, 8, 9, 10, 11, 12], bets=bets, expected=expected
        )

    def test_bet_validation(self):
        with pytest.raises(InvalidBetAmount):
            PassLineBet(27)

        with pytest.raises(InvalidBetAmount):
            PassLineBet(-10)

        with pytest.raises(InvalidBetAmount):
            PassLineBet(0)


class TestPassLineOdds(Tester):
    @pytest.fixture
    def bets(self):
        pass_line = PassLineBet(10)
        odds = PassLineOdds(amount=20, parent_bet=pass_line)
        return [pass_line, odds]

    @pytest.fixture
    def expected_bets(self):
        return [
            {"type": "PassLineBet", "amount": 10, "position": "table"},
            {"type": "PassLineOdds", "amount": 20, "position": "hand"},
        ]

    def test_point_hit(self, bets, expected_bets):
        self.verify_game(
            rolls=[4, 4],
            bets=bets,
            expected={"pot": 50, "bets": expected_bets, "point": 0},
        )
        self.verify_game(
            rolls=[5, 5],
            bets=bets,
            expected={"pot": 40, "bets": expected_bets, "point": 0},
        )
        self.verify_game(
            rolls=[6, 6],
            bets=bets,
            expected={"pot": 34, "bets": expected_bets, "point": 0},
        )
        self.verify_game(
            rolls=[8, 8],
            bets=bets,
            expected={"pot": 34, "bets": expected_bets, "point": 0},
        )
        self.verify_game(
            rolls=[9, 9],
            bets=bets,
            expected={"pot": 40, "bets": expected_bets, "point": 0},
        )
        self.verify_game(
            rolls=[10, 10],
            bets=bets,
            expected={"pot": 50, "bets": expected_bets, "point": 0},
        )

    def test_crap_out(self, bets, expected_bets):
        expected_bets[1]["position"] = "hand"
        expected = {"pot": -10, "bets": expected_bets, "poi nt": 0}
        self.verify_game(rolls=[2], bets=bets, expected=expected)
        self.verify_game(rolls=[3], bets=bets, expected=expected)
        self.verify_game(rolls=[12], bets=bets, expected=expected)

    def test_seven_out(self, bets, expected_bets):
        expected_bets[1]["position"] = "hand"
        expected = {"pot": -30, "bets": expected_bets, "point": 0}
        self.verify_game(rolls=[4, 7], bets=bets, expected=expected)

    def test_bet_validation(self):
        pass_line = PassLineBet(20)

        with pytest.raises(InvalidBetType):
            PassLineOdds(amount=10, parent_bet=Bet(20))
        with pytest.raises(InvalidBetType):
            PassLineOdds(amount=10, parent_bet="AAAAAAAAAAAAAAAAAAA")

        with pytest.raises(InvalidBetAmount):
            PassLineOdds(amount=200, parent_bet=pass_line)
        with pytest.raises(InvalidBetAmount):
            PassLineOdds(amount=10, parent_bet=pass_line)
        with pytest.raises(InvalidBetAmount):
            PassLineOdds(amount=0, parent_bet=pass_line)
        with pytest.raises(InvalidBetAmount):
            PassLineOdds(amount=-10, parent_bet=pass_line)
        with pytest.raises(InvalidBetAmount):
            PassLineOdds(amount=35, parent_bet=pass_line)


class TestComeBet(Tester):
    def bets(self):
        return [PassLineBet(10), ComeBet(10)]

    def expected_bets(self):
        return [
            {"type": "PassLineBet", "amount": 10, "position": "table"},
            {"type": "ComeBet", "amount": 10, "position": None},
        ]

    def verify_parametrized_games(self, rolls, pot, come_position):
        expected_bets = self.expected_bets()
        expected_bets[1]["position"] = come_position
        expected = {"pot": pot, "bets": expected_bets}
        self.verify_game(rolls=rolls, bets=self.bets(), expected=expected)

    @pytest.mark.parametrize(
        "rolls,pot,come_position",
        [
            ([6, 11, 7], 10, "hand"),
            ([6, 7, 11], 10, "hand"),
            ([8, 2], -10, "box"),
            ([9, 3], -10, "box"),
            ([10, 12], -10, "box"),
        ],
    )
    def test_in_come_box(self, rolls, pot, come_position):
        self.verify_parametrized_games(rolls, pot, come_position)

    @pytest.mark.parametrize(
        "rolls,pot,come_position",
        [([4, 6, 6], 10, "box"), ([4, 8, 7], -20, "hand"), ([4, 4, 4], 20, "box")],
    )
    def test_on_number(self, rolls, pot, come_position):
        self.verify_parametrized_games(rolls, pot, come_position)

    @pytest.mark.parametrize(
        "rolls,pot,come_position", [([7, 11, 4, 6, 8, 4, 8], 30, 6)]
    )
    def test_inactivity(self, rolls, pot, come_position):
        self.verify_parametrized_games(rolls, pot, come_position)

    @pytest.mark.parametrize(
        "rolls,pot,come_position", [([3, 4, 3, 7, 3, 4, 7], -30, "hand")]
    )
    def test_removal(self, rolls, pot, come_position):
        self.verify_parametrized_games(rolls, pot, come_position)


class TestComeOdds(Tester):
    def bets(self):
        come_bet = ComeBet(10)
        return [PassLineBet(10), come_bet, ComeOdds(10, parent_bet=come_bet)]

    def expected_bets(self):
        return [
            {"type": "PassLineBet"}
        ]

    def verify_parametrized_games(self, rolls, pot):
        expected = {"pot": pot, "bets": expected_bets}
        pass

    @pytest.mark.parametrize("rolls,pot", [([4, 6, 6]), 22])
    def test_on_number(self):
        rolls = [4, 6, 6]
        self.verify_game([], self.bets())
