import sys;args = sys.argv[1:]
import re
import random
import time

# args = 'someDct.txt 13x13 32 H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5stirrup H4x2##Ordained V0x1Proc V0x12Mah V5x0zoo'.split(' ')
if not args[0].upper().endswith('.TXT'):
  args = [0] + args

global HEIGHT, WIDTH, SIZE, BLOCKING, NONBLOCKING, DIR, POSITION, PZL
HEIGHT = int(args[1][0:args[1].upper().find('X')])
WIDTH = int(args[1][args[1].upper().find('X')+1:])
SIZE = HEIGHT*WIDTH
BLOCKING = int(args[2])
NONBLOCKING = SIZE-BLOCKING
DIR = ""
POSITION = {}
for arg in args[3:]:
  arg = arg.upper()
  # if arg.endswith(".TXT"):
  #   continue
  DIR = arg[0].upper()
  endOfDimension = re.search(r'[VH]\d+X\d+', arg).end()
  POSITION[(DIR, int(arg[1:arg.find('X')]), int(arg[arg.find('X')+1:endOfDimension]))] = arg[endOfDimension:] if arg[endOfDimension:] else '#'
PZL = ['.'*WIDTH for i in range(HEIGHT)]
for coord in POSITION:
  direction = coord[0]
  row = coord[1]
  col = coord[2]
  content = POSITION[coord]
  if direction == 'V':
    for i in content:
      if i == '#':
        BLOCKING -= 2
      else: NONBLOCKING -= 1
      if col+1 != WIDTH:
        PZL[row] = PZL[row][0:col] + i + PZL[row][col+1:]
      else: PZL[row] = PZL[row][0:col] + i
      row += 1
  else: #DIR = 'H
    #okay, idk what about if the horizontal goes over to the next row, will that happen.
    BLOCKING -= (c:=content.count('#'))*2
    NONBLOCKING = NONBLOCKING - len(content)+c
    PZL[row] = PZL[row][0:col] + content + PZL[row][col+len(content):]

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
      if ch == '#' and pzl[i][j] == '.':
        pzl = add(pzl, j, i, '#')
      if 65 <= ord(ch) <= 90 and pzl[i][j] == '.':
        pzl = add(pzl, j, i, '-')
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
def isInvalid(pzl):
  possible = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if pzl[y][x] == "."}
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
        pzl = add(pzl, col, row-i, '#')
        possible = update(pzl, possible, col, row-i)
      for i in range(d+1):
        pzl = add(pzl, col, row+i, '#')
        possible = update(pzl, possible, col, row+i)
      printpz(pzl)
    if (h:=l+r) < 2:
      for i in range(l + 1):
        pzl = add(pzl, col-i, row, '#')
        possible = update(pzl, possible, col-i, row)
      for i in range(r + 1):
        pzl = add(pzl, col+i, row, '#')
        possible = update(pzl, possible, col+i, row)
    pzl = symmetry(pzl)
  return pzl

#generates valid xWord boards
'''go through (. idk, - letters, # has to be blocking where 3h 3v doesnt work) 
and see if it can be a horitzontal and vertical word
how to find more blocking: 
- '''
def bruteForce(pzl, blocking):
  size = SIZE
  # for row in pzl:
  #   for ch in row:
  return pzl

def main():
  xW = symmetry(PZL)
  printpz(xW)
  xW = isInvalid(PZL) #get all the for certain ones
  xW = bruteForce(xW, BLOCKING)
  #take this out for final:
  for i in range(len(xW)):
    xW[i] = xW[i].replace('.','-')
  printpz(xW)

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024


