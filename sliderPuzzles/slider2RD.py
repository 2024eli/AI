import sys; args = sys.argv[1:]
import time; START = time.process_time()
import random

f = open(args[0]) if args else open('puzzles.txt')

GOAL = f.readline().strip()
size = len(GOAL)
NUMOFPZ = 500
gWIDTH = 4
gHEIGHT = 4

lookUpMan = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1),
             (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3),
             (2, 3), (3, 3)]

lookUp = [(1, 4), (0, 5, 2), (1, 6, 3), (2, 7), (8, 5, 0), (1, 4, 9, 6),
          (2, 5, 10, 7), (3, 6, 11), (12, 9, 4), (5, 8, 13, 10), (6, 9, 14, 11),
          (7, 10, 15), (13, 8), (12, 14, 9), (13, 15, 10), (14, 11)]

lookUpPATH = [('R', 'D'), ('L', 'D', 'R'), ('L', 'D', 'R'), ('L', 'D'),
              ('D', 'R', 'U'), ('U', 'L', 'D', 'R'), ('U', 'L', 'D', 'R'),
              ('U', 'L', 'D'), ('D', 'R', 'U'), ('U', 'L', 'D', 'R'),
              ('U', 'L', 'D', 'R'), ('U', 'L', 'D'), ('R', 'U'), ('L', 'R', 'U'),
              ('L', 'R', 'U'), ('L', 'U')]

lookUpGoal = {it:c for c, it in enumerate(GOAL)} #THIS PART TAKES UP WAYYYY TOOOO MUCH TIME
#print(lookUpGoal)

#HeapPQ functions
def heapUp(heap, k):
  parent = k//2
  if parent == 0:
    return
  if heap[parent] > heap[k]:
    heap[k], heap[parent] = heap[parent], heap[k]
    heapUp(heap, parent)

def heapDown(heap, k, last):
  l = 2*k
  r = 2*k+1
  if k > last or l > last:
    return
  if r > last:
    if heap[k] > heap[l]:
      heap[k], heap[l] = heap[l], heap[k]
  else:
    min = l if heap[l] < heap[r] else r
    if heap[k] > heap[min]:
      heap[k], heap[min] = heap[min], heap[k]
      heapDown(heap, min, last)

def removeVal(heap):
  heap[1], heap[-1] = heap[-1], heap[1]
  it = heap.pop()
  heapDown(heap, 1, len(heap)-1)
  return it

def insertVal(heap, val):
  heap.append(val)
  heapUp(heap, len(heap)-1)
  return True

def peekPQ(heap):
  if len(heap)!=1:
    return heap[1]
  return None

def swapChar(a, b, s):
  first, last = (a, b) if a < b else (b, a)
  return s[:first] + s[last] + s[first+1:last] + s[first] + s[last+1:]

def neighbors(puzzle, us):
  return [swapChar(i, us, puzzle) for i in lookUp[us]]

def findPath(goal, lvl, closedSet):
  path = [goal]
  while lvl != 0:
    for nbr in neighbors(goal, goal.index('_')):
      if nbr in closedSet and closedSet[nbr] == lvl-1:
        goal, lvl = nbr, closedSet[nbr]
        path.insert(0, nbr)
  return path

def condensePath(lstPzl):
  str = ''
  if lstPzl:
    if len(lstPzl) == 1:
      return 'G'
    for i in range(1, len(lstPzl)):
      indBefore = lstPzl[i-1].find('_')
      indAfter = lstPzl[i].find('_')
      iA = 0
      for j in range(len(lookUp[indBefore])):
        if lookUp[indBefore][j] == indAfter:
          iA = j
      str += lookUpPATH[indBefore][iA]
    return str
  return 'X'

#for individual puzzle
def manhattanHelper(start, end):
  x = abs(lookUpMan[start][0] - lookUpMan[end][0])
  y = abs(lookUpMan[start][1] - lookUpMan[end][1])
  return x+y

allMan = {(start, end): manhattanHelper(start, end) for end in range(size) for start in range(size)}
#print(allMan)
oneMan = {(start, end, it): (1 - 2*(allMan[(end, lookUpGoal[it])] > allMan[(start, lookUpGoal[it])])) for start in range(size) for end in lookUp[start] for it in GOAL if it != "_"}

#Manhattan distance
def h(pz, goal):
  return sum([allMan[c, lookUpGoal[it]] for c, it in enumerate(pz) if it != '_'])

def updateF(start, end, it, oldF):
  return oldF if oneMan[(start, end, it)] == -1 else oldF+2

def icEven(pzle):
  p = (pzle.index('_') // gHEIGHT)
  return icOdd(pzle) + ((p + 1) if pzle.index('_') / gHEIGHT is not int else (p))

def icOdd(pzle):
  p = pzle.replace('_','')
  return sum([sum([p[i]>j for j in p[i:]]) for i in range(size-1)])

def levelCount(pz):
  parseMe = [pz]
  dctSeen = {pz: 0}
  index = 1

  level = [pz]  # Level 0
  nextLevel = set()  # Puzzles in the next level, not removing the ones already seen
  while parseMe:  # While theres still more puzzles to be found
    for itm in level:
      for n in neighbors(itm):
        if n not in dctSeen:
          parseMe.append(n)
        nextLevel.add(n)
    for it in nextLevel:
      if it not in dctSeen:
        dctSeen[it] = index
        if it == GOAL:
          return dctSeen
    level = [*nextLevel]
    nextLevel = set()
    index += 1

def ret(pz, goal):
  lstPzl = astar(pz, goal)
  diff = time.process_time() - START
  print(f"{pz} path {condensePath(lstPzl)}\n")

def astar(root, goal):
  solvable = icEven(root) % 2 == icEven(goal) % 2 if gWIDTH % 2 == 0 else icOdd(root) % 2 == icOdd(goal) % 2
  if not solvable:
    return []
  #openSet = [(heur:=h(root, goal), root, 0)] #formerly parseMe (h, root, level)
  fBuckets = [[] for i in range(81)]
  fBuckets[h(root, goal)].append((root, 0)) # level is 0
  lastEmpty = 0
  closedSet = {} #formerly dctSeen
  while True:
    for i in range(lastEmpty, 81):
      if len(fBuckets[i]) > 0:
        lastEmpty = i
        pz, lvl = fBuckets[i].pop()
        break
    if pz in closedSet: continue
    closedSet[pz] = lvl
    if pz == goal:
      return findPath(goal, lvl, closedSet)
    for nbr in neighbors(pz, us:=pz.index('_')):
      f = updateF(us, n:=nbr.index('_'), pz[n], lastEmpty)
      fBuckets[f].append((nbr, lvl+1))
      #openSet.append((f, nbr, lvl+1))

def main():
  print(f"{GOAL} path G")
  print()
  for pz in f:
    ret(pz.strip(), GOAL)

if __name__ == "__main__": main()

#Evelyn Li, pd 7, 2024
