import numpy as np
import enum

class Player(enum.Enum):
   Player1 = 'x'
   Player2 = 'o'

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
		print('  ', '-' * 12)

		for i in range(3):
			print(i,' | ', end = "")
			for j in range(3):
				print(self.board[i][j], ' | ', end = "")
			print()
			print('  ', '-' * 12)
		print()
		print(self.turnToPlay.name, '(',self.turnToPlay.value,') is the next player')
		print()

	def IsWinning(self):
		# checking result in rows
		for row in range(MaxRow):
			for col in range(MaxCol - 4):
				if self.board[row][col] != '' and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
					print('there is a win in row', row, 'col from', col, col + 3, 'for', PlayerNameFromValue(self.board[row][col]))
					return True

		# checking result in columns
		for col in range(MaxCol):
			for row in range(MaxRow - 4):
				if self.board[row][col] != '' and self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
					print('there is a win in column', col, 'row from', row, row + 3, 'for', PlayerNameFromValue(self.board[row][col]))
					return True

		# checking result in upward diagonals
		for row in range (3):
			for col in range(4):
				if self.board[row][col] != '' and self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
					print('there is a win in upward diagonal from', (row, col), 'to', (row + 3, col + 3), 'for', PlayerNameFromValue(self.board[row][col]))
					return True

		# checking result in downward diagonals
		for row in range (MaxRow - 1, 2, -1):
			for col in range(4):
				if self.board[row][col] != '' and self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3]:
					print('there is a win in downward diagonal from', (row, col), 'to', (row - 3, col + 3), 'for', PlayerNameFromValue(self.board[row][col]))
					return True

		return False



myTicTacToe = TicTacToe()
myTicTacToe.Render()