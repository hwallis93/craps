# Fair dice rolls
# Button going on/off
# Basic game flow print outs, eg "crap out", "seven out", "button hit", "button on/off"
# Know when game has ended (7 out)
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
        print "Rolled {}".format(roll)

        if roll in [7,11] and self.button_is_off:
            print "Everyone wins!"

        elif roll in [2,3,12] and self.button_is_off:
            print "Crap out - everyone loses"

        elif roll in [4,5,6,8,9,10] and self.button_is_off:
            print "Button goes on {}".format(roll)
            self.button = roll

        elif roll is 7 and self.button_is_on:
            print "Seven out :("
            self.seven_out = True

        elif roll is self.button:
            print "Button hit - everyone wins!"
            print "Button goes off."
            self.button = 0

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self.button_is_on:
            print "Go again..."



def play_game():
    game = Game()

    while True:
        game.play_round()

        if game.seven_out:
            break

play_game()

