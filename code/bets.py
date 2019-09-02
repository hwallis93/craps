# TODO
# - Add more bets
#   - Come
# - Refactor to allow bets to be "returned to hand" rather than reapplying them
#   in Game or GameManager. Yeah so then bets "appear" as and when they know
#   that they should.
# - Ending the round when the shooter changes is arbitrary, the game should
#   just keep rolling ad infinitum

# Provides the Bet class
import logging
logger = logging.getLogger(__name__)

from math import floor
from exceptions import InvalidBetAmount, InvalidBetType, InvalidRoll


class Bet(object):
    """
    Represents a bet that the player desires to make. Can either be on the
    table or waiting to be placed.
    """
    def __init__(self, amount):
        self._amount = amount
        self._type = self.__class__.__name__
        self._position = "hand"
        self._verify()

    def __repr__(self):
        return f"<{self._type}({self._amount})>"

    def __eq__(self, other):
        try:
            return (self._type == other._type and
                    self._amount == other._amount and
                    self._position == other._position)
        except AttributeError:
            return False

    @property
    def state(self):
        return {
            "type": self._type,
            "amount": self._amount,
            "position": self._position
        }

    def get_winnings(self, roll, point):
        """
        Calculate how much the Bet wins for a given Point and roll
        """
        pass

    def update(self, roll, point):
        """
        Update the Bet's internal state. E.g. what a Come bet is on or whether
        to return a Bet to the hand, default is returning to hand if the Bet
        won or lost this round
        """
        if self._won(roll, point) or self._lost(roll, point):
            logger.info(f"Moved {self} to hand")
            self._position = "hand"

    def maybe_place(self, roll, point, game):
        """
        Make the Bet (place it on the table) if necessary
        :param game: Game object the Bet is part of
        """
        pass

    def _verify(self):
        """
        Verify the Bet is being created in a valid way
        """
        if self._amount % 10 != 0:
            explanation = "Amount must be a multiple of 10"
            raise InvalidBetAmount(self._type, self._amount, explanation)

        if self._amount <= 0:
            explanation = "Amount must be greater than 0"
            raise InvalidBetAmount(self._type, self._amount, explanation)

    def _won(self, roll, point):
        """
        Helper to determine whether the bet won
        """
        pass

    def _lost(self, roll, point):
        """
        Helper to determine whether the bet lost
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
    def get_winnings(self, roll, point):
        logger.debug(f"Calculate winnings for {self}")
        winnings = 0

        if self._won(roll, point):
            winnings = self._amount
        elif self._lost(roll, point):
            winnings = -self._amount

        logger.debug(f"{self} had winnings {winnings}")
        return winnings

    def maybe_place(self, roll, point, game):
        # Pass Line bet always goes straight on the table
        if self._position == "hand":
            logger.info(f"Placed bet {self}")
            self._position = "table"

    def _won(self, roll, point):
        return (point.is_off and roll in (7, 11) or
                point.is_on and roll is point.number)

    def _lost(self, roll, point):
        return (point.is_off and roll in (2, 3, 12) or
                point.is_on and roll is 7)


class PassLineOdds(Bet):
    """
    Odds behind the Pass Line bet
    - Pays out when the point is hit:
      - Point is 4 or 10 => Pays 2-to-1
      - Point is 5 or 9 => Pays 3-to-2
      - Point is 6 or 8 => Pays 6-to-5
    - Loses on 7-out
    """
    def __init__(self, pass_line_bet, *args, **kwargs):
        self.pass_line_bet = pass_line_bet
        super(PassLineOdds, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<{self._type}({self._amount}) behind {self.pass_line_bet}>"

    def __eq__(self, other):
        if super(PassLineOdds, self).__eq__(other):
            try:
                return self.pass_line_bet == other.pass_line_bet
            except AttributeError:
                return False
        else:
            return False

    def _verify(self):
        super(PassLineOdds, self)._verify()

        if not isinstance(self.pass_line_bet, PassLineBet):
            explanation = (
                f"Attempted to create without a PassLineBet - "
                f"{self.pass_line_bet}")
            raise InvalidBetType(self, explanation)

        if self._amount / self.pass_line_bet._amount not in (1, 2, 3, 4, 5):
            explanation = (f"Must be exactly 1-5 times as much as associated "
                           f"PassLineBet, which has value "
                           f"{self.pass_line_bet._amount}")
            raise InvalidBetAmount(self._type, self._amount, explanation)

    def get_winnings(self, roll, point):
        winnings = 0

        if self._won(roll, point):
            if point.number in (4, 10):
                winnings = 2 * self._amount
            elif point.number in (5, 9):
                winnings = floor(1.5 * self._amount)
            elif point.number in (6, 8):
                winnings = floor(1.2 * self._amount)
            else:
                raise ValueError("Inconsistency between win state and roll")

        if self._lost(roll, point):
            winnings = -self._amount

        logger.debug(f"{self} had winnings {winnings}")
        return winnings

    def maybe_place(self, roll, point, game):
        if self._position == "hand" and point.is_on:
            logger.info(f"Placed bet {self}")
            self._position = "table"

    def _won(self, roll, point):
        return point.is_on and roll is point.number

    def _lost(self, roll, point):
        return point.is_on and roll is 7


class ComeBet(Bet):
    """
    A bet in the Come box
    - Can only be laid if the point is on
    - 7 or 11 => Pays 1-to-1 (stays in come box)
    - 2, 3 or 12 => Loses
    - 4, 5, 6, 8, 9, 10 => Moved onto that number
    - If that number is rolled again before a 7 => Pays 1-to-1
    - else => Loses

    Positions: "hand", "box", 4, 5, 6, 8, 9, 10
    """
    def get_winnings(self, roll, point):
        winnings = 0
        if self._won(roll, point):
            winnings = self._amount
        elif self._lost(roll, point):
            winnings = -self._amount

        logger.debug(f"{self} had winnings {winnings}")
        return winnings

    def maybe_place(self, roll, point, game):
        if self._position == "hand" and point.is_on and game.come_box_is_empty:
            logger.info(f"Placed bet {self} in the Come box")
            self._position = "box"

    def update(self, roll, point):
        if self._lost(roll, point) or self._won(roll, point):
            logger.info(f"Moved {self} to hand")
            self._position = "hand"

        elif self._in_box and roll in (4, 5, 6, 8, 9, 10):
            logger.info(f"{self} goes on {roll}")
            self._position = roll

    def _won(self, roll, point):
        return (self._is_on and roll is self._position or
                self._in_box and roll in (7, 11))

    def _lost(self, roll, point):
        return (self._is_on and roll is 7 or
                self._in_box and roll in (2, 3, 12))

    @property
    def _is_on(self):
        return isinstance(self._position, int)

    @property
    def _in_box(self):
        return self._position == "box"
