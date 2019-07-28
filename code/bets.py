# TODO
# - Add more bets

# Provides the Bet class


class Bet(object):
    """
    Represents a bet on the table. Main purpose is to calculate how much money
    a bet makes for a given roll/state
    """

    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return(self.__class__.__name__ + "({})".format(self.amount))

    def get_winnings(self, roll, point):
        pass


class PassLineBet(Bet):
    """
    Main bet on the pass line (not the odds)
    - Double your money on 7/11 with come out roll
    - Double your money on point hit
    - Lose your money on 2/3/12 come out roll
    - Lose your money on 7 when point is on
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

