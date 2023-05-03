import sys; args = sys.argv[1:]
import math, random

#just connect randomly
def classical(numEdges, numNodes):
  currentEdges = numEdges
  for edge in range(numEdges):
    nodes1 = random.randint(0, numNodes)
    nodes2 = random.randint(0, numNodes)

  return 0

def inc(numEdges, numNodes):

  return 0

def printit(dct):
  for i in dct:
    print(i, end=':')
    print(dct[i])

def main():
  global numEdges, type, numNodes, dS, weights
  dS = {i:set() for i in range(numNodes)}
  numNodes = int(args[2])
  numEdges = args[0]*numNodes
  type = args[1][0].upper()
  if type == 'C':
    printit(classical(numEdges, numNodes))
  printit(inc(numEdges, numNodes))

if __name__ == "__main__": main()

#For each degree, d, in the resultant graph, the code should output d:# of nodes of degree d.

#Evelyn Li, pd 7, 2024