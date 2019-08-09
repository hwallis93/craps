from textwrap import dedent

class InvalidBetAmount(Exception):
    """
    Raise when attempting to create a bet with a disallowed amount
    """
    def __init__(self, bet, amount):
        self.bet = bet
        self.amount = amount

    def __str__(self):
        return(dedent("""
            Attempted to create a bet with an invalid amount:
            Bet type - {bet}
            Amount - {amount}""").format(
            bet=self.bet,amount=self.amount))

class InvalidBetType(Exception):
    """
    Raise when a bet is not of the expected type
    """
    pass

class InvalidRoll(Exception):
    """
    A dice roll has an invalid value
    """
    pass
