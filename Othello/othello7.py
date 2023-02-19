import sys;args = sys.argv[1:]
if args and args[0] == '':
  args.pop(0)
import re;
import random
import time;

def convertMoves(unformattedMoves, regex):
  formatted = []
  nextMovesList = uncondense(unformattedMoves)
  for i in nextMovesList:
    if "-" not in i and int(i) < 65:
      if (x:=re.search(regex, i)):
        col = ord(i[0].upper()) - 65
        row = int(i[1])-1
        formatted.append(row*8+col)
      else:
        formatted.append(int(i))
  return formatted

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
CACHE_NM = {}
CACHE_AB = {}
CACHE_MOVES = {}
CACHE_TURN = {}
dy = [0, 0, 1, -1, -1, 1, -1, 1]
dx = [1, -1, 0, 0, 1, -1, -1, 1]
corner_points = {0, 7, 56, 63}
corner_adj = {1,8,9,6,14,15,57,48,49,62,55,54}
edges = [(0,1,2,3,4,5,6,7), (7,15,23,31,39,47,55,63),(56,57,58,59,60,61,62,63), (0,8,16,24,32,40,49,56)]
formatMoves = "^[A-Za-z]\d*$"
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
  if re.search("^(\d|_|-)+$", arg):
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
    if it in token:
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

def turn3(pzl, token, opptoken, move):
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

def makeMoves3(pzl, token, move, lastTime):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  if VERBOSE: print()
  passed = False
  newPzl = pzl[:move] + token + pzl[move + 1:]
  newPzl = turn3(newPzl, token, opptoken, move)
  som = findMoves(newPzl, opptoken)
  if VERBOSE:
    print()
    print(f"{token} plays to {move}")
    printpz(newPzl, som, move)
  if lastTime and not VERBOSE:
    print(f"{token} plays to {move}")
    printpz(newPzl, som, move)
  if som:
    if VERBOSE: print(f"Possible moves for {opptoken}: ", *som)
  else:  # MAKE IT WORK FOR PASSES
    #print("No moves possible")
    passed = True
    som = findMoves(newPzl, token)
    if som:
      if VERBOSE: print(f"Possible moves for {token}: ", *som)
    print("-----------------------")
  return som, newPzl, passed

def playOthello3(pzl, token, opptoken):
  tknToPlay = token
  start = time.process_time()
  som = findMoves(pzl, token)
  newPzl = pzl
  if som:
    if VERBOSE or not LOM:
      printpz(BOARD, som, -65)
      print(f"Possible moves for {token}: ", *som)
      print()
    count = 0
    for ct,i in enumerate(LOM):
      if count % 2 == 0:
        som, newPzl, passed = makeMoves3(newPzl, token, i, (len(LOM)-1)==ct)
        tknToPlay = opptoken
        if passed:
          count+=1
      else:
        som, newPzl, passed = makeMoves3(newPzl, opptoken, i, (len(LOM)-1)==ct)
        tknToPlay = token
        if passed:
          count+=1
      count+=1
  else:
    #print("No moves possible")
    token, opptoken = opptoken, token
    som = findMoves(pzl, token)
    if VERBOSE: printpz(BOARD, som, -65)
    if som:
      if VERBOSE:
        print(f"Possible moves for {token}: ", *som)
        print()
      count = 0
      for ct, i in enumerate(LOM):
        if count % 2 == 0:
          som, newPzl, passed = makeMoves3(newPzl, token, i, (len(LOM)-1)==ct)
          tknToPlay = opptoken
          if passed:
            count += 1
        else:
          som, newPzl, passed = makeMoves3(newPzl, opptoken, i, (len(LOM)-1)==ct)
          tknToPlay = token
          if passed:
            count += 1
        count += 1
  if som:
    print(f"My preferred move is: {[*som][-1]}")
    print()
  return som, newPzl, tknToPlay

def printpz(solved, setOfPosMoves, move):
  while "*" in solved:
    solved.replace("*", ".")
  for i in range(1, SIZE+1):
    if (i-1) % WIDTH == 0 and i != 0:
      print()
    if i-1 in setOfPosMoves:
      print("*", end="")
    elif i == move+1:
      print(solved[i-1].upper(), end="")
    else:
      print(solved[i - 1], end="")
  print()
  print()
  print(f"{solved} {solved.count('x')}/{solved.count('o')}")

def alphabeta(pzl, token, beta, alpha, topLvl):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  posMoves = findMoves(pzl, token)
  if not posMoves:
    if not findMoves(pzl, opptoken):
      return [pzl.count(token) - pzl.count(opptoken)]
    ab = alphabeta(pzl, opptoken, -alpha, -beta, False)
    return [-ab[0]] + ab[1:] + [-1]
  best = [beta-1]
  for mv in posMoves:
    ab = alphabeta(makeMoves(pzl, token, mv), opptoken, -alpha, -beta, False)
    score = -ab[0]
    if score < beta: continue
    if score > alpha: return [score] + [mv]
    if topLvl:
      print(f"Min score: {score}, move sequence: {ab[1:] + [mv]}")
    best = [score] + ab[1:] + [mv]
    beta = score + 1
  return best

def stability(pzl, token, posMoves):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  corners = sum(1 for i in corner_points if i in posMoves)
  oppPosMoves = findMoves(pzl, opptoken)
  oppCorners = sum(1 for i in corner_points if i in oppPosMoves)
  stability = 0
  if corners + oppCorners > 0:
    stability = 100*(corners - oppCorners)/(corners+oppCorners)
  return stability

def scoreCalc(pzl, token, posMoves):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  score = 0
  oppMoveLen = len(findMoves(pzl, opptoken))
  score = 3 * (-oppMoveLen)
  cornerCount = 0
  for i in corner_points:
    if pzl[i] == token: cornerCount+=1
    elif pzl[i] == opptoken: cornerCount-=1
  score += 100*cornerCount
  return score

def safe_edge(pzl, token, posMoves):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  wedge = opptoken+"."+opptoken
  corner = []
  moves = set()
  for i in corner_points:
    if pzl[i] == token:
      corner.append(i)
  edgePieces = []
  for tup in edges:
    edgePieces.append("".join(pzl[i] for i in tup))
  for ind, ed in enumerate(edgePieces):
    if ed[0] == token:
      for ct, i in enumerate(ed):
        if i == ".":
          moves.add(edges[ind][ct])
          break;
    elif ed[7] == token:
      for ct, i in enumerate(ed[::-1]):
        if i == ".":
          moves.add(7-edges[ind][ct])
          break;
  for i in {*moves}:
    if i not in posMoves:
      moves = moves - {i}
  return [*moves]
def quickMove(pzl, token, depth):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  if pzl.count(".") >= HOLES:
    mg = midGame(pzl, token, -99999, 99999, 4)
    return mg[-1]
  if pzl.count(".") < HOLES:
    nm = alphabeta(pzl, token, -65, 65, True)
    return nm[-1]
  posMoves = [*findMoves(pzl, token)]
  posMoves_cpy = [*posMoves]
  for i in corner_points:
    if i in posMoves_cpy:
      return i
  for j in corner_adj:
    if j in posMoves_cpy:
      posMoves_cpy.remove(j)
  if posMoves_cpy:
    posMoves = posMoves_cpy
  ed = safe_edge(pzl, token, posMoves)
  if ed:
    return ed[0]
  choice = posMoves[0]
  #mobility section
  mobility = 1000 #possible moves
  for mv in posMoves:
    futureMoves = findMoves(makeMoves(pzl, token, mv), opptoken)
    corner = sum(1 for i in futureMoves if i in corner_adj)
    if corner == 0:
      moves = len(futureMoves)
      if moves < mobility:
        choice = mv
        mobility = moves
  return choice

def midGame(pzl, token, beta, alpha, depth):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  posMoves = [*findMoves(pzl, token)]
  if depth == 0:
    return [scoreCalc(pzl, token, posMoves)]
  if not posMoves:
    if not findMoves(pzl, opptoken):
      return [scoreCalc(pzl, token, posMoves)]
    mg = midGame(pzl, opptoken, -alpha, -beta, depth-1)
    return [-mg[0]] + mg[1:] + [-1]
  best = [beta-1]
  for mv in posMoves:
    mg = midGame(makeMoves(pzl, token, mv), opptoken, -alpha, -beta, depth-1)
    score = -mg[0]
    #print(score, beta, alpha)
    if score < beta: continue
    if score > alpha: return [score] + [mv]
    #print(f"Min score: {score}, move sequence: {mg[1:] + [mv]}")
    best = [score] + mg[1:] + [mv]
    beta = score + 1
  return best

def main():
  first = time.process_time()
  som, newPzl, tknToPlay = playOthello3(BOARD, TOKEN, OPPTOKEN)
  string = ", ".join(str(i) for i in som)
  choice = [0]
  #print("Othello 7 starting...")
  if som:
    choice = quickMove(newPzl, tknToPlay, 0)
    print(f"My preferred move is {choice}")
    # if newPzl.count(".") >= HOLES:
    #   choice = midGame(newPzl, tknToPlay, -99999, 99999, 4)
    # if newPzl.count(".") < HOLES:
    #   nm = alphabeta(newPzl, tknToPlay, -65, 65, True)
    #   #print(f"Min score: {nm[0]}, move sequence: {nm[1:]}")
    #   choice = nm
    print(f"Possible moves for {tknToPlay}: {string}")
    print(f"My preferred move is {choice}")

  # print(f"Elapsed time: {(time.process_time() - first)}s")
  # print(STATS)
  # print(((STATS['cacheNMHit'] - STATS["cacheNMSize"])/(STATS['cacheNMHit']))*100)
  print()

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024