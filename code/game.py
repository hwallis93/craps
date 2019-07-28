# TODO
# - Use this to determine amount lost over lots of games for a specific betting
#   strategy.
# - Proper logging
# - Make pot a delta, not anything to do with starting amount

import random
from bets import PassLineBet

class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """
    def __init__(self):
        self.point = Point()
        self.seven_out = False
        self.bets = []
        self.pot = 0

    def roll_the_dice(self):
        """
        Roll a pair of fair six-sided dice
        """
        return random.randint(1,6) + random.randint(1,6)

    def play_round(self, forced_roll = None):
        """
        Play a round of craps, a single dice throw
        """

        roll = forced_roll or self.roll_the_dice()
        print
        print("Rolled {}".format(roll))

        if roll in [7,11] and self.point.is_off:
            self._process_easy_win()

        elif roll in [2,3,12] and self.point.is_off:
            self._process_crap_out()

        elif roll in [4,5,6,8,9,10] and self.point.is_off:
            self._process_button_on(roll)

        elif roll is 7 and self.point.is_on:
            self._process_seven_out()

        elif roll is self.point.number:
            self._process_button_hit()

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self.point.is_on:
            self._process_button_miss()

        self._update_bets(roll)

    def _update_bets(self, roll):
        for bet in self.bets:
            winnings = bet.get_winnings(roll, self.point)
            self.pot += winnings

    def _process_easy_win(self):
        """
        Processing when 7 or 11 is rolled with the button off
        """
        print("Everyone wins!")

    def _process_crap_out(self):
        """
        Processing when 2, 3 or 12 is rolled with the button off
        """
        print("Crap out - everyone loses")

    def _process_button_on(self, roll):
        """
        Processing when the button goes on. I.e. rolled a 4, 5, 6, 8, 9 or 10
        with the button off
        """
        print("Button goes on {}".format(roll))
        self.point.put_on(roll)

    def _process_button_miss(self):
        """
        Processing when the button is on and will stay on (i.e. any number is
        rolled except the button or 7)
        """
        print("Go again...")

    def _process_button_hit(self):
        """
        Processing when the button is hit
        """
        print("Button hit - everyone wins!")
        print("Button goes off.")
        self.point.take_off()

    def _process_seven_out(self):
        """
        Processing when 7 is rolled with the button on
        """
        print("Seven out :(")
        self.seven_out = True

    def place_bets(self, bets):
        """
        Place a bet
        """
        for bet in bets:
            self.bets.append(bet)
            self.pot -= bet.amount


class Point(object):
    """
    Represents the point
    """
    def __init__(self):
        self._value = 0

    def put_on(self, value):
        self._value = value

    def take_off(self):
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


def play_game(bets, forced_rolls = None):
    """
    Helper function to run a whole game, i.e. until the shooter sevens out
    :param bets: [Bet] - Bets to be placed before the game begins
    :param forced_rolls: [int] - Fix the outcomes of the dice
    :return: int - Amount left in the player's pot after the game
    """
    game = Game()
    game.place_bets(bets)

    round_count = 0

    while not game.seven_out:

        if forced_rolls:
            forced_roll = forced_rolls[round_count]
        else:
            forced_roll = None

        game.play_round(forced_roll)
        round_count += 1

    return(game.pot)
