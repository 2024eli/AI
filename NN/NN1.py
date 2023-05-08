import sys;args = sys.argv[1:]
import math;
import random
import time;

def dotProduct(v1, v2): return sum(hadamardProduct(v1, v2))

def hadamardProduct(v1, v2):
  return [v1[i] * v2[i] for i in range(len(v1))]

#all the functions ------
def t1(input): #identity
  return input

def t2(input): #ramp
  if input > 0: return input
  return 0

def t3(input): #log
  return 1/(1+math.exp(-input))

def t4(input): #2*log
  return 2*t3(input)-1

def transfer(input):
  if funcName == 'T1': return t1(input)
  if funcName == 'T2': return t2(input)
  if funcName == 'T3': return t3(input)
  if funcName == 'T4': return t4(input)

#main
def nextNodes(input, layer):
  #find next num of nodes
  next = []
  for i in range(len(layer)//len(input)):
    next += [layer[i*len(input):(i+1)*len(input)]]
  nextVal = []
  for i in next:
    nextVal.append(transfer(dotProduct(input, i)))
  return nextVal

def feedforward(inputs, weights):
  nodes = []
  inp = inputs
  for layer in weights[:-1]:
    nodes.append(inp)
    inp = nextNodes(inp, layer)
  final = weights[-1]
  finalOut = [inp[i]*final[i] for i in range(len(inp))]
  nodes.append(finalOut)
  print(inp)
  #only want to return outputs
  print("whole list of nodes: ", end='')
  print(nodes)
  return finalOut

def main():
  global weights, funcName, inputs, nodes # weights list of list
  with open(args[0]) as f:
    weights = [[float(i) for i in line.split(' ')] for line in f]
  funcName = args[1]
  inputs = [float(i) for i in args[2:]]
  finalOuts = feedforward(inputs, weights)
  print()
  print(finalOuts)
  print()
  for i in finalOuts:
    print(str(i), end=' ')

if __name__ == '__main__':
  main()

#make a list of list of nodes
# Evelyn Li, pd 7, 2024