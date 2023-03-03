import sys;args = sys.argv[1:]
import re
import random
import time

args = '15x15 39 H0x0Mute V0x0mule V10x13Erica H7x5# V3x4# H6x7# V11x3#'.split(' ')
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
      if ch == '#' and not pzl[i][j].isalpha():
        add(pzl, j, i, '#')
      if ch.isalpha() and pzl[i][j] == '.':
        add(pzl, j, i, '-')
  return pzl

def symmetryOne(pzl, col, row):
  #len()-1-index
  newC = WIDTH-1-col
  newR = HEIGHT-1-row
  add(pzl, newC, newR, '#')
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

def update(pzl, possible, x, y):
  points = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
  for i in points:
    p = pzl[i[1]][i[0]]
    if p in ('.', '-') or p.isalpha():
      possible.add(i)
  return possible

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

def check2(pzl):
  symCount = []
  for i in pzl:
    for j in i:
      if j not in symCount and j != '#': symCount.append(j)
      if len(symCount) > 2: return False
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
  # return pzl

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

def threeHV(pzl):
  # possible = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if pzl[y][x] in ('.', '-') or pzl[y][x].isalpha()}
  for row, str in enumerate(pzl):
    for col, ch in enumerate(str):
      # row, col = (p:=possible.pop())[1], p[0] #(y, x)
      # if pzl[row][col] == '#': continue
      if ch == '#': continue
      l = left(pzl, col, row)
      r = right(pzl, col, row)
      u = up(pzl, col, row)
      d = down(pzl, col, row)
      # print(row, col, l, r, u, d)
      if (v:=u+d) < 2:
        return False
      if (h:=l+r) < 2:
        return False
      # pzl = symmetry(pzl)
  return True

def contig(pzl, c, r):
  xW = [i for i in pzl]
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
  if len(innerSet)>1: return False
  return True

def isInvalid(pzl, blocking):
  if not threeHV(pzl):
    return True
  row, col = 0, 0
  for r in range(HEIGHT):
    for c in range(WIDTH):
      if (ch := pzl[r][c]) == '#': continue
      row, col = r, c
      break
  if not contig(pzl, col, row):
    return True
  return False

#generates valid xWord boards, go through and check if valid
def bruteForce(pzl, blocking):
  # possible = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if pzl[y][x] == "."} #make faster through this
  blocks = BLOCKINGARG-''.join(pzl).count('#')
  if blocks < 0: return False
  # printpz(pzl)
  if blocks == 0:
    if isInvalid(pzl, blocking): return False
    return pzl
  # for p in possible:
  for row, str in enumerate(pzl):
    for col, ch in enumerate(str):
      # col, row = p[0],p[1]
      if ch == '.':
        newPzl = add([i for i in pzl], col, row, '#')
        newPzl = symmetryOne(newPzl, col, row) #change to better function
        if newPzl:
          bF = bruteForce(newPzl, blocks)
          if bF:
            return bF
  return False

def main():
  start = time.process_time()
  #globals
  global HEIGHT, WIDTH, SIZE, BLOCKING, BLOCKINGARG, DIR, POSITION, PZL, SYMBOLSET
  SYMBOLSET = '~`!@$%^&*()_+;:<>?,'
  HEIGHT = int(args[1][0:args[1].upper().find('X')])
  WIDTH = int(args[1][args[1].upper().find('X') + 1:])
  SIZE = HEIGHT * WIDTH
  BLOCKING = int(args[2])
  BLOCKINGARG = int(args[2])
  DIR = ""
  POSITION = {}
  for arg in args[3:]:
    arg = arg.upper()
    # if arg.endswith(".TXT"):
    #   continue
    DIR = arg[0].upper()
    endOfDimension = re.search(r'[VH]\d+X\d+', arg).end()
    POSITION[(DIR, int(arg[1:arg.find('X')]), int(arg[arg.find('X') + 1:endOfDimension]))] = arg[endOfDimension:] if arg[endOfDimension:] else '#'
  PZL = ['.' * WIDTH for i in range(HEIGHT)]
  # might ne a futrue problem im ngl
  if HEIGHT % 2 + WIDTH % 2 + BLOCKING % 2 == 3:
    # print('SCRUMPDIDLY')
    if PZL[HEIGHT // 2][WIDTH // 2] == '#':
      BLOCKING += 1
    else:
      BLOCKING -= 1
      add(PZL, WIDTH // 2, HEIGHT // 2, '#')
  elif HEIGHT % 2 + WIDTH % 2 == 2:
    # print('SCRUMPDIDLYDOOOOO')
    add(PZL, WIDTH // 2, HEIGHT // 2, '-')
  for coord in POSITION:
    direction = coord[0]
    row = coord[1]
    col = coord[2]
    content = POSITION[coord]
    if direction == 'V':
      for i in content:
        if i == '#': BLOCKING -= 2
        if col + 1 != WIDTH: PZL[row] = PZL[row][0:col] + i + PZL[row][col + 1:]
        else: PZL[row] = PZL[row][0:col] + i
        row += 1
    else:  # DIR = 'H
      BLOCKING -= (c := content.count('#')) * 2
      PZL[row] = PZL[row][0:col] + content + PZL[row][col + len(content):]

  #xWords
  if BLOCKINGARG == SIZE: return printpz(['#'*WIDTH for i in range(HEIGHT)])
  else:
    xW = symmetry(PZL)
    printpz(xW)
    xW = generate(xW, BLOCKING) #get all the for certain ones
    printpz(xW)
    row, col = 0, 0
    for r in range(len(xW)):
      for c in range(len(xW[r])):
        if (ch:=xW[r][c]) in ('-', '.') or ch.isalpha():
          row, col = r, c
          break
    xW = contiguous(xW, BLOCKINGARG-''.join(xW).count('#'), col, row)
    printpz(xW)
    #brute force
    # possible = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if xW[y][x] == "."}  # make faster through this
    xW = bruteForce(xW, BLOCKINGARG-''.join(xW).count('#'))
    #take this out for final:
    for i in range(len(xW)):
      xW[i] = xW[i].replace('.','-')
    printpz(xW)
    print(f"Time: {(time.process_time()-start):.4g}s")

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024


