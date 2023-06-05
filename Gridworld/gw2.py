import sys;args = sys.argv[1:]
import math;
import random
import re;
import time;

args = 'G24W12 E1=13 E2=14 E3=15 E4=16 E5=17 E6=18 E7=19 E8=20 E9=21 E10=22 V21R50'.split(' ')

def buildGraph(size):
  max = int(size**0.5)
  width = 0
  difference = 100000
  for i in range(1, max+1):
    if size/i - int(size/i) == 0:
      if int(size/i) - size/int(size/i) < difference:
        width = int(size/i)
        difference = width - size/width
  height = int(size/width)
  return width, height
def generate_grid():
  #0 available
  grid = 'o'*size
  for i in vRew:
    grid = grid[:i] + 'R' + grid[i+1:]
  return grid
def print_grid(grid):
  for i in range(gH):
    print(grid[gW*i:gW*(i+1)])
def stringSlc(slice, arr):
  indicesOfColon = []
  for i in range(len(slice)):
    if slice[i] == ':':
      indicesOfColon.append(i)
  if len(indicesOfColon) == 0: #index
    return [arr[int(slice)]]
  elif len(indicesOfColon) == 1: #range
    start = int(slice[:indicesOfColon[0]]) if slice[:indicesOfColon[0]] else 0
    end = int(slice[indicesOfColon[0]+1:]) if slice[indicesOfColon[0]+1:] else None
    if end == None:
      return arr[start:]
    return arr[start:end] #when its empty no work cuz int(empty) no work!
  else: #steps
    start = int(slice[:indicesOfColon[0]]) if slice[:indicesOfColon[0]] else 0
    return arr[start::int(slice[indicesOfColon[1]+1:])]
def findBoundarySet(arrSlices):
  bndSet = list()
  listOfSlicedIndices = []
  # print(arrSlices)
  for slc in arrSlices:
    listOfSlicedIndices += stringSlc(slc, indices)
  # print("listOfSlicedIndices", listOfSlicedIndices)
  for i in listOfSlicedIndices:
    row = i // gW
    col = i % gW
    for ct in range(4):
      newR = row + dy[ct]
      newC = col + dx[ct]
      ind = newR * gW + newC
      if valid(newR, newC, ind, -1):
        if dy[ct]+dx[ct] > 0:
          bndSet.append(f"{i}:{ind}")
        else:
          bndSet.append(f"{ind}:{i}")
  return bndSet
def valid(newR, newC, newInd, ind):
  if 0 <= newR < gH and 0 <= newC < gW and 0 <= newInd < size:
    if ind == -1: return True
    stringSlice = f"{newInd}:{ind}" if newInd < ind else f"{ind}:{newInd}"
    if stringSlice not in vBound:
      return True
  return False
def policy_converter(listOfPaths, ct):
  condense = set()
  if listOfPaths == []:
    return "*"
  directions = {1: 'E', -1:'W', gW: 'S', -gW: 'N'}
  direction = ''
  for p in listOfPaths:
    diff = p-ct
    direction+=directions[diff]
  return policy_key[''.join(sorted(direction))]
def nbrs_helper(node, secondYet, second, visited):
  nbrs = list()
  row = node // gW
  col = node % gW
  for i in range(len(dy)):
    newR = row + dy[i]
    newC = col + dx[i]
    newInd = newR * gW + newC
    if valid(newR, newC, newInd, node) and (second, newInd) not in visited:
      if not secondYet: nbrs.append((newInd, newInd))
      else: nbrs.append((second, newInd))
  return nbrs

def bfs(start):
  current = [(start, start)] #(second, last)
  visited = set()
  next = []
  shortest = set()
  leng = 0
  if start in vRew: return None, 'RW'
  secondYet = False
  done = False
  while current:
    leng+=1
    next = []
    for tup in current:
      second, back = tup
      nbrs = nbrs_helper(back, secondYet, second, visited)
      next += nbrs
      secondYet = True
    visited.update(set(current))
    for ct, tup in enumerate(next):
      if tup[1] in vRew:
        done = True
        shortest.add(tup[0])
    if done: break
    current = [i for i in next]
  return shortest, leng

def solve(grid):
  global minPaths, gPaths
  policy = ''
  if not vRew:
    return '.'*size
  for ct, i in enumerate(grid):
    shortestPaths, minLength = bfs(ct)
    # print(shortestPaths)
    if minLength == 'RW':
      policy += '*'
    elif not shortestPaths:
      policy+= '.'
    else:
      policy+= policy_converter(shortestPaths, ct)
  return policy

def main():
  # process args -------
  global indices, size, gW, gH, defRew, vRew, vBound, policy_key, dy, dx, minPaths, gPaths
  policy_key = {'ENW': '^', 'ENS': '>', 'NSW': '<', 'ESW':'v', 'ENSW': '+',
                'SW':'7', 'ES':'r','EN':'L','NW':'J','EW':'-','NS':'|', '*':'*',
                'N':'N', 'E':'E', 'S':'S', 'W':'W'}
  dy = [0, 0, 1, -1]
  dx = [1, -1, 0, 0]
  vRew = dict()
  vBound = set()
  if (result := (re.search('^GG?(\d*)(W(\d*))?(R(\d*))?$', args[0]))): #to get size and allat
    size = int(result.group(1))
    widthOverride = int(result.group(3)) if result.group(3) else None
    gW, gH = buildGraph(size)
    if widthOverride:
      gW, gH = widthOverride, int(size / widthOverride)
    defRew = int(result.group(5)) if result.group(5) else None
  indices = [i for i in range(size)]
  # print(indices)
  for arg in args[1:]:
    if (result:=(re.search('^V.*?(R(\d*))?(B+)?$', arg))) : #V vSlices (R[#]|B)
      print(result.groups())
      reward = int(result.group(2)) if result.group(2) else ''
      B = True if result.group(3) else False
      indexOfReward = None
      if arg.find('R') != -1: indexOfReward = arg.find('R')
      elif (result.group(3)): indexOfReward = arg.find('B')
      setSlices = set(arg[1:indexOfReward].split(','))
      if B: #BOUNDARY VERTICES --------------------
        #any intersecting edges get taken out!
        boundSet = findBoundarySet(setSlices) #has repeating, should look like: {'1:3'} will give a boundary between this!
        for i in boundSet:
          if i in vBound:
            vBound = vBound - {i}
          else:
            vBound.add(i)
      if indexOfReward and arg.find('R') != -1:
        for sle in setSlices:
          slicesCover = stringSlc(sle, indices)
          for m in slicesCover:
            if defRew or reward: vRew[m] = reward if reward else defRew
    elif (result:=(re.search('^E([+~])(.*?)([=~])(.*?)(R(\d*))?$', arg))):
      print(result.groups())
      toggle = result.group(1)
      first = result.group(2)
      connector = result.group(3)
      second = result.group(4)
      reward = int(result.group(6)) if result.group(6) else ''
      indexOfReward = None
      if arg.find('R') != -1:
        indexOfReward = arg.find('R')

  print(f"Reward @ Vertices: {vRew}")
  print(f"Boundaries @ Vertices: {vBound}")
  grid = generate_grid()
  print_grid(grid)
  print(f"Policy: {solve(grid)}")

if __name__ == '__main__':
  main()

#as wide as it is tall
# Evelyn Li, pd 7, 2024