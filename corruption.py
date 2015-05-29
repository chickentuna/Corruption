import sys

def log(t):
    print(t, file=sys.stderr)

CORRUPTION_TIME = 3
ORC_TIME = 5
FOREST_TIME = 2
#FOREST_HP = 1

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
    def move(self, direction, bounds):
        if direction == 'RIGHT':
            self.x += 1
        elif direction == 'LEFT':
            self.x -= 1
        elif direction == 'DOWN':
            self.y += 1
        elif direction == 'UP':
            self.y-= 1
        else:
            log('invalid move')
        if self.x < 0 or self.y < 0 or self.x > bounds.width or self.y > bounds.height:
            log('moved out of bounds')

class Cell(Coord):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.forest = False
        self.corrupted = False
        self.elves = 0
        self.orcs = 0
        self.tower = False
        self.rivendell = False        

class Grid(object):
    def __init__(self, w, h):
        self.height = h
        self.width = w
        self.array = [[Cell(x,y) for x in range(w)] for y in range(h)]
    def get(self, arg1, arg2=0):
        if isinstance(arg1, Coord):
            x = arg1.x
            y = arg1.y
        else:
            x = arg1
            y = arg2
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return self.array[y][x]
        return None


class Game(object):
    def __init__(self):
        #construction of a mockup map
        self.elves = [Coord(0,9),Coord(0,9),Coord(0,9)]
        self.towers = [Coord(9,0)]
        self.orcs = []
        self.forests = []
        self.land = Grid(10,10)
        
        forests = self.forests
        elves = self.elves
        towers = self.elves
        land = self.land

        land.get(0,9).rivendell = True
        for i in range(10):
            land.get(i,i).forest = True
            forests.append(Coord(i,i))
        for elf in elves:
            land.get(elf).elves += 1
        for tower in towers:
            land.get(tower).tower = True

        turn = 0
        dead = False
        countDown = {
            'corruption': CORRUPTION_TIME,
            'orc': ORC_TIME
        }
        self.sendInitInfo()
        while not dead:
            turn += 1
            self.sendTurnInfo()
            commands = self.getInstructions()
            if len(commands) != len(elves):
                dead = True
                continue    
            
            #move elves
            for i in range(commands):
                elf = elves[i]
                command = commands[i]
                if command != 'WAIT':
                    map.get(elf).elves -= 1
                    elf.move(command, land)
                    map.get(elf).elves += 1
            #move orcs
            for orc in orc:
                #move to closest tree
                pass
            #spread corruption
            countDown['corruption'] -= 1
            if countDown['corruption'] == 0:
                countDown['corruption'] = CORRUPTION_TIME
                pass
            #spawn orcs
            countDown['orc'] -= 1
            if countDown['orc'] == 0:
                countDown['orc'] = ORC_TIME
                pass
            #spread forests
            pass
        
    def sendInitInfo(self):
        land = self.land
        elves = self.elves
        print(land.width,land.height, len(elves))
        for row in land.array:
            out = ''
            for cell in row:
                if cell.tower:
                    out += 'T'
                elif cell.forest:
                    out += 'F'
                elif cell.rivendell:
                    out += 'R'
                elif cell.corrupted:
                    out += '#'
                else:
                    out += ' '
            print(out)
        for elf in elves:
            print(elf.x, elf.y)
        

    def sendTurnInfo(self):
        orcs = self.orcs
        print(len(orcs))
        for orc in orcs:
            print(orc.x, orc.y)

    def getInstructions(self):
        return  ['WAIT','WAIT','WAIT']

if __name__ == '__main__':
    game = Game()


    

