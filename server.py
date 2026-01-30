import socket
from communication import Socket
from dacite import from_dict
from messagetypes import Name, Turn, Game, Claim, Guess
from gametypes import Creature, Card, CardRow, Player, TotalGame
from random import shuffle, randint
from collections import Counter
import creatures


n_clients = 1
creature_list = [creatures.BUG, creatures.ANT, creatures.BAT]


def new_game() -> TotalGame:
    mix = []

    for creature in creature_list:
        mix.extend([creature]*8)

    shuffle(mix)

    pile = mix[:10]
    mix = mix[10:]

    freq1 = Counter(mix[:27])
    freq2 = Counter(mix[27:])

    if creatures.BUG in freq1:
        del freq1[creatures.BUG]

    for creature in creature_list:
        if creature not in freq1:
            freq1[creature] = 0
        if creature not in freq2:
            freq2[creature] = 0

    hand1 = [Card(creature, count) for creature,count in freq1.items()]
    hand2 = [Card(creature, count) for creature,count in freq2.items()]

    cmp = lambda x: x.creature.name

    hand1.sort(key=cmp)
    hand2.sort(key=cmp)

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


def game_won(game: TotalGame) -> bool:
    cards = game.player0.board.cards + game.player1.board.cards
    return any(card.count >= 4 for card in cards)


if __name__ == '__main__':
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

        print(game)

        for i, client in enumerate(clients):
            msg = game_msg(i, game)
            msg.turn = Turn.GUESS # TODO: REMOVE
            client.send(msg)
            claim = Claim(creatures.BUG, creatures.ANT)
            client.send(claim)

            guess = client.recv(Guess)

            print(guess)

        input()
