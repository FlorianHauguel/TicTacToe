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

	def DeepCopy(self):
		copy = TicTacToe()
		copy.board = self.board
		copy.turnToPlay = self.turnToPlay
		return copy

	def ChangeTurn(self):
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
			print(self.turnToPlay, 'play in', (i, j))
			self.ChangeTurn()
			return 1
				
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
		print(self.turnToPlay.name, '(',self.turnToPlay.value,') is the next player')
		print()

	def IsWinning(self):
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '':
				print('there is a win in row', i, 'for', PlayerNameFromValue(self.board[i][0]))
				return True
			if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '':
				print('there is a win in column', i, 'for', PlayerNameFromValue(self.board[0][i]))
				return True

		if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] != '':
			print('there is a win in downward diag for', PlayerNameFromValue(self.board[1][1]))
			return True

		if self.board[2][0] == self.board[1][1] == self.board[0][2] and self.board[1][1] != '':
			print('there is a win in upward diag for', PlayerNameFromValue(self.board[1][1]))
			return True

		return False



myTicTacToe = TicTacToe()
myTicTacToe.Render()

'''
for x in range(6):
	i = random.randint(0, 2)
	j = random.randint(0, 2)
	myTicTacToe.PlaceMark(i, j)
'''

while myTicTacToe.IsWinning() == False:
	case = input('Enter your choice (row, col):').split(',')
	row = int(case[0])
	col = int(case[1])
	print(row, col)
	myTicTacToe.PlaceMark(row, col)
	myTicTacToe.Render()

