from common import *

name = PlayerName('Jakob')
hand = CardRow([CardStack(Creature('fly','YY'), 5), CardStack(Creature('bat', '1234'), 1)])
board = CardRow([CardStack(Creature('caterpiller'))])

state = PlayerState(name, hand, board)

pack = state.pack()

print(PlayerState().unpack(pack))


