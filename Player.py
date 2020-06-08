import enum

class Player(enum.Enum):
   Player1 = 'x'
   Player2 = 'o'

def PlayerNameFromValue(val):
	if val == 'x':
		return Player.Player1.name
	if val == 'o':
		return Player.Player2.name
	return -1
