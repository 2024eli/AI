import sys;args = sys.argv[1:]
if args and args[0] == '':
  args.pop(0)
import re;
import random
import time;

#for changing LOM to parseable by code
def convertMoves(unformattedMoves, regex):
  formatted = []
  nextMovesList = uncondense(unformattedMoves)
  for i in nextMovesList:
    if "-" not in i:
      if (x:=re.search(regex, i)):
        col = ord(i[0].upper()) - 65
        row = int(i[1])-1
        formatted.append(row*8+col)
      else:
        formatted.append(int(i))
  return formatted

#also for changing LOM to parseable by code
def uncondense(unformattedMoves):
  formatted = []
  for i in unformattedMoves:
    movesString = i
    if len(movesString) > 2:
      j = 0
      while j < len(movesString):
        move = movesString[j]
        if move == "_":
          formatted.append(movesString[j + 1])
        else:
          formatted.append(movesString[j:j + 2])
        j += 2
    else:
      formatted.append(i)
  return formatted

SIZE = 64
WIDTH = 8
HOLES = 12
VERBOSE = False
CACHE_MOVES = {}
CACHE_TURN = {}
CACHE_AB = {}
CACHE_MG = {}
dy = [0, 0, 1, -1, -1, 1, -1, 1]
dx = [1, -1, 0, 0, 1, -1, -1, 1]
corner_points = {0, 7, 56,63}
corner_adj = {1,8,9,6,14,15,57,48,49,62,55,54}
square = {9:0, 14:7, 49:56, 54:63, 1:0, 8:0, 6:7, 15:7, 62:63, 48:56, 55:56, 57:63}
xSq = {9, 14, 49, 54}
cSq = {1, 8, 6, 15, 62, 48, 55, 57}
edges = [(0,1,2,3,4,5,6,7), (7,15,23,31,39,47,55,63),(56,57,58,59,60,61,62,63), (0,8,16,24,32,40,49,56)]
formatMoves = "^[A-Za-z]\d*$"
openingbook = {'...........................ox......xo...........................': [26],
               '..........................xxx......xo...........................': [20],
               '....................o.....xxo......xo...........................': [37],
               '..................o.......xox......xo...........................': [19],
               '....................o.....xxo......xxx..........................': [42],
               '..................ox......xxx......xo...........................': [34],
               '....................o.....xxo......oxx....o.....................': [34],
               '..................ox......oxx.....ooo...........................': [33],
               '..................ox.....xxxx.....ooo...........................': [21],
               }

BOARD = '.'*27+'ox......xo'+'.'*27
TOKEN = 'x'
LOM = []
specialToken = False
if 'v' in args or 'V' in args:
  VERBOSE = True
for arg in args:
  if len(arg) == 64:
    BOARD = arg.lower()
  if re.search("^HL", arg):
    HOLES = int(arg[2:])
  if re.search("^[XxOo]$", arg):
    specialToken = True
    TOKEN = arg
  if re.search("^(\d|[A-Za-z]\d|_|-)+$", arg):
    LOM.append(arg)
if not specialToken:
  if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
  else: TOKEN = 'o'
LOM = convertMoves(LOM, formatMoves)
OPPTOKEN = "o" if TOKEN == 'x' else "x"
# print("board: ", BOARD)
# print("token: ", TOKEN, OPPTOKEN)
# print("List of Possible Moves: ", LOM)

def findMoves(pzl, token):
  # returns a set of all possible moves
  if (tup:=(pzl, token)) in CACHE_MOVES:
    return CACHE_MOVES[tup]
  opptoken = 'o' if token.lower() == 'x' else "x"
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
  CACHE_MOVES[tup] = posMoves
  return posMoves

def makeMoves(pzl, token, move):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  newPzl = pzl[:move] + token + pzl[move + 1:]
  newPzl = turn(newPzl, token, opptoken, move)
  return newPzl

def turn(pzl, token, opptoken, move):
  #turn all the opptokens in between affected by the move into the token
  if (tup:=(pzl, token, move)) in CACHE_TURN:
    return CACHE_TURN[tup]
  converted = set()
  row = move // 8
  col = move % 8
  newPzl = list(pzl)
  for i in range(8):
    runningSet = list()
    newR = row + dy[i]
    newC = col + dx[i]
    ind = newR * 8 + newC
    if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
      while 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == opptoken:
        runningSet.append(ind)
        newR += dy[i]
        newC += dx[i]
        ind = newR * 8 + newC
      if 0 <= newR < 8 and 0 <= newC < 8 and pzl[ind] == token:
        for itt in runningSet:
          converted.add(itt)
  for i in converted:
    newPzl[i] = token
  realPzl = ''.join(newPzl)
  CACHE_TURN[tup] = realPzl
  return realPzl

def play(pzl, token):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  tknToPlay = token
  newPzl = pzl
  posMoves = findMoves(pzl, tknToPlay)
  if VERBOSE: printpz(newPzl, posMoves, -1)
  for ct, i in enumerate(LOM):
    if VERBOSE: print(f"{tknToPlay} plays to {i}")
    newPzl = makeMoves(newPzl, tknToPlay, i)
    tknToPlay = opptoken if token == tknToPlay else token
    posMoves = findMoves(newPzl, tknToPlay)
    if not posMoves:
      tknToPlay = opptoken if token == tknToPlay else token
      posMoves = findMoves(newPzl, tknToPlay)
    if VERBOSE:
      printpz(newPzl, posMoves, i)
      if posMoves: print(f"Possible moves for {tknToPlay}: ", *posMoves)
      print()
  return newPzl, tknToPlay

def printpz(solved, setOfPosMoves, move):
  while "*" in solved:
    solved.replace("*", ".")
  for i in range(1, SIZE+1):
    if (i-1) % WIDTH == 0 and i != 0:
      print()
    if i-1 in setOfPosMoves:
      print("*", end="")
    elif i-1 == move:
      print(solved[i-1].upper(), end="")
    else:
      print(solved[i - 1], end="")
  print()
  print()
  print(f"{solved} {solved.count('x')}/{solved.count('o')}")

def alphabeta(pzl, token, beta, alpha, topLvl):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  if (key:=(pzl, token, beta, alpha)) in CACHE_AB:
    return CACHE_AB[key]
  posMoves = findMoves(pzl, token)
  if not posMoves:
    if not findMoves(pzl, opptoken):
      CACHE_AB[(pzl, token, beta, alpha)] = [pzl.count(token) - pzl.count(opptoken)]
      return CACHE_AB[(pzl, token, beta, alpha)]
    ab = alphabeta(pzl, opptoken, -alpha, -beta, False)
    CACHE_AB[(pzl, token, beta, alpha)] = [-ab[0]] + ab[1:] + [-1] #does it have to be -alpha -beta or can it just be beta, alpha?
    return CACHE_AB[key]
  best = [beta-1]
  for mv in posMoves:
    ab = alphabeta(makeMoves(pzl, token, mv), opptoken, -alpha, -beta, False)
    score = -ab[0]
    if score < beta: continue
    if score > alpha:
      CACHE_AB[(pzl, token, beta, alpha)] = [score] + [mv]
      return CACHE_AB[(pzl, token, beta, alpha)]
    if topLvl:
      print(f"Min score: {score}, move sequence: {ab[1:] + [mv]}")
    best = [score] + ab[1:] + [mv]
    beta = score + 1
    # CACHE_AB[(pzl, token, beta, alpha)] = best
  return best

def scoreCalc(pzl, token, posMoves):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  score = 0
  oppMove = findMoves(pzl, opptoken)
  oppMoveLen = len(oppMove)
  mobility = oppMoveLen
  corners = 0
  corners = corn(pzl, token) - corn(pzl, opptoken)
  score = score+10*corners - 50*mobility
  # print(corners, mobility, score)
  return score

def corn(pzl, token):
  corner = []
  score = 0
  for i in corner_points:
    if pzl[i] == token: #corner lets go!
      score += 100
      corner.append(i)
  for i in square:
    if pzl[i] == token: # i have a square...
      if square[i] in corner: #yay i have this AND square!
        score += 150
      else:
        if i in cSq: # oh no i just have an x sq
          score -= 15
        elif i in xSq:
          score -= 90
  return score

def quickMove(pzl, token, depth):
  # rot = rotAndRef(pzl)
  if pzl in openingbook:
    return openingbook[pzl][-1]
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  if pzl.count(".") < HOLES:
    ab = alphabeta(pzl, token, -65, 65, True)
    return ab[-1]
  # rot = rotAndRef(pzl)
  # if rot: return rot[-1]
  if pzl.count(".") >= HOLES:
    mg = midGame(pzl, token, -99999, 99999, 4)
    return mg[-1]

def midGame(pzl, token, beta, alpha, depth):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  if (key := (pzl, token, beta, alpha)) in CACHE_MG:
    return CACHE_MG[key]
  posMoves = [*findMoves(pzl, token)]
  if depth == 0:
    CACHE_MG[(pzl, token, beta, alpha)] = [scoreCalc(pzl, token, posMoves)]
    return CACHE_MG[(pzl, token, beta, alpha)]
  if not posMoves:
    if not findMoves(pzl, opptoken):
      CACHE_MG[(pzl, token, beta, alpha)] = [scoreCalc(pzl, token, posMoves)]
      return CACHE_MG[(pzl, token, beta, alpha)]
    mg = midGame(pzl, opptoken, -alpha, -beta, depth-1)
    CACHE_MG[(pzl, token, beta, alpha)] = [-mg[0]] + mg[1:] + [-1]
    return CACHE_MG[(pzl, token, beta, alpha)]
  best = [beta-1]
  for mv in posMoves:
    mg = midGame(makeMoves(pzl, token, mv), opptoken, -alpha, -beta, depth-1)
    score = -mg[0]
    if score < beta: continue
    if score > alpha:
      CACHE_MG[(pzl, token, beta, alpha)] = [score] + [mv]
      return CACHE_MG[(pzl, token, beta, alpha)]
    # print(f"Min score: {score}, move sequence: {mg[1:] + [mv]}")
    best = [score] + mg[1:] + [mv]
    beta = score + 1
    # CACHE_MG[(pzl, token, beta, alpha)] = best
  return best

def main():
  first = time.process_time()
  newPzl, tknToPlay = play(BOARD, TOKEN)
  som = findMoves(newPzl, tknToPlay)
  #print("Othello 7 starting...")
  if som:
    # print(f"My preferred move is {list(som)[-1]}")
    choice = quickMove(newPzl, tknToPlay, 0)
    print(f"My preferred move is {choice}")
    # print(f"Possible moves for {tknToPlay}: ", *som)

class Strategy():
  logging = True  # Optional
  def best_strategy(self, board, player, best_move, still_running):
    depth = 1
    for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
      move = quickMove(board, player, depth)
      if move != -1:
        best_move.value = move
      depth += 1


if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024