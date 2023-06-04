import sys;args = sys.argv[1:]
import math;
import random
import re;
import time;

args = ['G12', 'V8R35']

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
  print(arrSlices)
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
      if valid(newR, newC, ind):
        if dy[ct]+dx[ct] > 0:
          bndSet.append(f"{i}:{ind}")
        else:
          bndSet.append(f"{ind}:{i}")
  return bndSet
def valid(row, col, ind):
  if 0 <= row < gH and 0 <= col < gW and 0 <= ind < size:
    return True
  return False
def policy_converter(path):
  startInd = path[0]
  nextInd = path[1]
  diff = nextInd - startInd
  if diff == 1:
    return 'E'
  if diff == -1:
    return 'W'
  if diff == gW:
    return 'S'
  if diff == -gW:
    return 'N'

def bfs(start, goal, distances):
  path = [goal]
  while True:
    potentialDist = []
    potential = []
    for i in range(len(dy)):
      current = path[-1]
      row = current // gW
      col = current % gW
      newR = row + dy[i]
      newC = col + dx[i]
      newInd = newR*gW+newC
      if valid(newR, newC, newInd):
        potential.append(newInd)
        potentialDist.append(distances[newInd])
    minVal = 1000
    minInd = 1000
    for ct, n in enumerate(potentialDist):
      if n < minVal:
        minVal = n
        minInd = ct
    leastDistInd = minInd
    path.append(potential[leastDistInd])
    if path[-1] == start:
      break
  return list(reversed(path))


def djikstra(grid, goal, start):
  if goal == start:
    return [1]
  seen = [False for i in range(size)]
  distances = [math.inf for i in range(size)]
  distances[start] = 0
  current = start
  row = current // gW
  col = current % gW
  while True:
    for i in range(len(dy)):
      newR = row + dy[i]
      newC = col + dx[i]
      potential = newR*gW+newC
      if valid(newR, newC, potential):
        if not seen[potential]: #add bound somewhere here
          distance = distances[current]+1#add the boundary heuristic sometime later here
          if distance < distances[potential]:
            distances[potential] = distance
    seen[current] = True
    #choosing next vertex
    next = [d for d in distances]
    for ct, s in enumerate(seen):
      if s == True:
        next[ct] = math.inf
    minVal = 1000
    minInd = 1000
    for ct, n in enumerate(next):
      if n < minVal:
        minVal = n
        minInd = ct
    current = minInd
    row = current // gW
    col = current % gW
    if current == goal:
      break
  print('DJIKSTRA---------')
  print(f"start: {start} and goal: {goal}")
  print(distances)
  return bfs(start, goal, distances)



def solve(grid):
  policy = ''
  for ct, i in enumerate(grid):
    minPathLen = 10000
    minPath = ''
    for reward in vRew:
      shortest_path = djikstra(grid, reward, ct)
      print(f"Path {shortest_path}")
      if len(shortest_path) == 1:
        policy+='*'
        continue
      path_policy = policy_converter(shortest_path)
      if minPathLen > len(shortest_path):
        minPathLen = len(shortest_path)
        minPath = path_policy
    policy += minPath
    print(policy)
  return policy

def main():
  # process args -------
  global indices, size, gW, gH, defRew, vRew, vBound, policy_key, dy, dx
  policy_key = {'ENW': '^', 'ENS': '>', 'NSW': '<', 'ESW':'v',
                'SW':'7', 'ES':'r','EN':'L','NW':'J','EW':'-','NS':'|', '*':'*'}
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
    if (result:=(re.search('^V.*?(R(\d*))?(B)?$', arg))): #V vSlices (R[#]|B)
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