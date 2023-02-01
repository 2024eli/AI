import sys;args = sys.argv[1:]
import re
import random
import time;

def setGlobals(inputArr):
  global gH, gW, AREA, SYMSET, INPUT, SOT, runningArea
  INPUT = ' '.join(inputArr).replace('x', ' ').replace('X',' ').split(' ')
  gH, gW = int(INPUT[0]), int((INPUT[1]))
  AREA = gH*gW
  SOT = [(int(INPUT[i]), int(INPUT[i+1]), int(INPUT[i])*int(INPUT[i+1])) for i in range(2, len(INPUT), 2)]
  runningArea = 0
  for i in SOT:
    runningArea += (i[0] * i[1])
  print("running area ", runningArea)
  SOT.sort(key = lambda x : x[2], reverse=True)
  while runningArea < AREA:
    SOT.append((1, 1, 1))
    runningArea+=1
  other = 'ABCDEFGHIJKLMNOPQRSTUV1234567890'
  SYMSET = {i: other[i] for i in range(len(SOT))}
  print("SYMSET ", SYMSET)
  print("SOT ", SOT)
  print("gH: ", gH, " gW: ", gW, " AREA: ", AREA)

def checkSum(pzl): #produces a checksum for each puzzle
  lowestOrd = min(ord(c) for c in pzl)
  return sum(ord(c) for c in pzl) - SIZE * lowestOrd

def addable(h, w, head, pzl):
  if ((col:=head[0]) + w) > gW or ((row:=head[1]) + h) > gH:
    return False
  if pzl[row][col:col+w].count('.') < w:
    return False
  return True

def add(h, w, choice, head, pzl):
  symbol = SYMSET[choice]
  if addable(h, w, head, pzl):
    newPzl = [i for i in pzl]
    for i in range(head[1], head[1]+h):
      newPzl[i] = pzl[i][0:head[0]] + symbol*w + pzl[i][head[0]+w:]
    #print('newPzl: ', newPzl)
    return newPzl
  return False

def bruteForce(pzl, row, dctOfChoices): #lot standing for list of tuples
  # returns a solved puzzle if possible else ""
  # print(pzl)
  # for i in pzl:
  #   print(i)
  # print()
  if '.' not in pzl[gH-1]:
    return pzl
  while '.' not in pzl[row]:
    row+=1
  if '.' in pzl[row]:
    col = pzl[row].find('.')
  for choice in dctOfChoices:
    cpyChoice = {i:dctOfChoices[i] for i in dctOfChoices}
    del cpyChoice[choice]
    h, w = SOT[choice][0], SOT[choice][1]
    #flip
    for i in range(2):
      if i==0:
        newPzl = add(h, w, choice, (col, row), pzl)
        if newPzl:
          bF = bruteForce(newPzl, row, cpyChoice)
          if bF:
            return bF
      if h!=w and i==1:
        newPzl = add(w, h, choice, (col, row), pzl)
        if newPzl:
          bF = bruteForce(newPzl, row, cpyChoice)
          if bF:
            return bF
  return False

def decomposition(solved):
  s = ''
  if solved == False:
    return 'No solution'
  seen = set()
  print(solved)
  for i in solved:
    print(i)
  print()
  rectToSym = {SYMSET[i]:SOT[i] for i in SYMSET}
  for i in solved:
    for j, symbol in enumerate(i):
      if symbol not in seen:
        seen.add(symbol)
        if j + (w:=rectToSym[symbol][1]) - 1 == i.rfind(symbol):
          s += f"{rectToSym[symbol][0]}x{w} "
        else:
          s += f"{w}x{rectToSym[symbol][0]} "
  return s

def printPzl(init, listOfTuples):
  start = time.process_time()
  solved = ''
  if runningArea == AREA:
    solved = decomposition(bruteForce(init, 0, SYMSET))
  else:
    solved = decomposition(False)
  if solved == "No solution":
    print(f"{solved}")
  else:
    print(f"Decomposition: {solved}")
  print(f"{(time.process_time() - start):.4g}s")
  # testing purposes
  #printpz(board)
  #printpz(solved)
  print()
  print()

def printpz(solved):
  return ""

def updateStats(phrase):
  if phrase in STATS:
    STATS[phrase] +=1
  else:
    STATS[phrase] = 1

if __name__ == '__main__':
  first = time.process_time()
  inputArr = []

  if args:
    inputArr = args
  else:
    inputArr = '15x14 3x3 12x2 6x5 4x5 3x4 7x3 4x2 3x6 5x5 4x10'.split(' ')
  setGlobals(inputArr)
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  '''
  if args:
    inputArr = args
    setGlobals(inputArr)
    init = ["".join("." for j in range(gW)) for i in range(gH)]
    printPzl(init, SOT)
    print(f"Total time: {(time.process_time() - first):.4g}s")
  else:
    inputArr = '3x4 2x3 2x3'.split(' ') #'22 22 7 14 8 13 9 12 10 15 4 6'.split(' ')
    setGlobals(inputArr)
    init = ["".join("." for j in range(gW)) for i in range(gH)]
    printPzl(init, SOT)
    print(f"Total time: {(time.process_time()-first):.4g}s")
  #TEST
  setGlobals('11X12 3x6 2x5 4x10 7x9 1x1'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('10X13 3x6 2x5 4x10 7x9 1x1'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('8X5 4 2 4 2 4 2 4 2 2 4'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('13X14 4x5 3x8 6x11 7x10 2x1'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('22 22 7 14 8 13 9 12 10 15 4 6'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('15X15 9x4 6x11 10x5 4x7 5x5 3x6'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('15x14 3x3 12x2 6x5 4x5 3x4 7x3 4x2 3x6 5x5 4x10'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('89x144 2x2 3x3 5x5 8x8 13x13 21x21 34x34 55x55 89x89'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('21x21 8x8 9x9 8x8 7x7 6x6 6x6 6x6 5x5 4x4 4x4 4x4'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")
  setGlobals('56X56 32x11 32 10 28x14 28 7 28x6 21 18 21 18 21x14 21 14 17x14 14 4 10x7'.split(' '))
  init = ["".join("." for j in range(gW)) for i in range(gH)]
  printPzl(init, SOT)
  print(f"Total time: {(time.process_time() - first):.4g}s")'''

# Evelyn Li, pd 7, 2024