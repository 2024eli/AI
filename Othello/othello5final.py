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
CACHE_NM = {}
CACHE_MOVES = {}
STATS = {"cacheNMHit": 0, "cacheNMSize": 0} #10% cache hit
dy = [0, 0, 1, -1, -1, 1, -1, 1]
dx = [1, -1, 0, 0, 1, -1, -1, 1]
corner_adj = {0: (1, 8, 9), 7:(6, 14, 15), 56:(57, 48, 49), 63:(62, 55, 54)}
edges = [(0,1,2,3,4,5,6,7), (7,15,23,31,39,47,55,63),(56,57,58,59,60,61,62,63), (0,8,16,24,32,40,49,56)]
formatMoves = "^[A-Za-z]\d*$"
if args and len(args[0]) == 64:
  BOARD = args[0].lower()
  if len(args) >=2 and len(args[1]) == 1 and re.search("^[XOxo]$", args[1]):
    TOKEN = args[1].lower()
    LOM = convertMoves(args[2:], formatMoves)
  else:
    if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
    else: TOKEN = 'o'
    LOM = convertMoves(args[1:], formatMoves)
else:
  BOARD = '.'*27+'ox......xo'+'.'*27
  if len(args) >=2 and len(args[0]) == 1 and re.search("^[XOxo]$", args[0]):
    TOKEN = args[0].lower()
    LOM = convertMoves(args[1:], formatMoves)
  else:
    if (64-BOARD.count('.')) % 2 == 0: TOKEN = 'x'
    else: TOKEN = 'o'
    LOM = convertMoves(args[0:], formatMoves)
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
  return ''.join(newPzl)

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
  print(f"{token} plays to {move}")
  newPzl = pzl[:move] + token + pzl[move + 1:]
  newPzl = turn3(newPzl, token, opptoken, move)
  som = findMoves(newPzl, opptoken)
  printpz(newPzl, som)
  if som:
    print(f"Possible moves for {opptoken}: ", *som)
  else:  # MAKE IT WORK FOR PASSES
    print("No moves possible")
    passed = True
    som = findMoves(newPzl, token)
    if som:
      print(f"Possible moves for {token}: ", *som)
  return som, newPzl, passed

def playOthello3(pzl, token, opptoken):
  tknToPlay = token
  start = time.process_time()
  som = findMoves(pzl, token)
  printpz(BOARD, som)
  if som:
    print(f"Possible moves for {token}: ", *som)
    print()
    count = 0
    newPzl = BOARD
    for i in LOM:
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
    print("No moves possible")
    token, opptoken = opptoken, token
    som = findMoves(pzl, token)
    if som:
      print(f"Possible moves for {token}: ", *som)
      print()
      count = 0
      newPzl = BOARD
      for i in LOM:
        if count % 2 == 0:
          som, newPzl, passed = makeMoves3(newPzl, token, i)
          tknToPlay = opptoken
          if passed:
            count += 1
        else:
          som, newPzl, passed = makeMoves3(newPzl, opptoken, i)
          tknToPlay = token
          if passed:
            count += 1
        count += 1
  print()
  return som, newPzl, tknToPlay

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

def quickMove(pzl, token):
  if pzl.count(".") < 8:
    nm = negamax(pzl, token, True)
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
  print(tknToPlay)
  print("othello5 code starting...")
  if (pos:=findMoves(newPzl, tknToPlay)):
    choice = quickMove(newPzl, tknToPlay)
    print(f"Possible moves for {tknToPlay}: {', '.join(str(i) for i in pos)}")
    print(f"The preferred move is {choice}")
    if newPzl.count(".") < 11:
      nm = negamax(newPzl, tknToPlay, True)
      return nm[-1]
  print(f"Elapsed time: {(time.process_time() - first)}s")
  # print(STATS)
  # print(((STATS['cacheNMHit'] - STATS["cacheNMSize"])/(STATS['cacheNMHit']))*100)
  print()

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024