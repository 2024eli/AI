import sys;args = sys.argv[1:]
import math;
import random
import re;
import time;

args = 'GG22R8 E+15,12,10,4=16,13,9,5R57 V13,18,0,16R57B V0,2R26B V6,20,0R91B'.split(' ')

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
      if valid1(newR, newC, ind):
        if dy[ct]+dx[ct] > 0:
          bndSet.append(f"{i}:{ind}")
        else:
          bndSet.append(f"{ind}:{i}")
  return bndSet
def isValid_edge(index, direc):
  direction = {'N': -gW, 'S': gW, 'E': 1, 'W': -1}
  next = index+direction[direc]
  if direc == 'E' or direc == 'W':
    if next//gW != index//gW: return False
  if direc == 'S' or direc == 'N':
    if next%gW != index%gW: return False
  return valid1(next//gW, next%gW, next)
def process_edge_directive1(toggle, first, connector, second, reward): #list of (toggle, first, connector, second, reward)
  global edges_ds #{(e1, e2, e3)
  edges = []
  #process splices
  s1 = stringSlc(first, indices)
  s2 = stringSlc(second, indices)
  edges = list(zip(s1, s2))
  if connector == '=':
    edges += list(zip(s2, s1))
  # toggles -----------
  if toggle == '+':
    for e in edges:
      if e not in edges_ds:
        edges_ds[e] = reward
  elif toggle == '~':
    for e in edges:
      if e in edges_ds:
        del edges_ds[e]
  elif toggle == '+~':
    for e in edges:
      if e in edges_ds:
        edges_ds[e] = reward
  else: #actually toggle
    for e in edges:
      if e in edges_ds:
        del edges_ds[e]
      else:
        edges_ds[e] = reward
  #return list of (second, reward)
def process_edge_directive2(toggle, slice, direc, connector, reward): #list of (toggle, first, connector, second, reward)
  global edges_ds
  direction = {'N': -gW, 'S': gW, 'E': 1, 'W': -1}
  s1 = stringSlc(slice, indices)
  edges = []
  for s in s1:
    if isValid_edge(s, direc):
      edges.append((s, s+direction[direc]))
      if connector=='=':
        edges.append((s+direction[direc], s))
  # toggles -----------
  if toggle == '+':
    for e in edges:
      if e not in edges_ds:
        edges_ds[e] = reward
  elif toggle == '~':
    for e in edges:
      if e in edges_ds:
        del edges_ds[e]
  elif toggle == '+~':
    for e in edges:
      if e in edges_ds:
        edges_ds[e] = reward
  else:  # actually toggle
    for e in edges:
      if e in edges_ds:
        del edges_ds[e]
      else:
        edges_ds[e] = reward

def valid(newR, newC, newInd, ind):
  if 0 <= newR < gH and 0 <= newC < gW and 0 <= newInd < size:
    if ind == -1: return True
    if (ind, newInd) not in edges_ds:
      return False
    return True
  return False
def valid1(newR, newC, newInd):
  if 0 <= newR < gH and 0 <= newC < gW and 0 <= newInd < size:
    return True
  return False
def policy_converter(listOfPaths, ct):
  global jumps, wanted_jumps
  condense = set()
  if listOfPaths == []:
    return "*"
  directions = {1: 'E', -1:'W', gW: 'S', -gW: 'N'}
  direction = ''
  for p in listOfPaths:
    diff = p-ct
    if diff not in directions:
      wanted_jumps.add(f"{ct}>{jumps[ct]}")
    else: direction+=directions[diff]
  return policy_key[''.join(sorted(direction))] if direction else '.'

def nbrs_helper(node, secondYet, second, visited):
  global jumps, edges_ds
  direction = {-gW, gW, 1, -1}
  nbrs = list()
  row = node // gW
  col = node % gW
  for tup in edges_ds:
    if tup[0] == node and (second, tup[0]) not in visited:
      if (diff:=tup[1]-tup[0]) not in direction:
        jumps[tup[0]] = tup[1]
      if not secondYet: nbrs.append((tup[1], tup[1], edges_ds[tup]))
      else: nbrs.append((second, tup[1], edges_ds[tup]))
  return nbrs

def nextTo(node):
  nbrs = list()
  row = node // gW
  col = node % gW
  for i in range(len(dy)):
    newR = row + dy[i]
    newC = col + dx[i]
    newInd = newR * gW + newC
    if valid1(newR, newC, newInd):
      nbrs.append(newInd)
  return nbrs

def bfs(start):
  current = [(start, start, None)] #(second, last)
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
      second, back, reward = tup
      nbrs = nbrs_helper(back, secondYet, second, visited)
      next += nbrs
      secondYet = True
    visited.update({(t[0], t[1]) for t in current})
    for ct, tup in enumerate(next):
      if tup[2]:
        done = True
        shortest.add(tup[0])
      elif tup[1] in vRew:
        done = True
        shortest.add(tup[0])
    if done: break
    current = [i for i in next]
  return shortest, leng

def solve(grid):
  global wanted_jumps
  policy = ''
  if not vRew and not edges_ds:
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
  for jump in wanted_jumps:
    policy += jump + ';'
  return policy

def main():
  # process args -------
  global indices, size, jumps, gW, gH, defRew, vRew, vBound, policy_key, dy, dx, edges_ds, wanted_jumps
  policy_key = {'ENW': '^', 'ENS': '>', 'NSW': '<', 'ESW':'v', 'ENSW': '+',
                'SW':'7', 'ES':'r','EN':'L','NW':'J','EW':'-','NS':'|', '*':'*',
                'N':'N', 'E':'E', 'S':'S', 'W':'W'}
  dy = [0, 0, 1, -1]
  dx = [1, -1, 0, 0]
  wanted_jumps = set()
  vRew = dict()
  vBound = set()
  jumps = dict()
  if (result := (re.search('^GG?(\d*)(W(\d*))?(R(\d*))?$', args[0]))): #to get size and allat
    size = int(result.group(1))
    widthOverride = int(result.group(3)) if result.group(3) else None
    gW, gH = buildGraph(size)
    if widthOverride:
      gW, gH = widthOverride, int(size / widthOverride)
    defRew = int(result.group(5)) if result.group(5) else None
  indices = [i for i in range(size)]
  edges_ds = dict()
  for node in range(size):
    nb = nextTo(node)
    for n in nb:
      edges_ds[(node, n)] = None
  for arg in args[1:]:
    if (result:=(re.search('^V.*?(R(\d*))?(B+)?$', arg))) : #V vSlices (R[#]|B)
      # print(result.groups())
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
  for v in vBound:
    vv = (int(v.split(':')[0]), int(v.split(':')[1]))
    if vv in edges_ds:
      del edges_ds[vv]
    if (vv[1], vv[0]) in edges_ds:
      del edges_ds[(vv[1], vv[0])]
  for arg in args[1:]:
    if (result:=(re.search('^E(\+~|\+|~)?([0-9,:]+?)([=~])(.+?)(R(\d*))?$', arg))):
      print(result.groups())
      toggle = result.group(1)
      firsts = result.group(2).split(',')
      connector = result.group(3)
      seconds = result.group(4).split(',')
      reward = None
      if arg.find('R') != -1:
        reward = int(result.group(6)) if result.group(6) else defRew
      # print((toggle, firsts, connector, seconds, reward))
      for s in range(len(firsts)):
        process_edge_directive1(toggle, firsts[s], connector, seconds[s], reward)
    elif (result:=(re.search('^E(\+~|\+|~)?(.*?)([NSWE])([=~])(R(\d*))?$', arg))):
      print(result.groups())
      toggle = result.group(1)
      slices = result.group(2).split(',')
      direc = result.group(3)
      connector = result.group(4)
      reward = None
      if arg.find('R') != -1:
        reward = int(result.group(6)) if result.group(6) else defRew
      for slice in slices:
        process_edge_directive2(toggle, slice, direc, connector, reward)
  # print(f"Reward @ Vertices: {vRew}")
  print(f"Boundaries @ Vertices: {vBound}")
  print(f"Edges Directive: {edges_ds}")
  grid = generate_grid()
  print_grid(grid)
  print(f"Policy: {solve(grid)}")

if __name__ == '__main__':
  main()

#as wide as it is tall
# Evelyn Li, pd 7, 2024