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

import random
import logging
from textwrap import dedent

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

class Game(object):
    """
    Represents a game - i.e. one shooter's worth of rolls
    """
    def __init__(self):
        self.point = Point()
        self.has_sevened_out = False
        self.bets = []
        self.pot = 0

    def __repr__(self):
        return(dedent(f"""
        {self.point}
        Bets: {self.bets}
        Pot: {self.pot}
        """))

    @property
    def state(self):
        return {
            "point": self.point,
            "bets": self.bets,
            "pot": self.pot
        }

    def place_bets(self, bets):
        """
        Place some bets
        """
        logging.critical(f"Placing bets: {bets}")
        for bet in bets:
            self.bets.append(bet)


    def update(self, roll):
        """
        Update game state given a dice roll
        """
        logging.critical(f"\nStarting update from state {self}"
                         f"\nwith dice roll {roll}")

        self._update_bets(roll)

        if roll in [7,11] and self.point.is_off:
            self._process_easy_win()

        elif roll in [2,3,12] and self.point.is_off:
            self._process_crap_out()

        elif roll in [4,5,6,8,9,10] and self.point.is_off:
            self._process_point_on(roll)

        elif roll is 7 and self.point.is_on:
            self._process_seven_out()

        elif roll is self.point.number:
            self._process_button_hit()

        elif roll in [2,3,4,5,6,8,9,10,11,12] and self.point.is_on:
            self._process_button_miss()

    def _update_bets(self, roll):
        for bet in self.bets:
            bet_update = bet.update(roll, self.point)
            winnings, removed = bet_update.winnings, bet_update.removed

            if winnings:
                self.pot += winnings
            elif removed:
                self.bets.remove(bet)
                self.pot -= bet.amount

    def _process_easy_win(self):
        pass

    def _process_crap_out(self):
        pass

    def _process_point_on(self, roll):
        self.point.put_on(roll)

    def _process_seven_out(self):
        self.has_sevened_out = True

    def _process_button_hit(self):
        self.point.take_off()

    def _process_button_miss(self):
        pass


class GameManager(object):
    """
    Responsible for determining the outcome of playing multiple games under
    certain conditions
    """
    def __init__(self, fixed_dice=None):
        self.fixed_dice = fixed_dice   #TODO next - pass this multiple fixedDice (maybe make FixedDice list-y?) Need good way of testing overall

    def play_games(self, num_games, bets):
        """
        Play some games with certain bets
        :param num_games: int
        :param bets: [Bet]
        :return: Winnings
        """
        winnings = 0
        for _ in range(num_games):
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
        while not self.game.has_sevened_out:
            self._play_round(bets)

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
        logging.critical(f"Game bets - {self.game.bets}\n bets - {bets}")
        if self.game.state["bets"] != bets:
            missing_bets = [bet for bet in bets if bet not in self.game.bets]
            self.game.place_bets(missing_bets)

    def _roll_the_dice(self):
        """
        Roll a pair of fair six-sided dice
        """
        if self.fixed_dice:
            roll = self.fixed_dice.get_next_roll()
            logging.critical(f"Forced to roll {roll}")
        else:
            roll =  random.randint(1,6) + random.randint(1,6)
            logging.critical(f"Randomly rolled {roll}")

        return(roll)


class FixedDice(object):
    def __init__(self, rolls):
        self.rolls = rolls
        self.count = 0

    def get_next_roll(self):
        roll = self.rolls[self.count]
        self.count += 1
        return roll


class Point(object):
    """
    Represents the point
    """
    def __init__(self):
        self._value = 0

    def __repr__(self):
        if self.is_off:
            return("Point: Off")
        else:
            return(f"Point: {self._value}")

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
