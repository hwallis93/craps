# TODO
# - Good way of setting a Game's state
# - File-based bet strategy config into GameManager
#   - Parse lines
#   - Update Bets to be created from str
#   - Add a "verify config" sort of function to check file is well formatted
# - Multithread GameManager's play_games?
# - Stats from GameManager
#   - Number of certain kinds of win etc...
import random
from exceptions import InvalidRoll

import logging

logger = logging.getLogger(__name__)


class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """

    def __init__(self, bets):
        logger.info("Creating Game")

        self._bets = bets
        self._pot = 0
        self._point = Point()
        self.come_box_is_empty = True

    @property
    def state(self):
        return {
            "bets": [bet.state for bet in self._bets],
            "pot": self._pot,
            "point": self._point,
        }

    def update(self, roll):
        """
        Update game state given a dice roll
        """
        logger.info(f"Updating game with roll - {roll}")
        logger.debug(f"From state {self.state}")

        for bet in self._bets:
            winnings = bet.get_winnings(roll, self._point)
            if winnings:
                logger.info(f"{bet} won {winnings} - Add to pot")
                self._pot += winnings

        for bet in self._bets:
            bet.update(roll, self._point)

        self._point.update(roll)

        for bet in self._bets:
            bet.maybe_place(roll, self._point, self)


class Point(object):
    """
    Represents the point
    """

    def __init__(self):
        logger.debug("Initalise Point")
        self._value = 0

    def __repr__(self):
        if self.is_off:
            return "<Point: Off>"
        else:
            return f"<Point: {self._value}>"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self._value == other._value

        elif isinstance(other, int):
            return self._value == other

        else:
            return False

    def update(self, roll):
        """
        For a given dice roll, update the point
        """
        if self.is_off:
            if roll in [4, 5, 6, 8, 9, 10]:
                logger.info(f"Point goes on {roll}")
                self._value = roll

        elif self.is_on:
            if roll is self.number:
                logger.info("Point is hit, turn it off")
                self._value = 0

            elif roll is 7:
                logger.info("Seven out, turn point off")
                self._value = 0

    @property
    def is_on(self):
        return self._value > 0

    @property
    def is_off(self):
        return self._value == 0

    @property
    def number(self):
        return self._value
