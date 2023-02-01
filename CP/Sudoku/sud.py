import sys;args = sys.argv[1:]
import random
import time;

def setGlobals(pzl):
  global SIZE, WIDTH, SYMSET, NBRS, LOCS, posToCS, miniW, miniH
  SIZE = len(pzl) #number of squares in a sudoku
  WIDTH = int(SIZE ** 0.5) #width of the entire puzzle
  miniH, miniW = 0, int(WIDTH**0.5) #initialize width and height of subblocks
  while miniW > 1:
    if WIDTH % miniW == 0: break
    miniW -=1
  if miniW < (miniH := WIDTH//miniW):
    miniW, miniH = miniH, miniW
  SYMSET = {i for i in pzl} - {'.'} - {'\n'}
  other = list('0ZYXWVUTSRQPONMLKJIHGFEDCBA987654321')
  while (len(SYMSET) != WIDTH):
    SYMSET.add(other.pop())
  rowcs = [{i for i in range(r*WIDTH, (r+1)*WIDTH)} for r in range(WIDTH)] #list of sets of indices in each row
  colcs = [{i for i in range(c, SIZE, miniW*miniH)} for c in range(WIDTH)] #list of sets of indices in each column
  subcs = [set() for i in range(WIDTH)] #list of sets of indices in each subblock
  c = -1
  for i in range(0, SIZE, WIDTH * miniH): #in range of indices of the first index of each subblock
    for j in range(miniH): #range of each subblocks height
      head = i + j * miniW #index of head of the subblock
      c += 1 #subblock number
      for q in range(miniW): #go through each index of the width
        first = head + q #index of head of the subblock for each subblock (shifts it through q)
        for w in range(miniH): #for each index horizonally
          col = first + WIDTH * w #go down each row for the column indices
          subcs[c].add(col) #add them to the respective subblock number
  LOCS = rowcs + colcs + subcs #set addition giving a giant list of constraint sets
  posToCS = [[cs for cs in LOCS if pos in cs] for pos in range(SIZE)]
  NBRS = [set().union(*[cs for cs in posToCS[pos]]) - {pos} for pos in range(SIZE)] #mapping index to all the neighboring indices

def checkSum(pzl): #produces a checksum for each puzzle
  return sum(ord(c) for c in pzl) - SIZE * ord('1')

def findOptimal(pzl, sym): #finding the best position
  m = WIDTH #initialize the min number of symbols
  opt = 0 #initial optimzied position
  for ind in sym: #iterate through indices with .
    numPosSym = len(sym[ind]) #number of possible symbols
    if numPosSym == 1: #shortest number of positions
      updateStats(f"bestDot early bail")
      return ind
    if numPosSym < m: #if numner of symbols is less than the width
      m = numPosSym #the new min number is number of symbols
      opt = ind #new index with min number of symbols
  updateStats(f"bestDot success")
  return opt #return optimized index

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
        if minLen <= 1:
          updateStats(f"enhance success")
          return symbol, minSet
  updateStats(f"enhance fail")
  return None, None

def bruteForce(pzl, sym, numNonDot):
  # returns a solved puzzle if possible else ""
  if numNonDot==SIZE or not sym:
    updateStats(f"bF success")
    return pzl
  choice = findOptimal(pzl, sym) #find the best position
  symb, enhanced = None, None
  if len(sym[choice]) > 1: #if the best position doesn't just have one symbol,
    symb, enhanced = findEn(pzl, sym) #call to find best symbol which returns a symbol if theres only one possible pos
  if enhanced: #if there exists a symbol that only has one possible position
    updateStats(f"choice ct: {len(enhanced)}")
    for i in enhanced:
      cpy = sym #{j: {*sym[j]} for j in sym}
      for nbr in NBRS[i]: #go through all neighbors of that index
        if nbr in sym: #if that neighbor is in the list of indices of dots
          cpy[nbr] -= {symb} #take out the symbol from the copy of the possible symbols dct
      cpy.pop(i) #take out the entire dictionary position
      newPzl = pzl[0:i] + symb + pzl[i + 1:]
      bF = bruteForce(newPzl, cpy, numNonDot+1)
      if bF:
        updateStats(f"bF enhance")
        return bF
  else: #run best position code
    for i, num in enumerate(sym[choice]): #i: index of choice, num: symbol
      updateStats(f"choice ct: {len(sym[choice])}")
      cpy = None
      if i != len(sym[choice])-1:
        updateStats("cpy")
        cpy = {i:{*sym[i]} for i in sym}
      else: #dont make a copy if it is the last choice
        updateStats("no copy")
        cpy = sym
      for nbr in NBRS[choice]: #same editing as previous if statement
        if nbr in sym:
          cpy[nbr] -= {num}
      cpy.pop(choice)
      newPzl = pzl[0:choice] + num + pzl[choice+1:]
      bF = bruteForce(newPzl, cpy,numNonDot+1)
      if bF:
        updateStats(f"bF bestDot")
        return bF
  updateStats(f"bF fail")
  return ""

def printPzl(board, space, symm):
  start = time.process_time()
  print(board)
  solved = bruteForce(board, symm, SIZE-board.count('.'))
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
  global STATS
  STATS = {}
  for pzl in f:
    pz = pzl.strip('\n')
    setGlobals(pz)
    symm = {i: SYMSET - {pz[j] for j in NBRS[i]} for i in range(SIZE) if pz[i] == '.'} #dictionary of all possible symbols
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