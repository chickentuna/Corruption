import sys, math

def log(t):
    if isinstance(t, tuple):
        print(*t, file=sys.stderr)    
    else:
        print(t, file=sys.stderr)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in input().split()]
i = 0
# game loop
while 1:
    log(('>', i))
    i+= 1
    for i in range(height):
        row = input()
    elfCount = int(input())
    for i in range(elfCount):
        elfX, elfY = [int(j) for j in input().split()]
    orcCount = int(input())
    for i in range(orcCount):
        orcX, orcY = [int(j) for j in input().split()]
    for i in range(elfCount):
        
        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."
        
        print("WAIT")
    sys.stdout.flush()