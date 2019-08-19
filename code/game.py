# TODO
# - Logging:
#   - Logs indent with each function call
#   - Import logging neatly from one place
# - File-based bet strategy config into GameManager
#   - Parse lines
#   - Update Bets to be created from str
#   - Add a "verify config" sort of function to check file is well formatted
# - Multithread GameManager's play_games?
# - Stats from GameManager
#   - Number of certain kinds of win etc...
import logging
logger = logging.getLogger(__name__)

import random


class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """
    def __init__(self):
        logger.debug("Creating Game object")
        self._bets = []
        self._pot = 0
        self._point = Point()
        self._has_sevened_out = False

    def __repr__(self):
        return(self.state)

    @property
    def state(self):
        return {
            "bets": self._bets,
            "pot": self._pot,
            "point": self._point,
        }

    def place_bets(self, bets):
        """
        Place some bets
        """
        logger.debug(f"Adding bets {bets}")
        self._bets += bets


    def update(self, roll):
        """
        Update game state given a dice roll
        """
        logger.debug(f"Updating game with roll - {roll}")
        self._update_bets(roll)

        if roll in [7,11] and self._point.is_off:
            self._process_easy_win()

        elif roll in [2,3,12] and self._point.is_off:
            self._process_crap_out()

        elif roll in [4,5,6,8,9,10] and self._point.is_off:
            self._process_point_on(roll)

        elif roll is 7 and self._point.is_on:
            self._process_seven_out()

        elif roll is self._point.number:
            self._process_button_hit()

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self._point.is_on:
            self._process_button_miss()


    def _update_bets(self, roll):
        logger.debug(f"Updating bets with roll - {roll}")
        for bet in self._bets:
            bet_update = bet.update(roll, self._point)
            winnings, removed = bet_update.winnings, bet_update.removed

            if winnings:
                logger.debug(f"Adding {winnings} to pot")
                self._pot += winnings
            elif removed:
                logger.debug(f"Removing bet from the table - {bet}")
                self._bets.remove(bet)
                self._pot -= bet.amount

    def _process_easy_win(self):
        logger.debug("Easy win")

    def _process_crap_out(self):
        logger.debug("Crap out")

    def _process_point_on(self, roll):
        logger.debug("Point goes on")
        self._point.put_on(roll)

    def _process_seven_out(self):
        logger.debug("Seven out")
        self._has_sevened_out = True

    def _process_button_hit(self):
        logger.debug("Point turned off")
        self._point.take_off()

    def _process_button_miss(self):
        logger.debug("Point not hit")


class GameManager(object):
    """
    Responsible for determining the outcome of playing multiple games under
    certain conditions
    """
    def play_games(self, num_games, bets, fixed_dice=None):
        """
        Play some games with certain bets
        :param num_games: int
        :param bets: [Bet]
        :param fixed_dice: FixedDice
        :return: Winnings
        """
        self.fixed_dice = fixed_dice

        winnings = 0
        for game in range(num_games):
            winnings += self._play_game(bets)

        return winnings

    @property
    def current_game_state(self):
        """
        Return the state of the game currently in progress for testing purposes
        """
        return self.game.state


    def _play_game(self, bets):
        self.game = Game()
        while not self.game._has_sevened_out:
            self._play_round(bets)

        if self.fixed_dice:
            self.fixed_dice.next_game()

        return self.game.state["pot"]

    def _play_round(self, bets):
        bets_to_place = self._decide_bets(bets)
        if bets_to_place:
            self.game.place_bets(bets_to_place)

        dice_roll = self._roll_the_dice()
        self.game.update(dice_roll)

    def _decide_bets(self, bets):
        """
        Determine whether we want to place more bets. For now, just ensure the
        bets we start with are always replaced
        """
        return [bet for bet in bets if bet not in self.game.state["bets"]]


    def _roll_the_dice(self):
        """
        Roll a pair of fair six-sided dice
        """
        if self.fixed_dice:
            roll = self.fixed_dice.get_next_roll()
        else:
            roll =  random.randint(1,6) + random.randint(1,6)

        return(roll)


class FixedDice(object):
    def __init__(self, rolls):
        """
        :param rolls: [[int]] - List of lists of rolls
        """
        self.rolls = rolls
        self.game_num = 0
        self.roll_num = 0

    def get_next_roll(self):
        roll = self.rolls[self.game_num][self.roll_num]
        self.roll_num += 1
        return roll

    def next_game(self):
        """
        Move on to the next game, i.e. the next set of dice rolls
        """
        self.game_num += 1


class Point(object):
    """
    Represents the point
    """
    def __init__(self):
        logger.debug("Initalise Point")
        self._value = 0

    def __repr__(self):
        if self.is_off:
            return("Point: Off")
        else:
            return(f"Point: {self._value}")

    def put_on(self, value):
        logger.debug(f"Point put on {value}")
        self._value = value

    def take_off(self):
        logger.debug("Point turned off")
        self._value = 0

    @property
    def is_on(self):
        return self._value > 0

    @property
    def is_off(self):
        return self._value == 0

    @property
    def number(self):
        if self._value is 0:
            number = None
        else:
            number = self._value
        return number
