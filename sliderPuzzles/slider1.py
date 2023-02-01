import sys; args = sys.argv[1:]
import time; VERYFIRST = time.process_time()
import random

if args:
  PZ = args[0]
  GOAL = args[1] if len(args) > 1 else "".join(sorted(PZ)).replace('_', '')+ '_'
  size = len(GOAL)
#PZ='8172345_6'; GOAL= '635128_47'
NUMOFPZ = 500

#Find size
def findSize(pz):
  global gWIDTH
  global gHEIGHT
  size = len(GOAL)
  gWIDTH = int(size**(1/2))
  while gWIDTH > 1:
    if size % gWIDTH == 0: break
    gWIDTH -= 1
  if gWIDTH < (gHEIGHT:=size // gWIDTH):
    gWIDTH, gHEIGHT = gHEIGHT, gWIDTH

if args: findSize(PZ)

def swapChar(a, b, s):
  first, last = (a, b) if a < b else (b, a)
  return s[:first] + s[last] + s[first+1:last] + s[first] + s[last+1:]

def print_pz(board):
  top = ""
  step = 10
  for i in range(0, len(board)+1, step):
    chunk = board[i:i+step]
    for j in range(gHEIGHT):
      for puzzle in chunk:
        top += puzzle[gWIDTH*j:gWIDTH*(j+1)] + " "
      print(top)
      top = ""

def neighbors(puzzle, dctSeen):
  myLst = []
  if (i:=puzzle.index("_"))-gWIDTH >= 0:
    myLst.append(swapChar(i, i-gWIDTH, puzzle))
  if i+gHEIGHT < gHEIGHT**2:
    myLst.append(swapChar(i, i+gHEIGHT, puzzle))
  if (v:= ((i+1) % gHEIGHT)) != 1 and v != 0:
    myLst.append(swapChar(i, i+1, puzzle))
    myLst.append(swapChar(i, i-1, puzzle))
  if v == 1:
    myLst.append(swapChar(i, i+1, puzzle))
  if v == 0:
    myLst.append(swapChar(i, i-1, puzzle))
  return [i for i in myLst if (i != PZ and i not in dctSeen)]

def findPath(dd, gg):
  path = []
  while (d:=dd[gg]) != "":
    path = [d] + path
    gg = d
  return path

def icEven(pzle):
  p = (pzle.index('_') // gHEIGHT)
  return icOdd(pzle) + ((p + 1) if pzle.index('_') / gHEIGHT is not int else (p))

def icOdd(pzle):
  p = pzle.replace('_','')
  return sum([sum([p[i]>j for j in p[i:]]) for i in range(size-1)])

def ret(pz, goal):
  START = time.process_time()
  path, boo = solve(pz, goal)
  print_pz(path)
  print(f"Steps: {boo-1}")
  diff = time.process_time() - START
  print(f"Time: {diff:.3g}s\n")
  return boo-1

def solve(pz, goal):
  solvable = icEven(pz) % 2 == icEven(goal) % 2 if gWIDTH % 2 == 0 else icOdd(pz) % 2 == icOdd(goal) % 2
  if not solvable:
    return [pz], 0
  elif pz==goal:
    return [pz], 1
  else:
    parseMe = [pz]
    dctSeen = {pz: ""} #key is a node, val is a parent
    front = 0
    while parseMe:
      it = parseMe[front]
      for i in neighbors(it, dctSeen): #for each unseen neighbor of item:
        parseMe.append(i)
        dctSeen[i] = it
        if i == goal: #finish up and exit
          (path:=findPath(dctSeen, goal)).append(goal)
          return path, len(path)
      front+=1

if args:
  ret(PZ, GOAL)
else:
  stats = [0, 0] #1 = total path len #2 = total solvable puzzles
  gHEIGHT, gWIDTH, size = 3, 3, 9
  for i in range(NUMOFPZ):
    pzLst = ['1', '2', '3', '4', '5', '6', '7', '8', '_']
    random.shuffle(pzLst)
    PZ = "".join(pzLst)
    random.shuffle(pzLst)
    GOAL = "".join(pzLst)
    steps = ret(PZ, GOAL)
    if steps != -1:
      stats[0] += 1
      stats[1] += steps
  print(f"Stats: {stats}")
  print(f"Total time: {time.process_time()-VERYFIRST}")
  print(f"Total numbers of puzzles: {NUMOFPZ}")
  print(f"Total number of solvable: {stats[0]}")
  print(f"Average path length of solvable puzzle goal pairs (integer): {stats[1]//stats[0]}")


#Evelyn Li, pd 7, 2024
