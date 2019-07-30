# TODO
# - Add more bets
#   - Pass Line odds
#   - Come
# - Put useful info on InvalidBetAmount


# Provides the Bet class
from textwrap import dedent

class Bet(object):
    """
    Represents a bet on the table. Main purpose is to calculate how much money
    a bet makes for a given roll/state
    """

    def __init__(self, amount):
        self.amount = amount
        self.bet_type = self.__class__.__name__
        self._verify_bet()

    def __repr__(self):
        return(self.bet_type + "({})".format(self.amount))

    def _verify_bet(self):
        if self.amount % 5 != 0:

            explanation = dedent("""
            Amount must be a multiple of 5
            """)
            raise InvalidBetAmount(self.bet_type, self.amount, explanation)

    def get_winnings(self, roll, point):
        pass


class PassLineBet(Bet):
    """
    Main bet on the pass line (not the odds)
    - Double your money on 7/11 with come out roll
    - Double your money on point hit
    - Lose your money on 2/3/12 come out roll
    - Loses on 7-out
    """

    def get_winnings(self, roll, point):

        if point.is_off and roll in [7, 11]:
            return self.amount

        elif roll == point.number:
            return self.amount

        elif point.is_off and roll in [2, 3, 12]:
            return -self.amount

        elif point.is_on and roll is 7:
            return -self.amount

        else:
            return 0


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
    pass


class InvalidBetAmount(Exception):
    """
    Raise when attempting to create a bet with a disallowed amount
    """
    def __init__(self, bet, amount, info):
        self.bet = bet
        self.amount = amount
        self.info = info

    def __str__(self):
        return(dedent("""
            Attempted to place a bet with an invalid amount:
            Bet type - {bet}
            Amount - {amount} {info}""").format(
            bet=self.bet,amount=self.amount,info=self.info))