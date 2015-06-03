import sys
import os
import time
from random import choice, randrange, seed

def log(t):
    print(t, file=sys.stderr)

CORRUPTION_TIME = 3
ORC_TIME = 12
#FOREST_TIME = 2

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target = None
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return self.x * 2 + self.y * 3
    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
    def distanceTo(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    def move(self, direction, bounds=None):
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
        if bounds is not None and (self.x < 0 or self.y < 0 or self.x > bounds.width or self.y > bounds.height):
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
        self.targetedBy = None
    def battle(self):
        return self.orcs > 0 and self.elves > 0
    def getNeighbours(self, land):
        x = self.x
        y = self.y
        up = land.get(x,y-1)
        left = land.get(x-1,y)
        down = land.get(x,y+1)
        right = land.get(x+1,y)
        return [i for i in (up,left,down,right) if (i is not None)]
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
        self.land = Grid(60,6)
        self.elves = []
        self.towers = []
        self.orcs = []
        self.forests = []
        
        forests = self.forests
        elves = self.elves
        towers = self.towers
        land = self.land
        orcs = self.orcs
        self.generateMap()

        self.rivendell.rivendell = True        
        for elf in elves:
            land.get(elf).elves += 1
        for orc in orcs:
            land.get(orc).orcs += 1
        for tower in towers:
            tower.tower = True
            tower.corrupted = True
        for forest in forests:
            forest.forest = True

        turn = 0
        dead = False
        self.corruptionTime = CORRUPTION_TIME
        self.orcTime = ORC_TIME

        self.sendInitInfo()
        self.sendTurnInfo()
        while not dead:
            turn += 1
            time.sleep (.2);
            commands = self.getInstructions()
            if len(commands) != len(elves):
                dead = True
                continue

            self.moveElves(commands)
            self.moveOrcs()
            self.trainOrcs()
            self.combat()
            self.spreadCorruption()
            self.spreadForests()
            if self.rivendell.corrupted:
                dead = True
            self.sendTurnInfo()
        print ('You survived',turn,'turns.')

    def generateMap(self):
        land = self.land
        elves = self.elves
        towers = self.towers
        forests = self.forests

        elfCount = int(min(land.height, land.width) / 2) - 1
        self.rivendell = land.get(0, randrange(land.height / 3, 2 * land.height / 3))
        t = land.get(land.width-1, randrange(land.height / 3, 2 * land.height / 3))
        towers.append(t)
        for i in range(elfCount):
            elves.append(Coord(0, self.rivendell.y))
        forestCount = randrange(land.height, pow(land.height, 2))
        saplings = set()
        for i in range(forestCount):
            x = randrange(1, land.width - 1)
            y = randrange(0, land.height)
            saplings.add(land.get(x,y))
        for sapling in saplings:
            forests.append(sapling)

    def spreadForests(self):
        forests = self.forests
        elves = self.elves
        land = self.land
        
        spreadTo = set()
        for forest in forests:
            if forest.elves > 0 and not forest.battle():
                for neighbour in forest.getNeighbours(land):
                    spreadTo.add(neighbour)
        for cell in spreadTo:
            if not cell.tower and not cell.rivendell and not cell.forest:
                cell.corrupted = False
                cell.forest = True
                forests.append(cell)

    def trainOrcs(self):
        self.orcTime -= 1
        if self.orcTime == 0:
            self.orcTime = ORC_TIME
            for tower in self.towers:
                tower.orcs += 1
                self.orcs.append(Coord(tower.x, tower.y))
    def combat(self):
        orcs = self.orcs
        forests = self.forests
        land = self.land

        mills = set()
        for orc in orcs:
            cell = land.get(orc)
            if cell.forest:
                if cell.elves < cell.orcs:
                    mills.add(cell)
        for forest in mills:
            forests.remove(forest)
            forest.forest = False
    def spreadCorruption(self):
        land = self.land

        self.corruptionTime -= 1
        if self.corruptionTime == 0:
            self.corruptionTime = CORRUPTION_TIME
            toCorrupt = set()
            for x in range(land.width):
                for y in range(land.height):
                    cell = land.get(x,y)
                    if cell.corrupted:
                        for neighbour in cell.getNeighbours(land):
                            toCorrupt.add(neighbour)
            for cell in toCorrupt:
                if not cell.forest:
                    cell.corrupted = True
    def moveOrcs(self):
        land = self.land
        orcs = self.orcs
        forests = self.forests
        redo = True
        while redo:
            redo = False
            for orc in orcs:
                #move to closest not targeted tree
                closests = [orc]
                least = -1

                for forest in forests:
                    if forest.orcs > forest.elves:
                        continue
                    d = forest.distanceTo(orc)
                    if least == -1 or d < least:
                        closests = [forest]
                        least = d
                    elif d == least:
                        closests.append(forest)
                closest = choice(closests)
                
                dx = closest.x - orc.x
                dy = closest.y - orc.y

                if closest in forests:
                    forest = land.get(closest)

                land.get(orc).orcs -= 1
                if abs(dx) > abs(dy):
                    orc.move('RIGHT' if dx > 0 else 'LEFT')
                elif abs(dx) < abs(dy):
                    orc.move('DOWN' if dy > 0 else 'UP')
                elif dx != 0:
                    orc.move('RIGHT' if dx > 0 else 'LEFT')
                elif dy != 0:
                    orc.move('DOWN' if dy > 0 else 'UP')
                land.get(orc).orcs += 1

    def moveElves(self, commands):
        elves = self.elves
        land = self.land
        for i in range(len(commands)):
            elf = elves[i]
            command = commands[i]
            if command != 'WAIT':
                land.get(elf).elves -= 1
                elf.move(command, land)
                land.get(elf).elves += 1
    def printGame(self):
        os.system('clear')
        land = self.land
        for row in land.array:
            out = ''
            for cell in row:
                if cell.battle():
                    out += 'œ'
                elif cell.elves > 0:
                    out += 'e'
                elif cell.orcs > 0:
                    out += 'o'
                elif cell.tower:
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
        self.printGame()
        return
        orcs = self.orcs
        print(len(orcs))
        for orc in orcs:
            print(orc.x, orc.y)

    def getInstructions(self):
        return ['WAIT' for i in range(len(self.elves))];

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            seed(sys.argv[1])
        except ValueError:
            print('Not a valid int:', sys.argv[1])
    else:
        s = str(time.time())
        seed()
        log = open('corruption.log', 'w')
        log.write('seed = "' + s + '"')
        log.close()
    game = Game()