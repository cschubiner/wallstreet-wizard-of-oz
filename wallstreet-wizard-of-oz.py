ROLES = ['taxman', 'auditor', 'monopolist', 'transferer']


import random
def shuffle(arr):
    for i in range(len(arr)):
        swapPos = random.randint(i, len(arr)-1)
        arr[i], arr[swapPos] = arr[swapPos], arr[i]


class Player:
    def __init__(self,role, name):
        self.role = role
        self.name = (name[0].upper() + name[1:].lower()).strip()
        self.money = 0

def getInt(msg):
    while True:
        ret = None
        try:
            ret = raw_input(msg + ": ")
            ret = int(ret)
            return ret
        except Exception, e:
          pass

def getNames(msg, numPpl):
    while True:
      ret = None
      try:
          ret = raw_input(msg + ": ")
          ret = ret.split()
          if len(ret) != numPpl:
            raise "hisdf"
          return ret
      except Exception, e:
        pass

def printMoney(players, turn):
    print 'Total money after turn',turn
    for p in players:
        print p.name,':',p.money

def getPlayerName(players, msg):
    nameSet = set()
    for p in players:
        nameSet.add(p.name.upper().strip())
    while True:
        ret = raw_input(msg + ": ").upper().strip()
        if ret in nameSet:
            return ret

def getPlayerByRole(players, role):
    for p in players:
        if p.role.upper().strip() == role.upper().strip() :
            return p

def getPlayerByName(players, name):
    for p in players:
        if p.name.upper().strip() == name.upper().strip():
            return p

numPpl = getInt('Enter num ppl')
names = getNames('Enter ppl names (space delimited)', numPpl)
shuffle(names)
players = list()
for i in range(numPpl):
    p = Player(role=ROLES[i], name=names[i])
    players.append(p)
shuffle(players)

turn = 0
for i in range(4):
    for p in players:
        p.money += 2

    for i in range(len(ROLES)):
        role = ROLES[i]
        if role == 'auditor':
            continue
        p = getPlayerByRole(players, role)
        print p.name, "'s turn (",role,')'
        targetName = getPlayerName(players, 'Input target player')
        t = getPlayerByName(players, targetName)
        if role == 'taxman':
            p.money += 1
            t.money -= 1
        if role == 'transferer':
            p.money -= 1
            t.money += 1
        if role == 'monopolist':
            t.money -= 1

    printMoney(players, turn)
