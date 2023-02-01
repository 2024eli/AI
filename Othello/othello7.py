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
    if "-" not in i:
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
HOLES = 13
CACHE_NM = {}
CACHE_AB = {}
CACHE_MOVES = {}
CACHE_TURN = {}
STATS = {"cacheNMHit": 0, "cacheNMSize": 0} #10% cache hit
dy = [0, 0, 1, -1, -1, 1, -1, 1]
dx = [1, -1, 0, 0, 1, -1, -1, 1]
corner_adj = {0: (1, 8, 9), 7:(6, 14, 15), 56:(57, 48, 49), 63:(62, 55, 54)}
edges = [(0,1,2,3,4,5,6,7), (7,15,23,31,39,47,55,63),(56,57,58,59,60,61,62,63), (0,8,16,24,32,40,49,56)]
formatMoves = "^[A-Za-z]\d*$"
BOARD = '.'*27+'ox......xo'+'.'*27
TOKEN = 'x'
LOM = []
specialToken = False
for arg in args:
  if len(arg) == 64:
    BOARD = arg.lower()
  if re.search("^HL", arg):
    HOLES = int(arg[2:])
  if re.search("^[XxOo]$", arg):
    specialToken = True
    TOKEN = arg
  if re.search("^(\d|_)+$", arg):
    LOM.append(arg)
if not specialToken:
  if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
  else: TOKEN = 'o'
LOM = convertMoves(LOM, formatMoves)
OPPTOKEN = "o" if TOKEN == 'x' else "x"
# print("board: ", BOARD)
# print("token: ", TOKEN)
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

def makeMoves3(pzl, token, move):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  print()
  passed = False
  print()
  print(f"{token} plays to {move}")
  newPzl = pzl[:move] + token + pzl[move + 1:]
  newPzl = turn3(newPzl, token, opptoken, move)
  som = findMoves(newPzl, opptoken)
  printpz(newPzl, som, move)
  if som:
    print(f"Possible moves for {opptoken}: ", *som)
  else:  # MAKE IT WORK FOR PASSES
    #print("No moves possible")
    passed = True
    som = findMoves(newPzl, token)
    if som:
      print(f"Possible moves for {token}: ", *som)
  return som, newPzl, passed

def playOthello3(pzl, token, opptoken):
  tknToPlay = token
  start = time.process_time()
  som = findMoves(pzl, token)
  newPzl = pzl
  if som:
    printpz(BOARD, som, -65)
    print(f"Possible moves for {token}: ", *som)
    print()
    count = 0
    for ct,i in enumerate(LOM):
      if count % 2 == 0:
        som, newPzl, passed = makeMoves3(newPzl, token, i)
        tknToPlay = opptoken
        if passed:
          count+=1
      else:
        som, newPzl, passed = makeMoves3(newPzl, opptoken, i)
        tknToPlay = token
        if passed:
          count+=1
      count+=1
  else:
    #print("No moves possible")
    token, opptoken = opptoken, token
    som = findMoves(pzl, token)
    printpz(BOARD, som, -65)
    if som:
      print(f"Possible moves for {token}: ", *som)
      print()
      count = 0
      for ct, i in enumerate(LOM):
        if count % 2 == 0:
          som, newPzl, passed = makeMoves3(newPzl, token, i)
          print(tknToPlay, passed)
          tknToPlay = opptoken
          if passed:
            count += 1
        else:
          som, newPzl, passed = makeMoves3(newPzl, opptoken, i)
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

def safe_edge(pzl, token, posMoves):
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  wedge = opptoken+"."+opptoken
  corner = []
  moves = set()
  for i in corner_adj:
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

def negamax(pzl, token, topLvl):
  #returns a list of the best pos score that tkn
  #can achieve, along with an optimal (reversed) move
  #sequence that can get tkn there.
  if (key:=(pzl, token)) in CACHE_NM:
    return CACHE_NM[key]
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  posMoves = findMoves(pzl, token)
  if pzl.count('.') == 0 or (not posMoves and not (oppPosMoves:=findMoves(pzl, opptoken))):
    return [pzl.count(token) - pzl.count(opptoken)]
  if not posMoves and oppPosMoves:
    nm = negamax(pzl, opptoken, False)
    CACHE_NM[key] = [-nm[0]] + nm[1:] + [-1]
    return CACHE_NM[key]
  bestSoFar = [-65]
  for mv in posMoves:
    newPzl = makeMoves(pzl, token, mv)
    nm = negamax(newPzl, opptoken, False)
    if -nm[0] > bestSoFar[0]:
      if topLvl:
        print(f"Min score: {-nm[0]}, move sequence: {nm[1:] + [mv]}")
      CACHE_NM[key] = [-nm[0]] + nm[1:] + [mv]
      bestSoFar = CACHE_NM[key]
  return bestSoFar

def alphabeta(pzl, token, beta, alpha, topLvl):
  if (key:=(pzl, token, beta, alpha)) in CACHE_AB:
    return CACHE_AB[key]
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  posMoves = findMoves(pzl, token)
  if not posMoves:
    if not findMoves(pzl, opptoken):
      return [pzl.count(token) - pzl.count(opptoken)]
    ab = alphabeta(pzl, opptoken, -alpha, -beta, False)
    CACHE_AB[key] = [-ab[0]] + ab[1:] + [-1]
    return CACHE_AB[key]
  best = [beta-1]
  for mv in posMoves:
    ab = alphabeta(makeMoves(pzl, token, mv), opptoken, -alpha, -beta, False)
    score = -ab[0]
    if score < beta: continue
    if score > alpha:
      return [score]
    if topLvl:
      print(f"Min score: {score}, move sequence: {ab[1:] + [mv]}")
    CACHE_AB[key] = [score] + ab[1:] + [mv]
    best = [score] + ab[1:] + [mv]
    beta = score + 1
  return best

def quickMove(pzl, token):
  global HOLES
  if pzl==BOARD:
    CACHE_AB.clear()
  if (pzl == ""):
    HOLES = token
  if pzl.count(".") < HOLES:
    nm = alphabeta(pzl, token, -65, 65, True)
    return nm[-1]
  opptoken = 'o'
  if token.lower() == 'o': opptoken = "x"
  posMoves = [*findMoves(pzl, token)]
  posMoves_cpy = [*posMoves]
  for i in corner_adj:
    if i in posMoves_cpy:
      return i
  for i in corner_adj:
    if pzl[i] == "." or pzl[i] == opptoken:
      for j in corner_adj[i]:
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

def main():
  first = time.process_time()
  som, newPzl, tknToPlay = playOthello3(BOARD, TOKEN, OPPTOKEN)
  print("othello6 (alpha beta pruning) code starting...")
  if (pos:=findMoves(newPzl, tknToPlay)):
    choice = quickMove(newPzl, tknToPlay)
    print(f"Possible moves for {tknToPlay}: {', '.join(str(i) for i in pos)}")
    print(f"The preferred move is {choice}")
    if newPzl.count(".") < HOLES:
      nm = alphabeta(newPzl, tknToPlay, -65, 65, True)
      #print(f"Min score: {nm[0]}, move sequence: {nm[1:]}")
      return nm[-1]
  print(f"Elapsed time: {(time.process_time() - first)}s")
  # print(STATS)
  # print(((STATS['cacheNMHit'] - STATS["cacheNMSize"])/(STATS['cacheNMHit']))*100)
  print()

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024