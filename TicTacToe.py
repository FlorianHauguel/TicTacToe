import numpy as np
import enum
import random

class Player(enum.Enum):
   Player1 = 'x'
   Player2 = 'o'

def PlayerNameFromValue(val):
	if val == 'x':
		return Player.Player1.name
	if val == 'o':
		return Player.Player2.name
	return -1

class TicTacToe():
	def __init__(self):
		self.board = np.zeros((3, 3), dtype = str)
		self.turnToPlay = Player.Player1

	def LastPlayed(self):
		if self.turnToPlay == Player.Player1:
			return Player.Player2
		else:
			return Player.Player1

	def DeepCopy(self):
		copy = TicTacToe()
		for row in range(3):
			for col in range(3):
				copy.board[row][col] = self.board[row][col]
		copy.turnToPlay = self.turnToPlay
		return copy

	def SwapTurn(self):
		if self.turnToPlay == Player.Player1:
			self.turnToPlay = Player.Player2
		else:
			self.turnToPlay = Player.Player1

	def PlaceMark(self, i, j):
		if self.board[i][j] != '':
			print('cell already played')
			return -1
		else:
			self.board[i][j] = self.turnToPlay.value
			print(self.turnToPlay.value, 'play in', (i, j))
			self.SwapTurn()
			return 1
	
	def RemoveMark(self, i, j):
		self.board[i][j] = ''
		self.SwapTurn()

	def Render(self):
		print()
		print('     0   1   2', end = "")
		print()
		print('  ', '-' * 13)

		for i in range(3):
			print(i,' | ', end = "")
			for j in range(3):
				toPrint = ' '
				if self.board[i][j] != '':
					toPrint = self.board[i][j]
				print(toPrint, '| ', end = "")
			print()
			print('  ', '-' * 13)
		print()
		if self.IsWinning():
			print(self.LastPlayed().value, 'won the game')
		else:
			print(self.turnToPlay.value,'is the next player')
		print()

	def IsWinning(self):
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '':
				#print('there is a win in row', i, 'for', PlayerNameFromValue(self.board[i][0]))
				return True
			if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '':
				#print('there is a win in column', i, 'for', PlayerNameFromValue(self.board[0][i]))
				return True

		if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] != '':
			#print('there is a win in downward diag for', PlayerNameFromValue(self.board[1][1]))
			return True

		if self.board[2][0] == self.board[1][1] == self.board[0][2] and self.board[1][1] != '':
			#print('there is a win in upward diag for', PlayerNameFromValue(self.board[1][1]))
			return True

		return False

	class Tree():
		def __init__(self):
			self.TicTacToe = TicTacToe()
			self.score
			self.childs = []

	def MiniMax(self, currentPlayer, depth = 0):
		#what if the position is winning?
		if self.IsWinning():
			print('Game already won by', self.LastPlayed().value)
			return -1
		
		totalScore = 0
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == '':
					print('Depth:', depth, (i, j), 'Turn to play:', self.turnToPlay.value)
					self.PlaceMark(i, j)
					self.Render()

					if self.IsWinning(): #parent loop, we check if the last player has won.
						print(self.LastPlayed().value, 'win')
						if self.LastPlayed() == currentPlayer: # max mode
							print('parent loop: max win')
							return 1
						else:  # min mode
							print('parent loop: min win')
							return -1

					else: #we check the other player in child loop.
						copy = self.DeepCopy()
						score = copy.MiniMax(currentPlayer, depth + 1)
						print('score:', score)

						# we can do some optimization with the returned score
						if score == 1 and self.LastPlayed() == currentPlayer: # max mode
							print('child loop: this is a max match, we return', score)
							return score # OPTIMIZATION: we don't need to check the other branch, 1 is the first max, but a max, let's pick it

						if score == -1 and self.turnToPlay == currentPlayer:  # min mode
							print('child loop: this is a min match, we return', score)
							return score # OPTIMIZATION: we don't need to check the other branch, -1 is the first min, let's pick it

						# if we can't decide, we need to take the min or the max of the rest of the branches
						if self.LastPlayed() == currentPlayer:
							print(depth, 'max conf, we take the max between', totalScore, 'and', score)
							totalScore = max(totalScore, score)
						else:
							print(depth, 'min conf, we take the min between', totalScore, 'and', score)
							totalScore = min(totalScore, score)

					#let's remove the previous mark
					self.RemoveMark(i, j)

		print('all possibilities in depth', depth, 'has been checked')
		if self.turnToPlay == currentPlayer:
			print('we return the max score', totalScore)
		else:
			print('we return the min score', totalScore)
		return totalScore


def Example1(input):
	input.PlaceMark(2, 0)
	input.PlaceMark(0, 0)
	input.PlaceMark(0, 2)
	input.PlaceMark(1, 1)
	input.PlaceMark(2, 2)
	input.PlaceMark(1, 2)

def Example2(input):
	input.PlaceMark(2, 0)
	input.PlaceMark(0, 0)
	input.PlaceMark(0, 2)
	input.PlaceMark(1, 1)

myTicTacToe = TicTacToe()


Example1(myTicTacToe)

myTicTacToe.Render()



myTicTacToe.MiniMax(myTicTacToe.turnToPlay)