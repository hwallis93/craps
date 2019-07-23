# TODO
# - Add basic betting sequence
# - Improve loop logic in play_game() to be neater

import random
from bets import PassLineBet

class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """
    def __init__(self, player_pot = 1000):
        self.point = Point()
        self.seven_out = False
        self.bets = []
        self.pot = player_pot

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
            self.process_easy_win()

        elif roll in [2,3,12] and self.point.is_off:
            self.process_crap_out()

        elif roll in [4,5,6,8,9,10] and self.point.is_off:
            self.process_button_on(roll)

        elif roll is 7 and self.point.is_on:
            self.process_seven_out()

        elif roll is self.point.number:
            self.process_button_hit()

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self.point.is_on:
            self.process_button_miss()

        self._update_bets(roll)

    def _update_bets(self, roll):
        for bet in self.bets:
            winnings = bet.get_winnings(roll, self.point)
            self.pot += winnings

    def process_easy_win(self):
        """
        Processing when 7 or 11 is rolled with the button off
        :return:
        """
        print("Everyone wins!")

    def process_crap_out(self):
        """
        Processing when 2, 3 or 12 is rolled with the button off
        :return:
        """
        print("Crap out - everyone loses")

    def process_button_on(self, roll):
        """
        Processing when the button goes on. I.e. rolled a 4, 5, 6, 8, 9 or 10
        with the button off
        :return:
        """
        print("Button goes on {}".format(roll))
        self.point.put_on(roll)

    def process_button_miss(self):
        """
        Processing when the button is on and will stay on (i.e. any number is
        rolled except the button or 7)
        :return:
        """
        print("Go again...")

    def process_button_hit(self):
        """
        Processing when the button is hit
        :return:
        """
        print("Button hit - everyone wins!")
        print("Button goes off.")
        self.point.take_off()

    def process_seven_out(self):
        """
        Processing when 7 is rolled with the button on
        :return:
        """
        print("Seven out :(")
        self.seven_out = True

    def place_pass_line_bet(self, amount):
        """
        Put a bet on the pass line
        """
        bet = PassLineBet(amount)
        self._store_bet(bet)

    def _store_bet(self, bet):
        """
        Save off a bet
        :param bet: A Bet object
        """
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


def play_game(forced_rolls = None):
    game = Game()

    while True:
        game.play_round()

    return(game.pot)

if __name__ == "__main__":
    play_game()
