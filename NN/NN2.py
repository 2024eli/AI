import sys;args = sys.argv[1:]
import math;
import random
import time;

# args = ['training.txt']

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

def backpropagation(xVal, t, weight): #err is the value of err(t-result)
  x = xVal[1:]
  x = x[::-1]
  k = 0.2 #learning rate
  errors = [[*i] for i in x]
  weights = [[i for i in j] for j in weight]
  weights = weights[::-1]
  # print('WEIGHTS', weights)
  for i in range(len(x)): #extra layer of errors
    # print('\nERR: ', errors)
    if i == 0:
      # print("input: ", t-x[i][0])
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
  # print('\nERR: ', errors)
  for i in range(len(weights)):
    for j in range(len(weights[i])):
      # print('x[i]', xVal[i])
      # print('x_layer_i', xVal[i][j//len(xVal[i])])
      # print('E_j_layer+1', errors[i][j//len(xVal[i])])
      # print('partial', partial)
      partial[i].append(xVal[i][j%len(xVal[i])] * errors[i][j//len(xVal[i])])
      # print('I MADE IT')
  # print('\npartial', partial)
  return [[weights[i][j] + k*partial[i][j] for j in range(len(weights[i]))] for i in range(len(weights))]

def main():
  global weights, nodes, t_output, errLst, wSample # weights list of list
  weights = []
  lst = []
  numInp = 0
  bestRun = 0
  minErr = 1
  minW = []
  with open(args[0]) as f:
    for line in f:
      print(line)
      i = line.split(' => ')
      numInp = len(i[0].split(' '))
      i = [j.strip() for j in i]
      lst.append([float(j) for j in i[0].split(' ')])
      lst[-1] += [float(j) for j in i[1].split(' ')]
  t_output = [i[-1:-(len(lst[0])-numInp)-1:-1] for i in lst]
  wSample = [[random.uniform(-1, 1)], [random.uniform(-1, 1) for i in range(2)],
             [random.uniform(-1, 1) for i in range((numInp+1) * 2)]][::-1]
  # wSample = [[0.3], [0.3 for i in range(2)],
  #            [0.3 for i in range((len(lst[0])) * 2)]][::-1]
  count = 0
  while True:
    count+= 1
    for i in range(len(lst)):
      # print('**************************************')
      inputs, output = lst[i][:-1] + [1], t_output[i][0] #t is expected output
      y, x, result = feedforward(inputs, wSample)
      # print('AFTER FIRST FEEDFORWARD------')
      # print('WEIGHTS', wSample)
      # print('X VAL: ', x)
      # print('FINAL OUTPUT: ', result)
      x.append([result])
      # print()
      # print('BACKPROPAGATION-------')
      newW = backpropagation(x, output, wSample)
      # print('\nNEW WEIGHTS', newW)
      wSample = [[w for w in weight] for weight in newW]
      if count % 1000 == 0:
        print('\nFINAL---------')
        print(f"RUN #{count}, actual: {result}, expect: {output}")
        print(f"Layer counts [{numInp + 1}, 2, 1, 1]")
        for l in newW:
          print(l)


if __name__ == '__main__':
  main()

#feed forward then back prop
# (1+ # of inputs) 2 1 1 NUM OF NODES per LAYER
# 2(1+# of inputs), 2, 1 NUM OF WEIGHTS
# Evelyn Li, pd 7, 2024