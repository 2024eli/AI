import sys; args = sys.argv[1:]
import random
import time;

if args:
  PZ1 = args[0]
else:
  PZ1 = "."*49
  PZ2 = "."*24

gCHOICES = {}
lookUp2 = {1: (0, 1, 2, 6, 7, 8),
           2: (2, 3, 4, 8, 9, 10),
           3: (5, 6, 7, 12, 13, 14),
           4: (7, 8, 9, 14, 15, 16),
           5: (9, 10, 11, 16, 17, 18),
           6: (13, 14, 15, 19, 20, 21),
           7: (15, 16, 17, 21, 22, 23)}
lookUp3 = {1: (12, 5, 6, 0, 1),
           2: (19, 13, 14, 7, 8, 2, 3),
           3: (20, 21, 15, 16, 9, 10, 4),
           4: (22, 23, 17, 18, 11),
           5: (0, 1, 2, 3, 4),
           6: (5, 6, 7, 8, 9, 10, 11),
           7: (12, 13, 14, 15, 16, 17, 18),
           8: (19, 20, 21, 22, 23),
           9: (3, 4, 10, 11, 18),
           10: (1, 2, 8, 9, 16, 17, 23),
           11: (0, 6, 7, 14, 15, 21, 22),
           12: (5, 12, 13, 19, 20)}

def printPzl(board, q):
  print("Q" + str(q))
  if q==1:
    print("board", board)
    n = int(len(board) ** (1 / 2))
    for i in range(len(board)):
      if i % n == 0 and i != 0:
        print()
      print(board[i], end="")
    print()
    print()
  if q==2:
    print(board + " =>")
    boardlst = list(board)
    s = "".join([str(int(i)+1) for i in boardlst])
    print(" " + s[0:5] + " ")
    print(s[5:12])
    print(s[12:19])
    print(" " + s[19:] + " ")
    print()
    print()
  if q==3:
    print(board + " =>")
    boardlst = list(board)
    s = "".join([str(int(i) + 1) for i in boardlst])
    print(" " + s[0:5] + " ")
    print(s[5:12])
    print(s[12:19])
    print(" " + s[19:] + " ")
    print()
    print()

def isInvalid1(pzl):
  pzlStr = pzl[0]
  dot = pzl[1]
  n = int(len(pzlStr) ** (1 / 2))
  now = pzlStr[dot]
  lst = []
  lrDia = []
  rlDia = []
  for ct, i in enumerate(pzlStr):
    if i == now:
      lst.append(((r:=ct//n), (c:=ct%n)))
      if r==c:
        lrDia.append((r, c))
      if r+c == n-1:
        rlDia.append((r, c))
  if len(rlDia) > 1 or len(lrDia) > 1:
    return True
  for i in range(len(lst)):
    for j in range(i+1, len(lst)):
      if lst[i][0] == lst[j][0] or lst[i][1] == lst[j][1]:
        return True
  return False

def isFinished(pzl):
  return "." not in pzl

def findChoices(pzl, n):
  c = set()
  for ct, it in enumerate(pzl):
    if it == ".":
      for num in range(n):
        s = pzl[0:ct] + str(num) + pzl[ct+1:]
        if s not in gCHOICES:
          c.add((s, ct))
      break
  return c

def q1Solver(pzl):
  #returns a solved puzzle if possible else ""
  if (p:=pzl[0]) != len(p) * p[0] and isInvalid1(pzl):
    return ""
  if isFinished(pzl[0]):
    return pzl[0]
  choices = findChoices((p:=pzl[0]), int(len(p) ** (1 / 2)))
  for choice in choices:
    gCHOICES[choice[0]] = ""
    bF = q1Solver(choice)
    if bF:
      return bF
  return ""

def isInvalid2(pzl):
  pzlStr = pzl[0]
  dot = pzl[1]
  n = int(len(pzlStr) ** (1 / 2))
  now = pzlStr[dot]
  for i in lookUp2:
    if dot in lookUp2[i]:
      for j in lookUp2[i]:
        if j != dot:
          if pzlStr[j] == now:
            return True
  return False

def q2Solver(pzl):
  if (p := pzl[0]) != len(p) * p[0] and isInvalid2(pzl):
    return ""
  if isFinished(pzl[0]):
    return pzl[0]
  choices = findChoices(pzl[0], 6)
  for choice in choices:
    gCHOICES[choice[0]] = ""
    bF = q2Solver(choice)
    if bF:
      return bF
  return ""

def isInvalid3(pzl):
  pzlStr = pzl[0]
  dot = pzl[1]
  n = int(len(pzlStr) ** (1 / 2))
  now = pzlStr[dot]
  for i in lookUp2:
    if dot in lookUp2[i]:
      for j in lookUp2[i]:
        if j != dot:
          if pzlStr[j] == now:
            return True
  for i in lookUp3:
    if dot in lookUp3[i]:
      for j in lookUp3[i]:
        if j != dot:
          if pzlStr[j] == now:
            return True
  return False

def q3Solver(pzl):
  if (p := pzl[0]) != len(p) * p[0] and isInvalid3(pzl):
    return ""
  if isFinished(pzl[0]):
    return pzl[0]
  choices = findChoices(pzl[0], 7)
  for choice in choices:
    gCHOICES[choice[0]] = ""
    bF = q3Solver(choice)
    if bF:
      return bF
  return ""

if __name__ == '__main__':
  gCHOICES = {}
  start = time.process_time()
  printPzl(q1Solver(("." * 49, 0)), 1)
  print(f"time: {time.process_time() - start}s")
  gCHOICES = {}
  start = time.process_time()
  printPzl(q2Solver(('.' * 24, 0)), 2)
  print(f"time: {time.process_time() - start}s")
  gCHOICES = {}
  start = time.process_time()
  printPzl(q3Solver(('.' * 24, 0)), 3)
  print(f"time: {time.process_time()-start}s")

'''
Q1 solution:
1 2 0 6 3 4 5
6 3 5 4 2 1 0
2 1 4 5 6 0 3
4 5 3 0 1 6 2
0 6 2 1 5 3 4
5 4 6 3 0 2 1
3 0 1 2 4 5 6

Q2 solution:
  6 5 4 6 2  
4 2 3 1 5 3 4
1 5 6 4 2 6 1
  2 1 3 1 5 
  
Q3 solution: no solution
'''

# Evelyn Li, pd 7, 2024