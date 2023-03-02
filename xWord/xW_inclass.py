import sys;

args = sys.argv[1:]
import re
import random
import time

# args = 'someDct.txt 13x13 32 H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5stirrup H4x2##Ordained V0x1Proc V0x12Mah V5x0zoo'.split(' ')
args = [0] + args

global HEIGHT, WIDTH, SIZE, BLOCKING, NONBLOCKING, DIR, POSITION, PZL
HEIGHT = int(args[1][0:args[1].upper().find('X')])
WIDTH = int(args[1][args[1].upper().find('X') + 1:])
SIZE = HEIGHT * WIDTH
NONBLOCKING = SIZE
BLOCKING = 0
DIR = ""
POSITION = {}
for arg in args[2:]:
  arg = arg.upper()
  if arg.find('X') == -1:
    BLOCKING = int(arg)
    NONBLOCKING = SIZE - BLOCKING
  # if arg.endswith(".TXT"):
  #   continue
  DIR = arg[0].upper()
  endOfDimension = re.search(r'[VH]\d+X\d+', arg).end()
  POSITION[(DIR, int(arg[1:arg.find('X')]), int(arg[arg.find('X') + 1:endOfDimension]))] = arg[endOfDimension:] if arg[
                                                                                                                   endOfDimension:] else '#'
PZL = ['-' * WIDTH for i in range(HEIGHT)]
for coord in POSITION:
  direction = coord[0]
  row = coord[1]
  col = coord[2]
  content = POSITION[coord]
  if direction == 'V':
    for i in content:
      if i == '#':
        BLOCKING -= 2
      else:
        NONBLOCKING -= 1
      if col + 1 != WIDTH:
        PZL[row] = PZL[row][0:col] + i + PZL[row][col + 1:]
      else:
        PZL[row] = PZL[row][0:col] + i
      row += 1
  else:  # DIR = 'H
    # okay, idk what about if the horizontal goes over to the next row, will that happen?
    BLOCKING -= (c := content.count('#')) * 2
    NONBLOCKING = NONBLOCKING - len(content) + c
    PZL[row] = PZL[row][0:col] + content + PZL[row][col + len(content):]


def printpz(solved):
  for i in solved:
    for j in i:
      print(j + " ", end="")
    print()


# takes all blocking and does symmetry on them
def symmetry(pzl):
  # transform 180
  pzlFlip = pzl[::-1]
  flip = []
  for i in range(len(pzlFlip)):
    flip.append(pzlFlip[i][::-1])
  for i, f in enumerate(flip):
    p = pzl[i]
    for j, ch in enumerate(f):
      if ch == '#' and p[j] == '-':
        pzl[i] = p[0:j] + '#' + p[j + 1:]
  return pzl


def add(pzl, x, y, ch):
  if pzl == -1:
    return -1
  if pzl[y][x] == ch:
    return pzl
  if pzl[y][x] == '#':
    return -1
  pzl[y] = pzl[y][0:x] + ch + pzl[y][x:]
  return pzl


# contiguous
def contiguous(pzl, x, y):
  if 0 <= x + y * WIDTH < SIZE and pzl[y][x] == '-':
    pzl = add(pzl, x, y, 'B')
    pzl = contiguous(pzl, x, y + 1)
    pzl = contiguous(pzl, x, y - 1)
    if (x + 1) % WIDTH:
      pzl = contiguous(pzl, x + 1, y)
    if (x + 1) % WIDTH != WIDTH - 1:
      pzl = contiguous(pzl, x - 1, y)
  return pzl

pzl = symmetry(PZL)
printpz(pzl)


'''
10x9 V0x0A
10x10 V0x1B V2x4C
9x10 V1x1D
11x11 V5x5E
9x9 V4x4#
9x9 V2x4#
11x13 V5x6#
'''

'''
9x9 16 V2X4# V3X3# V5X1#
4x4

'''


# Evelyn Li, pd 7, 2024


