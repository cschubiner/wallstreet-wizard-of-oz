R_RZ = 'Rabid Zombie'
R_ZC = 'Zombie Consort'
R_S = 'Sheriff'
R_D = 'Doctor'
R_C = 'Crier'

ROLES = [R_RZ, R_ZC, R_S, R_S, R_D, R_C]

names = ['Lawrence','Raissa','Doug','Kyle','Dartis','Lexxie']

inputPlayers = True

numPpl = len(names)
import random,sys



fIn = None
fOut = None
if len(sys.argv) != 1 and len(sys.argv) != 3:
    print 'Usage: python zombie-wizard-of-oz.py ([INPUT_FILE]) ([OUTPUT_FILE])'
    exit()

usingFiles = len(sys.argv) > 1

def shortToRole(s):
    for r in ROLES:
        if r.lower().startswith(s.lower()):
            return r

def shortToPlayer(s):
    for r in names:
        if r.lower().startswith(s.lower()):
            return r

def shuffle(arr):
    for i in range(len(arr)):
        swapPos = random.randint(i, len(arr)-1)
        arr[i], arr[swapPos] = arr[swapPos], arr[i]


class Player:
    def __init__(self,role, name):
        self.role = role
        self.name = (name[0].upper() + name[1:].lower()).strip()
        self.clear()
    def clear(self):
        self.infected = False
        self.healed = False
        self.blocked = False
        self.inspectionResults = None
        self.target = None
        self.didHeal = False


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


def getPlayerName(players, msg, allowSkip = False):
    # nameSet = set()
    # for p in players:
    #     nameSet.add(p.name.upper().strip())
    while True:
        ret = raw_input(msg + ": ").upper().strip()
        if ret == "SKIP" or ret == 'S':
            return False
        # if ret in nameSet:
            # return ret
        if len(ret) > 1:
            return ret

def getPlayersByRole(players, role):
    ret = list()
    for p in players:
        if p.role.upper().strip() == role.upper().strip():
            ret.append(p)
    return ret

def getPlayerByName(players, name):
    nname = shortToPlayer(name.upper().strip())
    if not nname:
        return None
    for p in players:
        if p.name.upper().strip() == nname.upper().strip():
            return p

def getInspectionResults(targetPlayer):
    ret = None
    if targetPlayer.role == R_ZC or targetPlayer.role == R_D:
        ret = [R_ZC, R_D]
    if targetPlayer.role == R_C:
        ret = [R_C]
    if targetPlayer.role == R_RZ or targetPlayer.role == R_S:
        ret = [R_RZ, R_S]

    shuffle(ret)
    return targetPlayer.name + ' == ' + '/'.join(ret) + '.'

if usingFiles:
    fIn = open(sys.argv[1],'r')
    fOut = open(sys.argv[2],'w')

players = list()
if inputPlayers:
    for r in ROLES:
        print r, ' ',
    print '\n'
    for name in names:
        while True:
            ret = raw_input("Enter " + name + "'s role: ").upper().strip()
            r = shortToRole(ret)
            if r:
                print name + "'s role is: " + r
                p = Player(role=r, name=name)
                players.append(p)
                break
else:
    shuffle(names)
    for i in range(numPpl):
        p = Player(role=ROLES[i], name=names[i])
        players.append(p)
    for i in range(min(len(ROLES), numPpl)):
        role = ROLES[i]
        p = getPlayersByRole(players, role)
        # broken
        print p.name, "(",role,')'

print getPlayersByRole(players, R_ZC)
print getPlayersByRole(players, R_S)
turn = 0
for i in range(10):
    playersLeft = set()
    for p in players:
        playersLeft.add(p)
        p.clear()
    while len(playersLeft) > 0:
        print '\nStill awaiting actions for:'
        for p in playersLeft:
            print p.name, ' ',
        print
        pName = getPlayerName(players, 'Input player', True)
        if pName == False:
            continue
        p = getPlayerByName(players, pName)
        if not p:
            continue

        if p.role == R_C:
            print 'No action for', p.role
            playersLeft.remove(p)
            continue

        tName = getPlayerName(players, 'Input target player', True)
        if tName == False:
            continue
        t = getPlayerByName(players, tName)
        if not t:
            continue
        p.target = t
        playersLeft.remove(p)

    # print results
    for p in getPlayersByRole(players, R_ZC):
        p.target.blocked = True
    for p in getPlayersByRole(players, R_RZ):
        if not p.blocked:
            p.target.infected = True
    for p in getPlayersByRole(players, R_S):
        if not p.blocked:
            p.inspectionResults = getInspectionResults(p.target)
    for p in getPlayersByRole(players, R_D):
        if not p.blocked:
            p.target.healed = True
            if p.target.infected:
                p.didHeal = True

    for p in players:
        print p.name, '--',p.role
        statuses = list()
        if p.infected and not p.healed:
            statuses.append('You are INFECTED.')
        if p.blocked:
            statuses.append('You were roleblocked.')
        else:
            if p.inspectionResults:
                statuses.append(p.inspectionResults)
            if p.didHeal:
                statuses.append('You healed his/her infection!')

        print ' '.join(statuses)
        print '\n'

if usingFiles:
    fIn.close()
    fOut.close()
