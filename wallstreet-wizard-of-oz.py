ROLES = ['taxman', 'auditor', 'monopolist', 'transferer']


import random,sys



fIn = None
fOut = None
if len(sys.argv) != 1 and len(sys.argv) != 3:
    print 'Usage: python wallstreet-wizard-of-oz.py ([INPUT_FILE]) ([OUTPUT_FILE])'
    exit()

usingFiles = len(sys.argv) > 1

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

def printAndWrite(msg):
    s = msg
    if isinstance(msg, list):
        s = ' '.join(str(x) for x in msg)
    if usingFiles:
        fOut.write(s + '\n')
    print s

def printMoney(players, turn):
    s = 'Total money after turn ' + str(turn)
    if usingFiles:
        fOut.write(s + '\n')
    print s
    for p in players:
        printAndWrite([p.name,':',p.money])

def getPlayerName(players, msg, allowSkip = False):
    nameSet = set()
    for p in players:
        nameSet.add(p.name.upper().strip())
    while True:
        ret = raw_input(msg + ": ").upper().strip()
        if ret == "SKIP" or ret == 'S':
            return False
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

if usingFiles:
    fIn = open(sys.argv[1],'r')
    fOut = open(sys.argv[2],'w')

numPpl = getInt('Enter num ppl')
names = getNames('Enter ppl names (space delimited)', numPpl)
shuffle(names)
players = list()
for i in range(numPpl):
    p = Player(role=ROLES[i], name=names[i])
    players.append(p)
shuffle(players)

turn = 0

for i in range(10):
    for p in players:
        p.money += 2

    for i in range(min(len(ROLES), numPpl)):
        role = ROLES[i]
        if role == 'auditor':
            continue
        p = getPlayerByRole(players, role)
        print p.name, "'s turn (",role,')'
        targetName = getPlayerName(players, 'Input target player', True)
        if targetName == False:
            continue

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
if usingFiles:
    fIn.close()
    fOut.close()
