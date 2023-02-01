import sys;args = sys.argv[1:]
if args and args[0] == '':
  args.pop(0)
import re;
import random
import time;

def setGlobals(input):
  global SIZE, WIDTH, STATS, BOARD, TOKEN, LOM, OPPTOKEN, dy, dx
  STATS = {}
  SIZE = 64
  WIDTH = 8
  dy = [0, 0, 1, -1, -1, 1, -1, 1]
  dx = [1, -1, 0, 0, 1, -1, -1, 1]
  formatMoves = "^[A-Za-z]\d*$"
  if input and len(input[0]) == 64:
    BOARD = input[0].lower()
    if len(input) >=2 and len(input[1]) == 1 and re.search("^[XOxo]$", input[1]):
      TOKEN = input[1].lower()
      #LOM = convertMoves(input[2:], formatMoves)
    else:
      if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
      else: TOKEN = 'o'
      #LOM = convertMoves(input[1:], formatMoves)
  else:
    BOARD = '.'*27+'ox......xo'+'.'*27
    if len(input) >=2 and len(input[0]) == 1 and re.search("^[XOxo]$", input[0]):
      TOKEN = input[0].upper()
      #LOM = convertMoves(input[1:], formatMoves)
    else:
      if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
      else: TOKEN = 'o'
      #LOM = convertMoves(input[0:], formatMoves)
  OPPTOKEN = "o" if TOKEN == 'x' else "x"
  # print("board: ", BOARD)
  # print("token: ", TOKEN)
  # print("List of Possible Moves: ", LOM)

def convertMoves(unformattedMoves, regex):
  formatted = []
  for i in unformattedMoves:
    if (x:=re.search(regex, i)):
      print(i)
      col = ord(i[0]) - 65
      row = int(i[1])-1
      formatted.append(row*8+col)
    else:
      formatted.append(int(i))
  return formatted

def findMoves(pzl):
  # returns a set of all possible moves
  print(pzl)
  posMoves = set()
  for ct, it in enumerate(pzl):
    if it == TOKEN:
      row = ct // 8
      col = ct % 8
      for i in range(8):
        newR = row+dy[i]
        newC = col+dx[i]
        ind = newR*8+newC
        if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == OPPTOKEN:
          while 0 <= newR < 8 and 0 <= newC < 8 and (pzl[ind] == OPPTOKEN):
            newR += dy[i]
            newC += dx[i]
            ind = newR*8+newC
          if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == TOKEN:
            continue
          if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == ".":
            posMoves.add(ind)
  print(posMoves)
  return posMoves

def playOthello():
  start = time.process_time()
  setOfMoves = findMoves(BOARD)
  if setOfMoves:
    printpz(BOARD, setOfMoves)
    print(f"Possible moves for {TOKEN}: ", *setOfMoves)
  else:
    print("No moves possible")
  print()

def printpz(solved, setOfPosMoves):
  if setOfPosMoves:
    for i in range(1, SIZE+1):
      if (i-1) % WIDTH == 0 and i != 0:
        print()
      if i-1 in setOfPosMoves:
        print("*", end="")
      else:
        print(solved[i - 1], end="")
  else:
    for i in range(1, SIZE+1):
      if (i-1) % WIDTH == 0 and i != 0:
        print()
      print(solved[i-1], end="")
  print()

def updateStats(phrase):
  if phrase in STATS:
    STATS[phrase] +=1
  else:
    STATS[phrase] = 1

if __name__ == '__main__':
  #othello.py [board] [tokenToPlay] [move1] [move2] ...
  first = time.process_time()
  setGlobals(args)
  playOthello()
  print(f"{(time.process_time() - first):.4g}s")
  print()

# 2*(numberOfSolvedPuzzles+(150-totalNumberOfPuzzles))/3
# Evelyn Li, pd 7, 2024