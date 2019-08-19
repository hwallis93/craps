# TODO
# - Add more bets
#   - Pass Line odds
#   - Come
# - Exception explanations should be logs
# - Have a think about whether bets should be saying they're removed from table
#   when they lose

# Provides the Bet class
import logging
logger = logging.getLogger(__name__)

from textwrap import dedent
from math import floor
from collections import namedtuple
from bet_exceptions import InvalidBetAmount, InvalidBetType, InvalidRoll

BetUpdate = namedtuple("BetUpdate", "winnings removed")

class Bet(object):
    """
    Represents a bet on the table. Main purpose is to calculate how much money
    a bet makes for a given roll/state
    """

    def __init__(self, amount):
        self.amount = amount
        self.bet_type = self.__class__.__name__
        self._verify()

    def __repr__(self):
        return f"{self.bet_type}({self.amount})"

    def __eq__(self, other):
        if (isinstance(other, Bet) and
            self.bet_type == other.bet_type and
            self.amount == other.amount):
            return True

        else:
            return False


    def _verify(self):
        if self.amount % 5 != 0:

            explanation = dedent("""
            Amount must be a multiple of 5
            """)
            raise InvalidBetAmount(self.bet_type, self.amount, explanation)

    def update(self, roll, point):
        """
        :param point: Point object
        :return: BetUpdate(int, bool)
        """
        pass


class PassLineBet(Bet):
    """
    Main bet on the pass line (not the odds)
    - Double your money on 7/11 with come out roll
    - Double your money on point hit
    - Lose your money on 2/3/12 come out roll
    - Loses on 7-out
    """

    def update(self, roll, point):
        if point.is_off and roll in [7, 11]:
            winnings = self.amount
        elif roll == point.number:
            winnings = self.amount
        else:
            winnings = 0

        if point.is_off and roll in [2, 3, 12]:
            removed = True
        elif point.is_on and roll is 7:
            removed = True
        else:
            removed = False

        return(BetUpdate(winnings, removed))


class PassLineOdds(Bet):
    """
    Odds behind the Pass Line bet
    - Not working if the point is off
    - Pays out when the point is hit:
      - Point is 4 or 10 => Pays 2-to-1
      - Point is 5 or 9 => Pays 3-to-2
      - Point is 6 or 8 => Pays 6-to-5
    - Loses on 7-out
    """
    def __init__(self, pass_line_bet, *args, **kwargs):
        self.pass_line_bet = pass_line_bet
        super(PassLineOdds, self).__init__(*args, **kwargs)

    def _verify(self):
        if not isinstance(self.pass_line_bet, PassLineBet):
            raise InvalidBetType()

        if (self.amount % 5 != 0 or
            self.amount / self.pass_line_bet.amount not in [1, 2, 3, 4, 5]):
            raise InvalidBetAmount(self.bet_type, self.amount)

    def get_winnings(self, roll, point):
        logging.critical(f"""Calculating PassLineOdds winnings with""")
        logging.critical(f"Point is on - {point.is_on}")
        if point.is_on and point.number == roll:

            if point.number in [4, 10]:
                winnings = 2*self.amount

            elif point.number in [5, 9]:
                winnings = floor(1.5*self.amount)

            elif point.number in [6, 8]:
                winnings = floor(1.2*self.amount)

            else:
                raise InvalidRoll()

        elif point.is_on and roll == 7:
            winnings = -self.amount

        else:
            winnings = 0

        return(winnings)

