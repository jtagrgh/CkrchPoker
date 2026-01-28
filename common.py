import socket

max_data_size = 1024

termch = b'\0'
termi = termch[0]

delims = ['_', ':', ';', ',']
encfmt = 'utf-8'


def encode(obj):
    return bytes(obj.pack(), encoding=encfmt)


def decode(data, obj):
    return obj.unpack(data.decode(encoding=encfmt))


class Creature:
    def __init__(self, name='none', code='X'):
        self.name = name
        self.code = code

    def __repr__(self):
        return self.pack()

    def pack(self, idx=0):
        return delims[idx].join([self.name, self.code])

    def unpack(self, data, idx=0):
        self.name, self.code = data.split(delims[idx])
        return self


class CardStack:
    def __init__(self, creature=Creature(), count=0):
        self.creature = creature
        self.count = count

    def __repr__(self):
        return self.pack()

    def pack(self, idx=0):
        return delims[idx].join([
            self.creature.pack(idx+1), str(self.count)])

    def unpack(self, data, idx=0):
        items = data.split(delims[idx])
        self.creature = Creature().unpack(items[0], idx+1)
        self.count = int(items[1])
        return self


class CardRow:
    def __init__(self, stacks=[CardStack()]):
        self.stacks = stacks

    def __repr__(self):
        return self.pack()

    def pack(self, idx=0):
        return delims[idx].join([stack.pack(idx+1) for stack in self.stacks])

    def unpack(self, data, idx=0):
        items = data.split(delims[idx])
        self.stacks = []
        for item in items:
            self.stacks.append(CardStack().unpack(item, idx+1))
        return self


class PlayerName:
    def __init__(self, name='defaultuser'):
        self.name = name

    def __repr__(self):
        return self.name

    def pack(self, idx=0):
        return self.name

    def unpack(self, data, idx=0):
        self.name = data
        return self


class PlayerState:
    def __init__(self, name=PlayerName(), hand=CardRow(), board=CardRow()):
        self.name = name
        self.hand = hand
        self.board = board

    def __repr__(self):
        return self.pack()

    def pack(self, idx=0):
        return delims[idx].join([
            self.name.pack(idx+1),
            self.hand.pack(idx+1), 
            self.board.pack(idx+1)])

    def unpack(self, data, idx=0):
        items = data.split(delims[idx])
        self.name = PlayerName().unpack(items[0], idx+1)
        self.hand = CardRow().unpack(items[1], idx+1)
        self.board = CardRow().unpack(items[2], idx+1)
        return self


caterpiller = Creature('caterpiller', '\U0001F41B')
ladybug = Creature('ladybug', '\U0001F41E')
scorpion = Creature('scorpion', '\U0001F982')
bat = Creature('bat', '\U0001F987')
mouse = Creature('mouse', '\U0001F42D')
cricket = Creature('cricket', '\U0001F41C')
frog = Creature('frog', '\U0001F438')
spider = Creature('spider', '\U0001F577')
error = Creature('error', 'X')

creatures = [caterpiller, ladybug, scorpion, bat, mouse, cricket, frog, spider]

creature_names = {creature.name : creature for creature in creatures}

class Socket:
    def __init__(self, sock=None):
        if sock:
            self.sock = sock
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data):
        data += b'\0'
        totalsent = 0
        while totalsent < len(data):
            sent = self.sock.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError('Socket connection broken')
            totalsent += sent

    def recv(self):
        data = bytes()
        while not data or data[-1] != termi:
            chunk = self.sock.recv(max_data_size - len(data))
            if chunk == b'':
                raise RuntimeError('Socket connection broken')
            data += chunk
        return data




'''
class CreatureMsg:
    def __init__(self, creature=error, count=0):
        self.name = creature.name
        self.count = count

    def encode(self):
        return encode(self.name, self.count)

    def decode(self, data):
        self.name, self.count = decode(data)

class CreatureCount:
    def __init__(self, creature=error, count=0):
        self.name = creature
        self.count = str(count)

class HandInitMessage:
    def __init__(self, creatures=[CreatureCount()], starting=False):
        self.creatures = creatures
        self.starting = starting

    def encode(self):
        datastr = ''
        for creature in self.creatures:
            datastr += creature.creature.name + delim1 + creature.count + delim2
        datastr += '1' if self.starting else '0'
        return bytes(datastr, encoding=encfmt)

    def decode(self, data):
        segs = data.decode().spilt(delim2)
        self.starting = True if segs[-1] == '1' else False
        self.creatures = []
        for seg in segs[:-1]:
            name, count = seg.spilt(delim1)
            creature = creature_names[name]
            count = int(count)
            creature_count = CreatureCount(creature, count)
            self.creatures.append(creature_count)
'''
