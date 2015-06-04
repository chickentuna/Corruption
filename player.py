import sys, math

def log(t):
    if isinstance(t, tuple):
        print(*t, file=sys.stderr)    
    else:
        print(t, file=sys.stderr)

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target = None
        self.action = "WAIT"
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return self.x * 2 + self.y * 3
    def __repr__(self):
        return str(self.x) + ' ' + str(self.y)
    def distanceTo(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

width, height = [int(i) for i in input().split()]

# game loop
while 1:
    elves = []
    forests = []
    for y in range(height):
        row = input()
        for x in range(len(row)):
            if row[x] == 'F':
                forests.append(Coord(x,y))
    elfCount = int(input())
    for i in range(elfCount):
        elfX, elfY = [int(j) for j in input().split()]
        elves.append(Coord(elfX,elfY))
    orcCount = int(input())
    for i in range(orcCount):
        orcX, orcY = [int(j) for j in input().split()]
    
    for i in range(elfCount):
        elf = elves[i]
        if elf.target == None:
            for forest in forests:
                if (forest.target == None):
                    neigh = (Coord(forest.x, forest.y - 1),
                            Coord(forest.x, forest.y + 1),
                            Coord(forest.x - 1, forest.y),
                            Coord(forest.x + 1, forest.y))
                    if any([(c not in forests and c.x >=0 and c.y >= 0 and c.x < width and c.y < height) for c in neigh]):
                        forest.target = elf
                        elf.target = forest
                        break
        elf.action = "WAIT"
        if elf.target != None:
            dx = elf.target.x - elf.x
            dy = elf.target.y - elf.y
            if dx != 0:
                elf.action = 'RIGHT' if dx > 0 else 'LEFT'
            elif dy != 0:
                elf.action = 'DOWN' if dy > 0 else 'UP'
            else:
                elf.target.target = None
                elf.target = None
        print(elf.action)
    sys.stdout.flush()