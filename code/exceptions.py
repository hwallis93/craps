import logging
logger = logging.getLogger(__name__)

from textwrap import dedent


class InvalidBetAmount(Exception):
    """
    Raise when a bet has a disallowed amount
    """
    def __init__(self, bet, amount, detail=None):
        self.bet = bet
        self.amount = amount
        self.detail = detail

    def __str__(self):
        return dedent(f"""
        Bet has an invalid amount.
        Bet - {self.bet}
        Amount - {self.amount}
        Detail - {self.detail or "No extra detail"}
        """)


class InvalidBetType(Exception):
    """
    Raise when a bet is not of the expected type
    """
    def __init__(self, bet, detail=None):
        self.bet = bet
        self.detail = detail

    def __str__(self):
        return dedent(f"""
        Bet is of invalid type.
        Bet - {self.bet}
        Detail - {self.detail or "Not specified"}
        """)

class InvalidRoll(Exception):
    """
    Raise when a dice roll has an invalid value
    """
    def __init__(self, roll, detail=None):
        self.roll = roll
        self.detail = detail

    def __str__(self):
        return dedent(f"""
        Dice roll has invalid value
        Roll - {self.roll}
        Detail - {self.detail or "No extra detail"}
        """)

