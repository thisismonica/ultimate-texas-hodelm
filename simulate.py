__author__ = 'monica_wang'
from ultimatepoker import Game

totalGain = 0
totalBet = 0
simulateTimes = 1000000
for i in range(simulateTimes):
    game = Game(False)
    gain, bet = game.playGame()
    totalGain += gain
    totalBet += bet


print "=============Simulation Result================"
print "Total Gain after ", simulateTimes," times Play: ", totalGain
print "Total Bet after ", simulateTimes," times Play: ", totalBet
print "Total Gain Ratio after ", simulateTimes," times Play: ", totalGain/totalBet


