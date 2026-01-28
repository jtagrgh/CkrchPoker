import socket
import common

client = common.Socket()
client.connect('localhost', 7778)

client.send(b'Jakob')

data = client.recv()
msg = common.HandInitMessage()
msg.decode(data)

