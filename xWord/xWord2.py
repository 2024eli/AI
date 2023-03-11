import sys;args = sys.argv[1:]
import re
import random
import time

# args = 'someDct.txt 13x13 32 H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5stirrup H4x2##Ordained V0x1Proc V0x12Mah V5x0zoo'.split(' ')
if not args[0].upper().endswith('.TXT'):
  args = [0] + args

def printpz(solved):
  for i in solved:
    for j in i:
      print(j+' ', end='')
    print()
  print()

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
        add(pzl, j, i, '#')
      if 65 <= ord(ch) <= 90 and pzl[i][j] == '.':
        add(pzl, j, i, '-')
  return pzl

def add(pzl, x, y, ch):
  pzl[y] = pzl[y][0:x] + ch + pzl[y][x+1:]
  return pzl

def up(pzl, col, row):
  up = 0
  if row == 0:
    return 0
  for u in range(1, row+1):
    if (p:=pzl[row-u][col])=='#':break
    if p in ('.', '-') or p.isalpha(): up+=1
  return up

def down(pzl, col, row):
  down = 0
  if row == HEIGHT-1:
    return 0
  for d in range(1, HEIGHT-row):
    if (p:=pzl[row+d][col])=='#':break
    if p in ('.', '-') or p.isalpha(): down+=1
  return down

def right(pzl, col, row):
  right = 0
  if col == WIDTH-1:
    return 0
  for r in range(1, WIDTH-col):
    if (p:=pzl[row][col+r])=='#':break
    if p in ('.', '-') or p.isalpha(): right+=1
  return right

def left(pzl, col, row):
  left = 0
  if col == 0:
    return 0
  for l in range(1, col+1):
    if (p:=pzl[row][col-l])=='#':break
    if p in ('.','-') or p.isalpha(): left+=1
  return left

#for every spot, look and see if it can be in a 3h and a 3v
def generate(pzl, blocks):
  possible = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if pzl[y][x] == "."}
  blocking = 0
  while possible:
    row, col = (p:=possible.pop())[1], p[0] #(y, x)
    if pzl[row][col] == '#': continue
    l = left(pzl, col, row)
    r = right(pzl, col, row)
    u = up(pzl, col, row)
    d = down(pzl, col, row)
    # print(row, col, l, r, u, d)
    if (v:=u+d) < 2:
      for i in range(u+1):
        if pzl[row-i][col] != '#':
          add(pzl, col, row-i, '#')
          blocking -= 1
      for i in range(d+1):
        if pzl[row+i][col] != '#':
          add(pzl, col, row+i, '#')
          blocking -= 1
    if (h:=l+r) < 2:
      for i in range(l + 1):
        if pzl[row][col-i] != '#':
          add(pzl, col-i, row, '#')
          blocking -= 1
      for i in range(r + 1):
        if pzl[row][col+i] != '#':
          add(pzl, col+i, row, '#')
          blocking -= 1
    pzl = symmetry(pzl)
  return pzl

def check1(pzl, ch):
  for i in range(len(pzl)):
    for j in range(len(pzl[i])):
      if (p:=pzl[i][j]) == '.':
        return (j, i)
  return True

def translate(hashes, pzl):
  for i in range(HEIGHT):
    for j in range(WIDTH):
      if hashes[i][j] == '#' and pzl[i][j] != '#':
        add(pzl, j, i, '#')
  return pzl

def contiguousHelper(pzl, c, r, ch, symbolsUsed):
  if 0 <= r < HEIGHT and 0 <= c < WIDTH and ((p:=pzl[r][c]) in ('-','.') or p in symbolsUsed or p.isalpha()):
    add(pzl, c, r, ch) #PATH
    contiguousHelper(pzl, c, r+1, ch, symbolsUsed)
    contiguousHelper(pzl, c, r-1, ch, symbolsUsed)
    contiguousHelper(pzl, c+1, r, ch, symbolsUsed)
    contiguousHelper(pzl, c-1, r, ch, symbolsUsed)
  return pzl

def contiguous(pzl, blocking, c, r):
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
            add(xWord, ch, i, '#')
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

def coord(pzl):
  row, col = 0, 0
  for r in range(HEIGHT):
    for c in range(WIDTH):
      if (ch := pzl[r][c]) in ('-', '.') or ch.isalpha():
        row, col = r, c
        break
  return col, row

def printpzString(pzl):
  if pzl == False:
    print('False')
    return False
  for ct, it in enumerate(pzl):
    print(it, end=' ')
    if (ct+1) % WIDTH == 0:
      print()
  print()

def cont(pzl, index):
  if pzl[index] != '-' and not pzl[index].isalpha(): return pzl
  col, row = index % WIDTH, index // WIDTH
  pzl = pzl[:index] + '$' + pzl[index+1:]
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
  pzl = pzl[:ind] + '#' + pzl[ind+1:]
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
  if '-' in cont(pzl, pzl.find('-')): return False
  if (bl:=pzl.count('#')) == BLOCKINGARG: return pzl
  elif bl > BLOCKINGARG: return False
  # printpzString(pzl)
  for i in {j for j, c in enumerate(pzl) if c == '-'}:
    newPzl = put(pzl, i)
    if newPzl:
      bF = bruteForce(newPzl)
      if bF:
        return bF
  return False

# ------------------ XWORD 2 METHODS ------------------------------------ #


def main():
  start = time.process_time()
  #globals
  global HEIGHT, WIDTH, SIZE, BLOCKING, BLOCKINGARG, NONBLOCKING, DIR, POSITION, PZL, SYMBOLSET, WORDS
  SYMBOLSET = '~`!@$%^&*()_+;:<>?,'
  WORDS = list()
  HEIGHT = int(args[1][0:args[1].upper().find('X')])
  WIDTH = int(args[1][args[1].upper().find('X') + 1:])
  SIZE = HEIGHT * WIDTH
  file = args[0]
  BLOCKING = int(args[2])
  BLOCKINGARG = int(args[2])
  NONBLOCKING = SIZE - BLOCKING
  DIR = ""
  POSITION = {}
  for arg in args[3:]:
    arg = arg.upper()
    DIR = arg[0].upper()
    endOfDimension = re.search(r'[VH]\d+X\d+', arg).end()
    POSITION[(DIR, int(arg[1:arg.find('X')]), int(arg[arg.find('X') + 1:endOfDimension]))] = arg[endOfDimension:] if arg[endOfDimension:] else '#'
  PZL = ['.' * WIDTH for i in range(HEIGHT)]
  if HEIGHT % 2 + WIDTH % 2 + BLOCKING %2 == 3:
    add(PZL, WIDTH//2, HEIGHT//2, '#')
  elif HEIGHT % 2 + WIDTH % 2 == 2:
    add(PZL, WIDTH // 2, HEIGHT // 2, '-')
  for coord in POSITION:
    direction = coord[0]
    row = coord[1]
    col = coord[2]
    content = POSITION[coord]
    if direction == 'V':
      for i in content:
        if i == '#': BLOCKING -= 2
        else: NONBLOCKING -= 1
        if col + 1 != WIDTH: PZL[row] = PZL[row][0:col] + i + PZL[row][col + 1:]
        else: PZL[row] = PZL[row][0:col] + i
        row += 1
    else:  # DIR = 'H
      BLOCKING -= (c := content.count('#')) * 2
      NONBLOCKING = NONBLOCKING - len(content) + c
      PZL[row] = PZL[row][0:col] + content + PZL[row][col + len(content):]
    with open(args[0]) as f:
      for line in f:
        word = line.strip()
        if len(word) < 3: continue
        WORDS.append(word)

  #xWords
  if BLOCKINGARG == SIZE: return printpz(['#'*WIDTH for i in range(HEIGHT)])
  else:
    xW = symmetry(PZL)
    xW = generate(xW, BLOCKING) #get all the for certain ones
    row, col = 0, 0
    for r in range(len(xW)):
      for c in range(len(xW[r])):
        if (ch:=xW[r][c]) in ('-', '.') or ch.isalpha():
          row, col = r, c
          break
    xW = contiguous(xW, BLOCKINGARG-''.join(xW).count('#'), col, row)

    #brute force
    xW = ''.join(xW)
    xW = xW.replace('.', '-')
    xW = bruteForce(xW)
    printpzString(xW)
    print(f"Time: {(time.process_time() - start):.4g}s")

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024
