__author__ = 'monica_wang'

from deck import Deck
from bet import Bet
import strategy
from hand import Hand
from hand import compareHands
from hand import HandType
from BlindBetTable import BlindBet

class Game:
    def __init__(self, stdout):
        self._deck = Deck(1)
        self._deck.shuffle()
        self._bet = Bet(1.0)
        self._dealer = []
        self._player = []
        self._community = []
        self._gain = 0
        self.stdout = stdout

    def startRound1(self):
        self._player += self._deck.draw(2)
        self._dealer += self._deck.draw(2)
        self._bet.play = strategy.round1Bet(self._player)  # 0 or 4
        if self.stdout:
            print "***************************"
            print "Round1: "
            print "Dealer: " + ", ".join([str(c) for c in self._dealer])
            print "Player: " + ", ".join([str(c) for c in self._player])
            print "==Play Bet=="
            print "\t", self._bet.play

    def startRound2(self):
        self._community += self._deck.draw(3)
        if self._bet.play == 0:
            self._bet.play = strategy.round2Bet(self._player, self._community)
        if self.stdout:
            print "\nRound2: "
            print "Dealer: " + ", ".join([str(c) for c in self._dealer])
            print "Player: " + ", ".join([str(c) for c in self._player])
            print "Community: " + ", ".join([str(c) for c in self._community])
            print "==Play Bet=="
            print "\t", self._bet.play

    def startRound3(self):
        self._community += self._deck.draw(2)
        self._playerHand = Hand(self._player+self._community)
        self._dealerHand = Hand(self._dealer+self._community)

        if self.stdout:
            print "\nRound3: "
            print "Community: " + ", ".join([str(c) for c in self._community])
            print "Dealer Hand: " + str(self._dealerHand)
            print "Player Hand: " + str(self._playerHand)
            if self._dealerHand.type < HandType.PAIR:
                print "...Ante Push..."

        if self._bet.play != 0:
            result = compareHands(self._playerHand, self._dealerHand)
            if result == 1:
                self._gain = self.gainFromWin()
                if self.stdout:
                    print "Player Win!"
            elif result == -1:
                self._gain = self.gainFromLose()
                if self.stdout:
                    print "Player Lose!"
            else:
                self._gain = 0
                if self.stdout:
                    print "Push"
        else:
            self._gain = self.gainFromLose()
            if self.stdout:
                print "Player Fold!"


    def gainFromWin(self):
        res = self._bet.play + BlindBet.Table[self._playerHand.type] * self._bet.blind
        res += self._bet.ante if self._dealerHand.type >= HandType.PAIR else 0
        return res

    def gainFromLose(self):
         res = 0 - self._bet.play - self._bet.blind
         res -= self._bet.ante if self._dealerHand.type >= HandType.PAIR else 0
         return res

    def playGame(self):
        self.startRound1()
        self.startRound2()
        self.startRound3()
        if self.stdout:
            print "\n==GAIN THIS ROUND=="
            print "\t", self._gain
        return self._gain, (self._bet.blind + self._bet.ante + self._bet.play)

if __name__ == '__main__':
    game = Game()
    game.playGame()
