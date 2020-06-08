import numpy as np
import enum
import random
import operator

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
				myTree = Tree(myTicTacToe)
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
				myTree = Tree(myTicTacToe)
				myTree.MiniMax(myTicTacToe.turnToPlay)
				bestMove = myTree.BestMove()
				self.PlaceMark(bestMove[0], bestMove[1])
				self.Render()
		input('Hit space to finish')

class Tree():
	def __init__(self, ticTac):
		self.TicTacToe = ticTac.DeepCopy()
		self.score = 0
		self.move = (-1, -1)
		self.children = []

	def BestMove(self):
		bestChild = max(self.children, key=lambda item: item.score)
		print('best move is', bestChild.move, 'score:', bestChild.score)
		return bestChild.move

	def Child(self, x, y):
		for child in self.children:
			if child.move == (x, y):
				return child
		print('couldn\'t find the child', (x, y))
		return

	def MiniMax(self, currentPlayer, depth = 0):
		#what if the position is winning?
		if self.TicTacToe.IsWinning():
			#print('Game already won by', self.TicTacToe.LastPlayed().value)
			return -1 #shouldn't happened, and if it does this return value is wrong
		
		firstChild = True
		bestScore = 0
		bestMove = (-1, -1)

		for i in range(3):
			for j in range(3):
				if self.TicTacToe.board[i][j] == '':
					newChild = Tree(self.TicTacToe)
					newChild.move = (i, j)
					#print('Depth:', depth, (i, j), 'Turn to play:', newChild.TicTacToe.turnToPlay.value)
					#input('Press Enter...')
					newChild.TicTacToe.PlaceMark(i, j)

					self.children.append(newChild)

					#newChild.TicTacToe.Render()

					if newChild.TicTacToe.IsWinning(): #parent loop, we check if the last player has won.
						#print(newChild.TicTacToe.LastPlayed().value, 'win')
						#input('Press Enter...')
						if newChild.TicTacToe.LastPlayed() == currentPlayer: # max mode
							#print('parent loop: max win')
							#input('Press Enter...')
							newChild.score = 1
						else:  # min mode
							#print('parent loop: min win')
							#input('Press Enter...')
							newChild.score = -1
						return newChild.score

					else: #we check the other player in child loop.
						score = newChild.MiniMax(currentPlayer, depth + 1)
						newChild.score = score
						#print('score:', score)
						#print('last played', newChild.TicTacToe.LastPlayed())
						#print('we check for', currentPlayer)
						#input('Press Enter...')

						# we can do some optimization with the returned score
						if  score == 1 and newChild.TicTacToe.LastPlayed() == currentPlayer: # max mode
							#print('child loop: this is a match, we return', newChild.score)
							#input('Press Enter...')
							return score # OPTIMIZATION: we don't need to check the other branch, 1 is the first max, but a max, let's pick it
						
						if 	score == -1 and newChild.TicTacToe.LastPlayed() != currentPlayer:  # min mode
							#print('child loop: this is a min match, we return', newChild.score)
							#input('Press Enter...')
							return score # OPTIMIZATION: we don't need to check the other branch, -1 is the first min, let's pick it
						
						# if we can't decide, we need to take the min or the max of the rest of the branches
						if firstChild:
							bestScore = newChild.score
							bestMove = newChild.move
							firstChild = False
							#print('first child, we take it as best score for now...', bestScore, ':', bestMove)
							#input('Press Enter...')
						else:
							if newChild.TicTacToe.LastPlayed() == currentPlayer:
								#print(depth, 'max conf, we take the max between', bestScore, 'and', score)
								#input('Press Enter...')
								bestScore = max(bestScore, score)
							else:
								#print(depth, 'min conf, we take the min between', bestScore, 'and', score)
								#input('Press Enter...')
								bestScore = min(bestScore, score)

		#print('Return total score', bestScore)
		#input('Press Enter...')
		return bestScore


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

def Example3(input):
	input.PlaceMark(0, 0)
	input.PlaceMark(1, 1)
	input.PlaceMark(2, 2)
	input.PlaceMark(2, 0)

myTicTacToe = TicTacToe()
myTicTacToe.PvBot()






'''
Example3(myTicTacToe)
myTicTacToe.Render()


myTree = Tree(myTicTacToe)
myTree.MiniMax()
myTicTacToe.Render()
myTree.BestMove()

for child in myTree.children:
	print(child.score, child.move)

print(myTree.Child(0,2))
'''


