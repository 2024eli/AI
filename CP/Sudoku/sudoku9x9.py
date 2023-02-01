import sys;args = sys.argv[1:]
import random
import time;

def setGlobals(pzl):
  global SIZE, WIDTH, SYMSET, NBRS, LOCS, posToCS, miniW, miniH, STATS
  STATS = {}
  SIZE = len(pzl)
  WIDTH = int(len(pzl) ** 0.5)
  miniH, miniW = 0, 0
  if (int(WIDTH ** 0.5 // 1) == int(WIDTH ** 0.5)):
    miniH, miniW = int(WIDTH ** 0.5), int(WIDTH ** 0.5)
  else:
    miniH, miniW = int(WIDTH ** 0.5 // 1), int(WIDTH ** 0.5 // 1 + 1)
  SYMSET = {*"123456789"}
  '''
  SYMSET = {i for i in pzl} - {'.'}
  other = list('0ZYXWVUTSRQPONMLKJIHGFEDCBA987654321')
  while (len(SYMSET) != WIDTH):
    SYMSET.add(other.pop())'''
  rowcs = [{i for i in range(r*WIDTH, (r+1)*WIDTH)} for r in range(WIDTH)]
  colcs = [{i for i in range(c, c+SIZE-miniW*miniH+1, miniW*miniH)} for c in range(WIDTH)]
  subcs = [set() for i in range(WIDTH)]
  c = -1
  for i in range(0, len(pzl) - 1, WIDTH * miniH):
    for j in range(miniH):
      head = i + j * miniH
      c += 1
      for q in range(miniW):
        first = head + q
        for w in range(miniH):
          col = first + WIDTH * w
          subcs[c].add(col)
  LOCS = rowcs + colcs + subcs
  posToCS = {i: list() for i in range(SIZE)}
  #posToCS = {i: [rowcs[i//WIDTH], colcs[i%WIDTH], *(j for j in subcs if i in j)] for i in range(SIZE)}
  for i in range(SIZE):
    r = i // WIDTH
    c = i % WIDTH
    posToCS[i].append(rowcs[r])
    posToCS[i].append(colcs[c])
    for j in subcs:
      if i in j:
        posToCS[i].append(j)
        break
  NBRS = {i: (posToCS[i][0] | posToCS[i][1] | posToCS[i][2])-{i} for i in posToCS}

def checkSum(pzl):
  return sum(ord(c) for c in pzl) - SIZE * ord('1')

def findOptimal(pzl, sym):
  m = WIDTH
  opt = 0
  for ind in sym:
    numPosSym = len(sym[ind])
    if numPosSym < m: #if numner of symbles is less than the width
      m = numPosSym #the new max numer is number of symbols
      opt = ind #add into set
  updateStats(f"bestDot success")
  return opt

def findEn(pzl, sym):
  #returns minimum of set positions that each symbol in sym can be
  minSet = set()
  minLen = len(NBRS[0])
  for cs in LOCS:
    s = {pzl[i] for i in cs if pzl[i] != "."}
    for symbol in SYMSET:
      temp = set()
      for ind in cs:
        if pzl[ind] not in s and symbol in sym[ind]:
          temp.add(ind)
      if temp and len(temp) < minLen:
        minSet = temp
        minLen = len(minSet)
        if len(minSet) <= 1:
          updateStats(f"enhance success")
          return symbol, minSet
  updateStats(f"enhance fail")
  return None, None

def bruteForce(pzl, sym):
  # returns a solved puzzle if possible else ""
  if '.' not in pzl or not sym:
    updateStats(f"bF success")
    return pzl
  choice = findOptimal(pzl, sym)
  symb, enhanced = None, None
  if len(sym[choice]) > 1:
    symb, enhanced = findEn(pzl, sym) #
  #print(symb, enhanced, sym[choice])
  if enhanced:
    updateStats(f"choice ct: {len(enhanced)}")
    for i in enhanced:
      cpy = sym #{j: {*sym[j]} for j in sym}
      for nbr in NBRS[i]:
        if nbr in sym:
          cpy[nbr].discard(symb)
      del cpy[i]
      newPzl = pzl[0:i] + symb + pzl[i + 1:]
      bF = bruteForce(newPzl, cpy)
      if bF:
        updateStats(f"bF enhance")
        return bF
  else:
    for num in sym[choice]:
      updateStats(f"choice ct: {len(sym[choice])}")
      cpy = None
      if len(sym[choice]) == 1:
        cpy = sym
      else:
        cpy = {i:{*sym[i]} for i in sym}
      for nbr in NBRS[choice]:
        if nbr in sym:
          cpy[nbr].discard(num)
      del cpy[choice]
      newPzl = pzl[0:choice] + num + pzl[choice+1:]
      bF = bruteForce(newPzl, cpy)
      if bF:
        updateStats(f"bF bestDot")
        return bF
  updateStats(f"bF fail")
  return ""

def printPzl(board, space, symm):
  start = time.process_time()
  print(board)
  solved = bruteForce(board, symm)
  sp = " " * space
  print(f"{sp}{solved} {checkSum(solved)} {(time.process_time() - start):.4g}s")
  # testing purposes
  #printpz(board)
  #printpz(solved)
  print()
  print()

def printpz(solved):
  for i in range(1, SIZE+1):
    if (i-1) % WIDTH == 0 and i != 0:
      print()
    print(" " + solved[i-1] + " ", end="")
    if i%3 == 0 and i%WIDTH != 0:
      print(" | ", end="")
    if i % (WIDTH*miniH) == 0 and i != SIZE:
      print("\n"+"----------+-----------+---------", end="")

def updateStats(phrase):
  if phrase in STATS:
    STATS[phrase] +=1
  else:
    STATS[phrase] = 1

if __name__ == '__main__':
  first = time.process_time()
  f = open(args[0]) if args else open('puzzles.txt')
  c = 1
  setGlobals("." * 81)
  for pz in f:
    symm = {i: SYMSET - {pz[j] for j in NBRS[i]} for i in range(SIZE) if pz[i] == '.'}
    print(str(c) + ": ", end="")
    space = 2 + len(str(c))
    printPzl(pz.strip(), space, symm)
    #if c == 56: break
    c += 1
  print(f"Total time: {(time.process_time()-first):.4g}s")
  print("STATS:")
  for key in STATS:
    print(f"{key}: {STATS[key]}")
  print()

# 2*(numberOfSolvedPuzzles+(150-totalNumberOfPuzzles))/3
# Evelyn Li, pd 7, 2024