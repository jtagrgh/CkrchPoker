import socket
from communication import Socket
from dacite import from_dict
from messagetypes import Name, Turn, Game
from gametypes import Creature, Card, CardRow, Player, TotalGame
from random import shuffle, randint
from collections import Counter
import creatures


n_clients = 1
creature_list = [creatures.BUG, creatures.FLY, creatures.RAT]


def new_game() -> TotalGame:
    mix = []

    for creature in creature_list:
        mix.extend([creature]*8)

    shuffle(mix)

    pile = mix[:10]
    mix = mix[10:]

    freq1 = Counter(mix[:27])
    freq2 = Counter(mix[27:])

    hand1 = [Card(creature, count) for creature,count in freq1.items()]
    hand2 = [Card(creature, count) for creature,count in freq2.items()]

    player1 = Player(CardRow([]), CardRow(hand1))
    player2 = Player(CardRow([]), CardRow(hand2))

    claim_player = randint(0,1)

    game = TotalGame(claim_player, player1, player2)

    return game


def game_msg(idx: int, game: TotalGame) -> Game:
    turn = Turn.CLAIM if idx == game.claim_player else Turn.GUESS

    if idx == 0:
        opp_board = game.player1.board
        board = game.player0.board
        hand = game.player0.hand
    elif idx == 1:
        opp_board = game.player0.board
        board = game.player1.board
        hand = game.player1.hand

    game_msg = Game(turn, opp_board, board, hand)

    return game_msg


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('localhost', 7778))
    server.listen(n_clients)

    clients = []

    for _ in range(n_clients):
        (socket, addr) = server.accept()
        client = Socket(socket)

        name = client.recv(Name)

        print(f'<{name.name}> has connected')

        clients.append(client)
    
    print('All clients connected. Beginning game.')

    game = new_game()

    msg0 = game_msg(0, game)

    clients[0].send(msg0)

