import sys;args = sys.argv[1:]
import math;
import random
import time;

args = ['nn2test.txt']

def dotProduct(v1, v2): return sum(hadamardProduct(v1, v2))
def hadamardProduct(v1, v2): return [v1[i] * v2[i] for i in range(len(v1))]
def tranFunc(input): return 1/(1+math.exp(-input)) #log
def nextNodes(inputs, layer):
  #find next num of nodes
  next = []
  for i in range(len(layer)//len(inputs)):
    next += [layer[i*len(inputs):(i+1)*len(inputs)]] #weights used
  nextVal = [] #the nextStuff
  y = []
  for w in next:
    s = dotProduct(inputs, w)
    y.append(s)
    nextVal.append(tranFunc(s))
  return nextVal, y

def feedforward(inputs, weights):
  y = []
  x = []
  xVal = inputs
  x.append(xVal)
  for layer in weights[:-1]:
    xVal, yVal = nextNodes(xVal, layer)
    x.append(xVal)
    y.append(yVal)
  final = weights[-1]
  finalOut = [xVal[i]*final[i] for i in range(len(xVal))]
  y.append(finalOut)
  return y, x, finalOut

def avg(lst):
  return sum(lst)/len(lst)

def error(t, y):
  return .5 * (t - y) ** 2
def deriv(x): return x*(1-x)

def backpropagation(x, y, w, t, err): #err is the value of err(t-result)
  newW = [[*i] for i in w]
  newX = [[*i] for i in x]
  newY = [[*i] for i in y]
  print('newW: ', newW)
  print('newY: ', newY)
  print('newX: ', newX)
  errPW = [{} for i in newW] #actually make the structure so I can go backwards, each weight has a error
  #ultimate first
  ultimate = err*x[-1][0] #CALCULATE
  errPW[-1][ultimate] = (0,0)
  print('errPW: ', errPW)
  #loop



def main():
  global weights, nodes, t_output, errLst, wSample # weights list of list
  weights = []
  lst = []
  with open(args[0]) as f:
    for line in f:
      i = line.split(' => ')
      lst.append([float(j) for j in i[0].split(' ')])
      lst[-1].append(float(i[1]))
  t_output = [i[-1] for i in lst]
  errLst = [0 for i in range(len(lst))]
  for i in range(100000):
    wSample = [[random.random()], [random.random() for i in range(2)],
               [random.random() for i in range((len(lst[0]) - 1) * 2)]][::-1]
    ran = random.randint(0, len(lst)-1)
    inputs, output = lst[ran][:-1], t_output[ran]
    y, x, result = feedforward(inputs, wSample)
    result = result[0]
    err = error(t_output[ran], result)
    errLst[ran] = err
    newW = backpropagation(x, y, wSample, t_output[ran], err)
    newNodes, newResult = feedforward(inputs, newW)
    newResult = newResult[0]
    err = error(t_output[ran], newResult)
    newErrLst = [e for e in errLst]
    newErrLst[ran] = err
    newTotErr = avg(newErrLst)
    print(f"RUN #{i}, error: {newTotErr}")
  print('FINAL error: ', minError)
  print('Layer counts [3, 2, 1, 1]')
  for l in minW:
    print(l)

if __name__ == '__main__':
  main()

#feed forward then back prop
# (1+ # of inputs) 2 1 1 NUM OF NODES per LAYER
# 2(1+# of inputs), 2, 1 NUM OF WEIGHTS
# Evelyn Li, pd 7, 2024