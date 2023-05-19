import sys;args = sys.argv[1:]
import re
import random
import time

# args = 'someDct.txt 13x13 32 H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5stirrup H4x2##Ordained V0x1Proc V0x12Mah V5x0zoo'.split(' ')
if not args[0].upper().endswith('.TXT'):
  args = [0] + args

def printpzString(pzl):
  if pzl == False:
    print('False')
    return False
  for ct, it in enumerate(pzl):
    print(it, end=' ')
    if (ct+1) % WIDTH == 0:
      print()
  print()

def add(pzl, ind, ch):
  return pzl[:ind] + ch + pzl[ind+1:]

def add1(pzl, x, y, ch):
  pzl[y] = pzl[y][0:x] + ch + pzl[y][x+1:]

# def symmetry(pzl):

def cont(pzl, index):
  if pzl[index] != '-' and not pzl[index].isalpha(): return pzl
  col, row = index % WIDTH, index // WIDTH
  pzl = add(pzl, index, '$')
  if row > 0:
    pzl = cont(pzl, index-WIDTH)
  if row < HEIGHT-1:
    pzl = cont(pzl, index+WIDTH)
  if col > 0:
    pzl = cont(pzl, index-1)
  if col < WIDTH-1:
    pzl = cont(pzl, index+1)
  return pzl

def insert(pzl, ind):
  if pzl[ind].isalpha(): return False
  pzl = add(pzl, ind, '#')
  row, col = ind // WIDTH, ind % WIDTH
  if row != 0 and pzl[(up:=(row-1)*WIDTH+col)] != '#':
    if row in (1, 2):
      pzl = insert(pzl, up)
      if pzl==False: return False
    else: #has to have at least a two margin on top
      go = False
      for i in range((row-2)*WIDTH+col, (row-4)*WIDTH+col, -WIDTH):
        if pzl[i] == '#':
          go = True
          break
      if go:
        pzl = insert(pzl, up)
        if not pzl: return False
  if row != HEIGHT-1 and pzl[(down:=(row+1)*WIDTH+col)] != '#':
    if row > HEIGHT-4:
      pzl = insert(pzl, down)
      if not pzl: return False
    else:
      go = False
      for i in range((row + 2) * WIDTH + col, (row + 4) * WIDTH + col, WIDTH):
        if pzl[i] == '#':
          go = True
          break
      if go:
        pzl = insert(pzl, down)
        if not pzl: return False
  if col != 0 and pzl[(left:=row*WIDTH+col-1)] != '#':
    if col in (1, 2):
      pzl = insert(pzl, left)
      if not pzl: return False
    else:
      go = False
      for i in range(row * WIDTH + col-3, row * WIDTH + col-1):
        if pzl[i] == '#':
          go = True
          break
      if go:
        pzl = insert(pzl, left)
        if not pzl: return False
  if col != WIDTH-1 and pzl[(right:=row*WIDTH+col+1)] != '#':
    if col > WIDTH-4:
      pzl = insert(pzl, right)
      if not pzl: return False
    else:
      go = False
      for i in range(row * WIDTH + col+2, row * WIDTH + col+4):
        if pzl[i] == '#':
          go = True
          break
      if go:
        pzl = insert(pzl, right)
        if not pzl: return False
  return pzl

def put(pzl, ind):
  pzl = insert(pzl, ind)
  if pzl: pzl = insert(pzl, SIZE-ind-1)
  return pzl

def bruteForce(pzl):
  if (bl:=pzl.count('#')) == BLOCKINGARG: return pzl
  elif bl > BLOCKINGARG: return False
  printpz(pzl)
  if '-' in cont(pzl, pzl.find('-')): return False
  for i in {j for j, c in enumerate(pzl) if c == '-'}:
    newPzl = put(pzl, i)
    if newPzl:
      bF = bruteForce(newPzl)
      if bF:
        return bF
  return False

#takes all blocking and does symmetry on them
def symmetry(pzl):
  #transform 180
  pzlFlip = pzl[::-1]
  flip = []
  for i in range(len(pzlFlip)):
    flip.append(pzlFlip[i][::-1])
  for i, f in enumerate(flip):
    for j, ch in enumerate(f):
      if ch == '#' and not 65 <= ord(pzl[i][j]) <= 90:
        add1(pzl, j, i, '#')
      if 65 <= ord(ch) <= 90 and pzl[i][j] == '.':
        add1(pzl, j, i, '-')
  return pzl

def setUpPzl(pzl, pos):
  for tup in pos:
    direc, row, col = tup[0], tup[1], tup[2]
    content = pos[tup]
    if direc == 'V':
      for i in content:
        if col + 1 != WIDTH:
          pzl[row] = pzl[row][0:col] + i + pzl[row][col + 1:]
        else:
          pzl[row] = pzl[row][0:col] + i
        row += 1
    else:
      pzl[row] = pzl[row][0:col] + content + pzl[row][col + len(content):]
  if HEIGHT % 2 + WIDTH % 2 + BLOCKING % 2 == 3:
    add1(pzl, WIDTH // 2, HEIGHT // 2, '#')
  elif HEIGHT % 2 + WIDTH % 2 == 2:
    add1(pzl, WIDTH // 2, HEIGHT // 2, '-')
  # symmetry
  pzl = symmetry(pzl)
  return pzl

def check1(pzl, ch):
  for i in range(len(pzl)):
    for j in range(len(pzl[i])):
      if (p:=pzl[i][j]) == '.':
        return (j, i)
  return True
def contiguousHelper(pzl, c, r, ch, symbolsUsed):
  if 0 <= r < HEIGHT and 0 <= c < WIDTH and ((p:=pzl[r][c]) in ('-','.') or p in symbolsUsed or p.isalpha()):
    add1(pzl, c, r, ch) #PATH
    contiguousHelper(pzl, c, r+1, ch, symbolsUsed)
    contiguousHelper(pzl, c, r-1, ch, symbolsUsed)
    contiguousHelper(pzl, c+1, r, ch, symbolsUsed)
    contiguousHelper(pzl, c-1, r, ch, symbolsUsed)
  return pzl

def cont(pzl, blocking, c, r):
  xW = [i for i in pzl]
  block = 0
  innerSet = set()
  contiguousHelper(xW, c, r, '=', innerSet)
  isIt = check1(xW, '=')
  innerSet.add('=')
  i = 0
  while isIt != True:
    symbol = SYMBOLSET[i]
    contiguousHelper(xW, isIt[0], isIt[1], symbol, innerSet)
    innerSet.add(symbol)
    isIt = check1(xW, symbol)
    i+=1
  xWord = [i for i in xW]
  while innerSet:
    symbol = innerSet.pop()
    for i in range(HEIGHT):
      if block + blocking < 0: break
      if symbol in (s:=xWord[i]):
        for ch in range(WIDTH):
          if xWord[i][ch] == symbol:
            add1(xWord, ch, i, '#')
            block -= 1
          if block + blocking < 0: break
    xWord = symmetry(xWord)
    if blocking + 2*block >= 0:
      xW = [i for i in xWord]
    else:
      xWord = [i for i in xW]
    block = 0
  pzl = translate(xW, pzl) #retain all the hashes from xW onto pzl
  return pzl

def translate(hashes, pzl):
  for i in range(HEIGHT):
    for j in range(WIDTH):
      if hashes[i][j] == '#' and pzl[i][j] != '#':
        add1(pzl, j, i, '#')
  return pzl

def main():
  start = time.process_time()
  #globals
  global HEIGHT, WIDTH, SIZE, BLOCKING, BLOCKINGARG, NONBLOCKING, DIR, POSITION, PZL, SYMBOLSET
  SYMBOLSET = '~`!@$%^&*()_+;:<>?,'
  HEIGHT = int(args[1][0:args[1].upper().find('X')])
  WIDTH = int(args[1][args[1].upper().find('X') + 1:])
  SIZE = HEIGHT * WIDTH
  BLOCKING = int(args[2])
  BLOCKINGARG = int(args[2])
  NONBLOCKING = SIZE - BLOCKING
  DIR = ""
  POSITION = {}
  for arg in args[3:]:
    arg = arg.upper()
    # if arg.endswith(".TXT"):
    #   continue
    DIR = arg[0].upper()
    endOfDimension = re.search(r'[VH]\d+X\d+', arg).end()
    POSITION[(DIR, int(arg[1:arg.find('X')]), int(arg[arg.find('X') + 1:endOfDimension]))] = arg[endOfDimension:] if arg[endOfDimension:] else '#'
  PZL = setUpPzl(['-'*WIDTH for i in range(HEIGHT)], POSITION)
  row, col = 0, 0
  for r in range(HEIGHT):
    for c in range(WIDTH):
      if (ch := PZL[r][c]) in ('-', '.') or ch.isalpha():
        row, col = r, c
        break
  PZL = cont(PZL, BLOCKINGARG - ''.join(PZL).count('#'), col, row)
  PZL = ''.join(PZL)

  #xWords
  if BLOCKINGARG == SIZE: return printpz('#'*SIZE)
  else:
    # xW = PZL[::-1] #symmetry first
    printpz(PZL)
    xW = bruteForce(PZL)
    printpz(xW)
    print(f"Time: {(time.process_time()-start):.4g}s")

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024
