import socket
from communication import Socket
from messagetypes import Name, Game
from dacite import from_dict, Config
from enum import Enum


client = Socket()
client.connect('localhost', 7778)

client.send(Name('Jakob'))

game = client.recv(Game)

print(game)
