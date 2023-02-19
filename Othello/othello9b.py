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

#rotation/reflection
def rotAndRef(b): #b is board = pzl, w is width = 8
  w = 8
  if b in openingbook: return True, openingbook[b]
  L = [b, "".join(b[rs:rs + w][::-1] for rs in range(0, len(b), w))]
  if L[1] in openingbook: return True, translateMoves(b, L[1], "VF")
  L += ["".join(d[cs::w][::-1] for cs in range(w)) for d in L]
  if L[2] in openingbook: return True, translateMoves(b, L[2], '1|90CW')
  if L[3] in openingbook: return True, translateMoves(b, L[3], "VF|90CW")
  L += ["".join(d[::-1]) for d in L]
  if L[4] in openingbook: return True, translateMoves(b, L[4], "1|180")
  if L[5] in openingbook: return True, translateMoves(b, L[5], "VF|180")
  if L[6] in openingbook: return True, translateMoves(b, L[6], "1|90CW|180")
  if L[7] in openingbook: return True, translateMoves(b, L[7], "VF|90CW|180")
  return False, 0

#rotations and reflect the moves back to correct
def translateMoves(og, book, tran):
  print('translating moves')
  moves = openingbook[book]
  transKey = transformations[tran]
  realMoves = []
  for i in moves:
    realMoves.append(transKey[i])
  return realMoves

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
corner_points = {0, 7, 56, 63}
corner_adj = {1,8,9,6,14,15,57,48,49,62,55,54}
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
               'xxxxxxxxxxoxxoxxxooxoxoxxxoxxoxxxxoxoxxxxxooxxxx..oooo.x........': [49],
               'oxxxxxxxooooxooxoooxxxoxoooxxxoxoooxoooxooxxoooxooooo...x.oo....': [61],
               'xxxxxxxxxxooxoooxoxxxxooxooxxoxoxooxooo.xoxxoo..ooooo...x.oo....': [47]
               }
# transformations = {'VF': {42: 45, 45: 42, 3: 4, 4: 3, 35: 36, 36: 35, 41: 46, 46: 41, 9: 14, 14: 9, 40: 47, 47: 40, 34: 37, 37: 34, 1: 6, 6: 1, 2: 5, 5: 2, 8: 15, 15: 8, 27: 28, 28: 27, 32: 39, 39: 32, 33: 38, 38: 33, 58: 61, 61: 58, 59: 60, 60: 59, 26: 29, 29: 26, 51: 52, 52: 51, 0: 7, 7: 0, 57: 62, 62: 57, 19: 20, 20: 19, 56: 63, 63: 56, 18: 21, 21: 18, 24: 31, 31: 24, 25: 30, 30: 25, 43: 44, 44: 43, 50: 53, 53: 50, 49: 54, 54: 49, 10: 13, 13: 10, 11: 12, 12: 11, 17: 22, 22: 17, 48: 55, 55: 48, 16: 23, 23: 16},
#                    '1|90CW': {55: 6, 57: 55, 30: 11, 52: 30, 29: 19, 44: 29, 9: 14, 14: 54, 3: 31, 31: 60, 27: 28, 28: 36, 4: 39, 39: 59, 22: 10, 53: 22, 36: 28, 1: 15, 15: 62, 2: 23, 23: 61, 10: 22, 61: 23, 47: 5, 58: 47, 46: 13, 50: 46, 20: 37, 37: 43, 0: 7, 7: 63, 21: 18, 45: 21, 62: 15, 59: 39, 19: 29, 54: 14, 18: 21, 13: 46, 38: 12, 51: 38, 12: 38, 6: 55, 43: 37, 11: 30, 63: 7, 60: 31, 5: 47},
#                    'VF|90CW': {6: 15, 15: 6, 9: 54, 54: 9, 10: 46, 46: 10, 33: 51, 51: 33, 20: 29, 29: 20, 1: 55, 55: 1, 0: 63, 63: 0, 24: 60, 60: 24, 48: 57, 57: 48, 34: 43, 43: 34, 19: 37, 37: 19, 7: 7, 11: 38, 38: 11, 35: 35, 21: 21, 2: 47, 47: 2, 26: 44, 44: 26, 25: 52, 52: 25, 12: 30, 30: 12, 49: 49, 16: 61, 61: 16, 40: 58, 58: 40, 3: 39, 39: 3, 27: 36, 36: 27, 13: 22, 22: 13, 17: 53, 53: 17, 41: 50, 50: 41, 14: 14, 8: 62, 62: 8, 32: 59, 59: 32, 18: 45, 45: 18, 5: 23, 23: 5, 4: 31, 31: 4, 28: 28, 56: 56, 42: 42},
#                    '1|180': {17: 46, 46: 17, 9: 54, 54: 9, 25: 38, 38: 25, 24: 39, 39: 24, 8: 55, 55: 8, 31: 32, 32: 31, 16: 47, 47: 16, 15: 48, 48: 15, 0: 63, 63: 0, 7: 56, 56: 7, 23: 40, 40: 23, 22: 41, 41: 22, 6: 57, 57: 6, 30: 33, 33: 30, 14: 49, 49: 14, 5: 58, 58: 5, 29: 34, 34: 29, 13: 50, 50: 13, 21: 42, 42: 21, 20: 43, 43: 20, 28: 35, 35: 28, 27: 36, 36: 27, 12: 51, 51: 12, 19: 44, 44: 19, 4: 59, 59: 4, 3: 60, 60: 3, 26: 37, 37: 26, 11: 52, 52: 11, 10: 53, 53: 10, 18: 45, 45: 18, 2: 61, 61: 2, 1: 62, 62: 1},
#                    'VF|180': {19: 43, 43: 19, 3: 59, 59: 3, 11: 51, 51: 11, 20: 44, 44: 20, 28: 36, 36: 28, 12: 52, 52: 12, 4: 60, 60: 4, 24: 32, 32: 24, 8: 48, 48: 8, 5: 61, 61: 5, 16: 40, 40: 16, 29: 37, 37: 29, 0: 56, 56: 0, 13: 53, 53: 13, 1: 57, 57: 1, 21: 45, 45: 21, 22: 46, 46: 22, 6: 62, 62: 6, 17: 41, 41: 17, 30: 38, 38: 30, 14: 54, 54: 14, 25: 33, 33: 25, 9: 49, 49: 9, 26: 34, 34: 26, 10: 50, 50: 10, 18: 42, 42: 18, 31: 39, 39: 31, 2: 58, 58: 2, 15: 55, 55: 15, 23: 47, 47: 23, 27: 35, 35: 27, 7: 63, 63: 7},
#                    '1|90CW|180': {42: 18, 45: 42, 35: 27, 36: 35, 20: 26, 26: 43, 5: 16, 16: 58, 4: 24, 24: 59, 12: 25, 25: 51, 13: 17, 17: 50, 6: 8, 8: 57, 11: 33, 33: 52, 57: 8, 1: 48, 48: 62, 0: 56, 56: 63, 59: 24, 32: 3, 60: 32, 58: 16, 40: 2, 61: 40, 62: 48, 63: 56, 50: 17, 2: 40, 10: 41, 41: 53, 9: 49, 49: 54, 52: 33, 53: 41, 18: 42, 43: 26, 51: 25, 54: 49, 34: 19, 44: 34, 3: 32, 27: 35, 19: 34},
#                    'VF|90CW|180': {7: 56, 56: 7, 6: 48, 48: 6, 15: 57, 57: 15, 39: 60, 60: 39, 5: 40, 40: 5, 14: 49, 49: 14, 22: 50, 50: 22, 31: 59, 59: 31, 23: 58, 58: 23, 30: 51, 51: 30, 47: 61, 61: 47, 55: 62, 62: 55, 13: 41, 41: 13, 3: 24, 24: 3, 12: 33, 33: 12, 20: 34, 34: 20, 27: 27, 21: 42, 42: 21, 29: 43, 43: 29, 38: 52, 52: 38, 4: 32, 32: 4, 46: 53, 53: 46, 63: 63, 54: 54, 1: 8, 8: 1, 2: 16, 16: 2, 10: 17, 17: 10, 19: 26, 26: 19, 28: 35, 35: 28, 36: 36, 11: 25, 25: 11, 37: 44, 44: 37, 18: 18, 0: 0, 9: 9, 45: 45}}
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
  oppMoveLen = len(findMoves(pzl, opptoken))
  mobility = oppMoveLen
  corners = 0
  x = 0
  c = 0
  for i in corner_points:
    if pzl[i] == token: corners += 1
  for i in xSq:
    if pzl[i] == token: x += 1
  for i in cSq:
    if pzl[i] == token: c += 1
  score = 9500*corners - 1500*x - 800*c - 30*mobility
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
  if pzl.count(".") >= HOLES:
    mg = midGame(pzl, token, -99999, 99999, 3)
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

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024