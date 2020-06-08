import numpy as np

class TicTacTree():
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
			return -1 #shouldn't happened, and if it does this return value is wrong
		
		firstChild = True
		bestScore = 0
		bestMove = (-1, -1)

		for i in range(3):
			for j in range(3):
				if self.TicTacToe.board[i][j] == '':
					newChild = TicTacTree(self.TicTacToe)
					newChild.move = (i, j)
					newChild.TicTacToe.PlaceMark(i, j)
					self.children.append(newChild)

					if newChild.TicTacToe.IsWinning(): #parent loop, we check if the last player has won.
						if newChild.TicTacToe.LastPlayed() == currentPlayer: # max mode
							newChild.score = 1
						else:  # min mode
							newChild.score = -1
						return newChild.score

					else: #we check the other player in child loop.
						score = newChild.MiniMax(currentPlayer, depth + 1)
						newChild.score = score

						# we can do some optimization with the returned score
						if  score == 1 and newChild.TicTacToe.LastPlayed() == currentPlayer: # max mode
							return score # OPTIMIZATION: we don't need to check the other branch, 1 is the first max, but a max, let's pick it
						
						if 	score == -1 and newChild.TicTacToe.LastPlayed() != currentPlayer:  # min mode
							return score # OPTIMIZATION: we don't need to check the other branch, -1 is the first min, let's pick it
						
						# if we can't decide, we need to take the min or the max of the rest of the branches
						if firstChild:
							bestScore = newChild.score
							bestMove = newChild.move
							firstChild = False
						else:
							if newChild.TicTacToe.LastPlayed() == currentPlayer:
								bestScore = max(bestScore, score)
							else:
								bestScore = min(bestScore, score)
		return bestScore

