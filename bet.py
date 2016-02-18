__author__ = 'monica_wang'

class Bet:
    def __init__(self, unit):
        self.ante = unit

        # blind matches ante
        self.blind = self.ante

        # play bet initial zero
        self.play = 0