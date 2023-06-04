import sys;args = sys.argv[1:]
import math;
import random
import re;
import time;

# args = 'GG100 V48,43,28,91,10,67,8,6R11B V68,11R21 V85,90,63,70,17,98,61,67,40,75,1R55BB V94R37 V62,27,66,34R32 V18,77R83'.split(' ')

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
  for slc in arrSlices:
    listOfSlicedIndices += stringSlc(slc, indices)
  print("listOfSlicedIndices", listOfSlicedIndices)
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
def policy_converter(listOfPaths):
  condense = set()
  if listOfPaths == []:
    return "*"
  for path in listOfPaths:
    condense.add((path[-1], path[-2]))
  directions = {gW: 'S', -gW: 'N', 1: 'E', -1:'W'}
  direction = ''
  for c in condense:
    diff = c[1]-c[0]
    direction+=directions[diff]
  return policy_key[''.join(sorted(direction))]


def djikstra(path, start, goal):
  global minPaths, gPaths
  if start in path:
    return
  path.append(start)
  if start == goal:
    if len(path) < minPaths:
      minPaths = len(path)
      gPaths = []
    if len(path) == minPaths:
      gPaths.append([i for i in path])
  else:
    row = start // gW
    col = start % gW
    if valid(row+1, col, (newInd:=(row+1)*gW+col), start):
      djikstra(path, newInd, goal)
    if valid(row-1, col, (newInd:=(row-1)*gW+col), start):
      djikstra(path, newInd, goal)
    if valid(row, col+1, (newInd:=row*gW+col+1), start):
      djikstra(path, newInd, goal)
    if valid(row, col-1, (newInd := row * gW + col -1), start):
      djikstra(path, newInd, goal)
  path.pop()


def solve(grid):
  global minPaths, gPaths
  policy = ''
  if not vRew:
    return '.'*size
  for ct, i in enumerate(grid):
    gPaths = list()
    minPaths = 1000
    for reward in vRew:
      djikstra([], reward, ct)
      # print(f"Reward {reward} start {ct} minPath {minPaths}")
      # for path in gPaths:
      #   print(path)
    if minPaths == 1:
      policy+= '*'
    else:
      policy+= policy_converter(gPaths)

  return policy

def main():
  # process args -------
  global indices, size, gW, gH, defRew, vRew, vBound, policy_key, dy, dx, minPaths, gPaths
  policy_key = {'ENW': '^', 'ENS': '>', 'NSW': '<', 'ESW':'v', 'ENSW': '+',
                'SW':'7', 'ES':'r','EN':'L','NW':'J','EW':'-','NS':'|', '*':'*',
                'N':'N', 'E':'E', 'S':'S', 'W':'W'}
  # policy_key = {{1,-2,2}: '^', {1,-1,2}: '>', {1,-1,-2}: '<', {-1,2,-2}:'v',
  #               {-1,-2}:'7', {-1,2}:'r', {1,2}:'L', {1,-2}:'J', {-2,2}:'-', {1,-1}:'|'}
  # policy_key = ['N','W','S','E']
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
  print(indices)
  for arg in args[1:]:
    if (result:=(re.search('^V.*?(R(\d*))?(B+)?$', arg))): #V vSlices (R[#]|B)
      print(result.groups())
      reward = int(result.group(2)) if result.group(2) else None
      B = True if result.group(3) else False
      indexOfReward = arg.find(f"R{reward}")
      arrSlices = arg[1:indexOfReward].split(',')
      if B: #BOUNDARY VERTICES --------------------
        #any intersecting edges get taken out!
        boundSet = findBoundarySet(arrSlices) #has repeating, should look like: {'1:3'} will give a boundary between this!
        for i in boundSet:
          if i in vBound:
            vBound = vBound - {i}
          else:
            vBound.add(i)
      else:
        for sle in arrSlices:
          slicesCover = stringSlc(sle, indices)
          for m in slicesCover:
            vRew[m] = reward if reward else defRew
    elif arg[0] == 'E':
      print("edges")
  print(f"Reward @ Vertices: {vRew}")
  print(f"Boundaries @ Vertices: {vBound}")
  grid = generate_grid()
  print_grid(grid)
  print(f"Policy: {solve(grid)}")

if __name__ == '__main__':
  main()

#as wide as it is tall
# Evelyn Li, pd 7, 2024