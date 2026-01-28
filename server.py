import socket
import common

n_clients = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('localhost', 7778))
    server.listen(n_clients)

    clients = []

    for _ in range(n_clients):
        (socket, addr) = server.accept()
        client = common.Socket(socket)
        data = client.recv()
        name = data.decode()
        clients.append(socket)
        msg = common.HandInitMessage()
        client.send(msg.encode())
        print(f'Recieved client <{name}> at <{addr}>. Total clients <{len(clients)}>')
    
    print('All clients connected. Beginning game.')

