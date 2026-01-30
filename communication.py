import socket
import json
from dataclasses import dataclass, asdict
from dacite import from_dict, Config
from enum import Enum


config = Config(cast=[Enum])


encfmt = 'utf-8'
termb = b'\0'
termi = termb[0]
buff_size = 2048


class Socket:
    def __init__(self, sock=None):
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def send(self, msg):
        msgstr = json.dumps(asdict(msg))
        data = bytes(msgstr, encoding=encfmt)
        data += termb
        totalsent = 0
        while totalsent < len(data):
            sent = self.sock.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError('Socket connection broken')
            totalsent += sent

    def recv(self, data_class):
        data = bytes()
        while not data or data[-1] != termi:
            chunk = self.sock.recv(buff_size)
            if chunk == b'':
                raise RuntimeError('Socket connection broken')
            data += chunk
        msgstr = data.decode(encoding=encfmt)[:-1]
        msgjson = json.loads(msgstr)
        msg = from_dict(data_class=data_class, data=msgjson, config=config)
        return msg


