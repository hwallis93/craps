# TODO
# - Design for the 6 possible roll categories
# - game.print_state() to print all state
# - Add basic betting (7/11 win, crap out, button hit, 7 out)

import random

class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """
    def __init__(self):
        self.button = 0
        self.seven_out = False

    def roll_the_dice(self):
        """
        Roll a pair of fair six-sided dice
        """
        return random.randint(1,6) + random.randint(1,6)

    @property
    def button_is_off(self):
        return self.button is 0

    @property
    def button_is_on(self):
        return self.button > 0

    def play_round(self):
        """
        Play a round of craps, a single dice throw
        """

        roll = self.roll_the_dice()
        print
        print("Rolled {}".format(roll))

        if roll in [7,11] and self.button_is_off:
            self.process_easy_win()

        elif roll in [2,3,12] and self.button_is_off:
            self.process_crap_out()

        elif roll in [4,5,6,8,9,10] and self.button_is_off:
            self.process_button_on(roll)

        elif roll is 7 and self.button_is_on:
            self.process_seven_out()

        elif roll is self.button:
            self.process_button_hit()

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self.button_is_on:
            self.process_button_miss()

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
        self.button = roll

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
        self.button = 0

    def process_seven_out(self):
        """
        Processing when 7 is rolled with the button on
        :return:
        """
        print("Seven out :(")
        self.seven_out = True


def play_game():
    game = Game()

    while True:
        game.play_round()

        if game.seven_out:
            break

if __name__ == "__main__":
    play_game()