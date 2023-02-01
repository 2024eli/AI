import time
import random

gWIDTH = 0
gHEIGHT = 0
numPuzzles = 500
start_time = time.process_time()
PZ = '321_'

def swap(pz, i1, i2):
  return pz[:i1] + pz[i2] + pz[i1 + 1:i2] + pz[i1] + pz[i2 + 1:]

def levelCount(pz):
  global gWIDTH;
  global gHEIGHT
  gWIDTH = findWidth(pz)
  gHEIGHT = len(pz) // gWIDTH

  pz = createSquare(pz)

  parseMe = [pz]
  dctSeen = {pz: 0}
  index = 1

  level = [pz]  # Level 0
  nextLevel = set()  # Puzzles in the next level, not removing the ones already seen
  print("Level 0: 1")
  while parseMe:  # While theres still more puzzles to be found
    # itm = parseMe[index]
    for itm in level:
      for n in neighbors(itm):
        if n not in dctSeen:
          parseMe.append(n)
        nextLevel.add(n)
    val = sum(1 for it in nextLevel if it not in dctSeen)
    if val == 0:
      print(dctSeen)
      return "Level " + str(index) + ": 0"
    print(f"Level {index}: {val}")  # prints puzzles in level
    for it in nextLevel:
      if it not in dctSeen:
        dctSeen[it] = index
    level = [*nextLevel]
    nextLevel = set()
    index += 1


def neighbors(pz):
  ind = pz.index('_')
  lst = []
  # UP
  if ind - (gWIDTH + 1) > -1:
    lst.append(swap(pz, ind - (gWIDTH + 1), ind))
  # DOWN
  if ind + (gWIDTH + 1) < len(pz):
    lst.append(swap(pz, ind, ind + gWIDTH + 1))
  # LEFT
  if ind - 1 > -1 and pz[ind - 1] != " ":
    lst.append(swap(pz, ind - 1, ind))
  # RIGHT
  if ind + 1 < len(pz) and pz[ind + 1] != " ":
    lst.append(swap(pz, ind, ind + 1))
  return lst

def findWidth(pz):
  return len(pz) // int(len(pz) ** (1 / 2))

def createSquare(pz):
  newStr = ""
  while (pz):
    newStr += pz[:gWIDTH] + " "
    pz = pz[gWIDTH:]
  newStr += pz
  return newStr

print(levelCount(PZ))
end_time = time.process_time()
print(f"Time: {end_time - start_time:.1g}s")

# Emi Zhang Evelyn Li 2024 Pd 7