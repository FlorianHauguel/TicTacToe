import numpy as np

from Player import *
from TicTacTree import *

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
			#print(self.turnToPlay.value, 'play in', (i, j))
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
		elif self.IsFull():
			print('it\'s a draw')
		else:
			print(self.turnToPlay.value,'to play')
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

	def IsFull(self):
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == '':
					return False
		return True

	def IsFinished(self):
		return self.IsWinning() or self.IsFull()

	def PvP(self):
		while self.IsFinished() == False:
			coord = input('Enter your move (x, y) and h for hint:')
			if coord == 'h':
				myTree = TicTacTree(myTicTacToe)
				myTree.MiniMax(myTicTacToe.turnToPlay)
				myTree.BestMove()
				self.Render()
			else:
				x = int(coord.split(',')[0])
				y = int(coord.split(',')[1])
				print(x, y)
				self.PlaceMark(x, y)
				self.Render()
		input('Hit space to finish')

	def PvBot(self):
		while self.IsFinished() == False:
			coord = input('Enter your move (x, y):')
			x = int(coord.split(',')[0])
			y = int(coord.split(',')[1])
			print(x, y)
			self.PlaceMark(x, y)
			self.Render()

			if self.IsFinished() == False:
				myTree = TicTacTree(myTicTacToe)
				myTree.MiniMax(myTicTacToe.turnToPlay)
				bestMove = myTree.BestMove()
				self.PlaceMark(bestMove[0], bestMove[1])
				self.Render()
		input('Hit space to finish')


myTicTacToe = TicTacToe()
myTicTacToe.PvBot()

