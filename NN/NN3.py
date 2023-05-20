import sys;args = sys.argv[1:]
import math;
import random
import time;

args = ['training.txt']

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
  # print(inputs, weights, final, xVal)
  finalOut = [xVal[i]*final[i] for i in range(len(xVal))]
  y.append(finalOut)
  return y, x, finalOut[0]

def avg(lst):
  return sum(lst)/len(lst)

def error(t, y):
  return .5 * (t - y) ** 2
def deriv(x): return x*(1-x)

def backpropagation(xVal, t, weight, k): #err is the value of err(t-result)
  x = xVal[1:]
  x = x[::-1]
  errors = [[*i] for i in x]
  weights = [[i for i in j] for j in weight]
  weights = weights[::-1]
  for i in range(len(x)): #extra layer of errors
    if i == 0:
      errors[i][0] = (t - x[i][0])
      continue
    if i == 1: #change for test 11
      errors[i][0] = (errors[0][0])*weights[i-1][0]*deriv(x[i][0])
      continue
    for j in range(len(x[i])):
      errors[i][j] = deriv(x[i][j]) * sum(weights[i-1][len(x[i])*k+j]*errors[i-1][k] for k in range(len(x[i-1])))
  partial = [[] for i in weights]
  weights = weights[::-1]
  x = x[::-1]
  errors = errors[::-1]
  for i in range(len(weights)):
    for j in range(len(weights[i])):
      partial[i].append(xVal[i][j%len(xVal[i])] * errors[i][j//len(xVal[i])])
  return [[weights[i][j] + k*partial[i][j] for j in range(len(weights[i]))] for i in range(len(weights))]

def main():
  global weights, nodes, t_output, errLst, wSample # weights list of list
  weights = []
  numInput = 2
  #args--------------
  argStr = args[0].replace('=', '')
  inequalityInd = argStr.find('<') if argStr.find('>') == -1 else argStr.find('>')
  inequality = argStr[inequalityInd]
  limit = float(argStr[inequalityInd+1:])
  #------------------
  wSample = [[random.uniform(-1, 1) for i in range(15)],
             [random.uniform(-1, 1) for i in range(15)],
             [random.uniform(-1, 1) for i in range(3)],
             [random.uniform(-1, 1) for i in range(1)]]
  count = 0
  t = 0
  k = 0.3
  while True:
    count+= 1
    # print('**************************************')
    xVal = random.uniform(-1.5, 1.5)
    yVal = random.uniform(-1.5, 1.5)
    if inequality == '<':
      t = 1 if xVal**2+yVal**2 < limit else 0
    if inequality == '>':
      t = 1 if xVal ** 2 + yVal ** 2 > limit else 0
    y, x, result = feedforward([xVal, yVal, 1], wSample)
    x.append([result])
    newW = backpropagation(x, t, wSample, k)
    wSample = [[w for w in weight] for weight in newW]
    if count % 5000 == 0:
      print('\nFINAL---------')
      print(f"RUN #{count}, actual: {result}, expect: {t}")
      print(f"Error: {0.5 * (result - t) ** 2}")
      print(f"Layer counts [3, 5, 3, 1, 1]")
      for l in newW:
        print(l)
      k = k*0.975


if __name__ == '__main__':
  main()

#feed forward then back prop
#things to change: transfer function, output, etc
# Evelyn Li, pd 7, 2024