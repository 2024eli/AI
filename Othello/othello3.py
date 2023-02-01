import sys;args = sys.argv[1:]
if args and args[0] == '':
  args.pop(0)
import re;
import random
import time;

def setGlobals(input):
  global SIZE, WIDTH, BOARD, TOKEN, LOM, OPPTOKEN, dy, dx
  SIZE = 64
  WIDTH = 8
  dy = [0, 0, 1, -1, -1, 1, -1, 1]
  dx = [1, -1, 0, 0, 1, -1, -1, 1]
  formatMoves = "^[A-Za-z]\d*$"
  if input and len(input[0]) == 64:
    BOARD = input[0].lower()
    if len(input) >=2 and len(input[1]) == 1 and re.search("^[XOxo]$", input[1]):
      TOKEN = input[1].lower()
      LOM = convertMoves(input[2:], formatMoves)
    else:
      if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
      else: TOKEN = 'o'
      LOM = convertMoves(input[1:], formatMoves)
  else:
    BOARD = '.'*27+'ox......xo'+'.'*27
    if len(input) >=2 and len(input[0]) == 1 and re.search("^[XOxo]$", input[0]):
      TOKEN = input[0].lower()
      LOM = convertMoves(input[1:], formatMoves)
    else:
      if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
      else: TOKEN = 'o'
      LOM = convertMoves(input[0:], formatMoves)
  OPPTOKEN = "o" if TOKEN == 'x' else "x"
  # print("board: ", BOARD)
  # print("token: ", TOKEN)
  # print("List of Possible Moves: ", LOM)

def convertMoves(unformattedMoves, regex):
  formatted = []
  for i in unformattedMoves:
    if "-" not in i:
      if (x:=re.search(regex, i)):
        col = ord(i[0].upper()) - 65
        row = int(i[1])-1
        formatted.append(row*8+col)
      else:
        formatted.append(int(i))
  return formatted

def findMoves(pzl, token, opptoken):
  # returns a set of all possible moves
  posMoves = set()
  for ct, it in enumerate(pzl):
    if it == token:
      row = ct // 8
      col = ct % 8
      for i in range(8):
        newR = row+dy[i]
        newC = col+dx[i]
        ind = newR*8+newC
        if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
          while 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
            newR += dy[i]
            newC += dx[i]
            ind = newR*8+newC
          if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == ".":
            posMoves.add(ind)
  return posMoves

def makeMoves(pzl, token, opptoken, move, som):
  print()
  passed = False
  print(f"{token} plays to {move}")
  newPzl = pzl[:move] + token + pzl[move + 1:]
  newPzl = turn(newPzl, token, opptoken, move)
  som = findMoves(newPzl, opptoken, token)
  printpz(newPzl, som)
  if som:
    print(f"Possible moves for {opptoken}: ", *som)
  else:  # MAKE IT WORK FOR PASSES
    print("No moves possible")
    passed = True
    som = findMoves(newPzl, token, opptoken)
    if som:
      print(f"Possible moves for {token}: ", *som)
  return som, newPzl, passed

def turn(pzl, token, opptoken, move):
  #turn all the opptokens in between affected by the move into the token
  converted = set()
  row = move // 8
  col = move % 8
  newPzl = pzl
  for i in range(8):
    runningSet = set()
    newR = row + dy[i]
    newC = col + dx[i]
    ind = newR * 8 + newC
    if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
      while 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
        runningSet.add(ind)
        newR += dy[i]
        newC += dx[i]
        ind = newR * 8 + newC
      if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == token:
        for itt in runningSet:
          converted.add(itt)
  for i in converted:
    newPzl = newPzl[:i] + token + newPzl[i+1:]
  return newPzl

def playOthello(pzl, token, opptoken):
  start = time.process_time()
  som = findMoves(pzl, token, opptoken)
  printpz(BOARD, som)
  if som:
    print(f"Possible moves for {token}: ", *som)
    print()
    count = 0
    newPzl = BOARD
    for i in LOM:
      if count % 2 == 0:
        som, newPzl, passed = makeMoves(newPzl, token, opptoken, i, som)
        if passed:
          count+=1
      else:
        som, newPzl, passed = makeMoves(newPzl, opptoken, token, i, som)
        if passed:
          count+=1
      count+=1
  else:
    print("No moves possible")
    token, opptoken = opptoken, token
    som = findMoves(pzl, token, opptoken)
    if som:
      print(f"Possible moves for {token}: ", *som)
      print()
      count = 0
      newPzl = BOARD
      for i in LOM:
        if count % 2 == 0:
          som, newPzl, passed = makeMoves(newPzl, token, opptoken, i, som)
          if passed:
            count += 1
        else:
          som, newPzl, passed = makeMoves(newPzl, opptoken, token, i, som)
          if passed:
            count += 1
        count += 1
  print()

def printpz(solved, setOfPosMoves):
  while "*" in solved:
    solved.replace("*", ".")
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
  print()
  print(f"{solved} {solved.count('x')}/{solved.count('o')}")

if __name__ == '__main__':
  #othello.py [board] [tokenToPlay] [move1] [move2] ...
  first = time.process_time()
  setGlobals(args)
  playOthello(BOARD, TOKEN, OPPTOKEN)
  print(f"{(time.process_time() - first):.4g}s")
  print()

# Evelyn Li, pd 7, 2024