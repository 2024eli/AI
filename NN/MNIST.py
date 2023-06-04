import sys;args = sys.argv[1:]
import math;
import random
import time;
import time;
import numpy as np;

args = ['mnist_train.csv', 'mnist_test.csv']

def dotProduct(v1, v2): return sum(hadamardProduct(v1, v2))
def hadamardProduct(v1, v2): return [v1[i] * v2[i] for i in range(len(v1))]
def tranFunc(input): return 1/(1+math.exp(-input)) #log
def nextNodes(inputs, layer):
  #find next num of nodes
  next = []
  for i in range(len(layer)//len(inputs)):
    next += [layer[i*len(inputs):(i+1)*len(inputs)]] #weights used
  nextVal = [] #the nextStuff
  for w in next:
    s = dotProduct(inputs, w)
    nextVal.append(tranFunc(s))
  return nextVal
def feedforward(inputs, weights):
  x = []
  xVal = inputs
  x.append(xVal)
  for layer in weights[:-1]:
    xVal = nextNodes(xVal, layer)
    x.append(xVal)
  final = weights[-1]
  finalOut = [xVal[i]*final[i] for i in range(len(xVal))]
  return x, finalOut
def check(t, y):
  max = -1e9
  maxInd = 0
  correctInd = 0
  for ct, i in enumerate(y):
    if i > max:
      max = i
      maxInd = ct
  for i in range(10):
    if t[i] == 1:
      correctInd = i
      break
  return 1 if maxInd == correctInd else 0
def deriv(x): return x*(1-x)

def run(weights):
  accuracy = 0
  count = 0
  for case in testLst:
    count+= 1
    inputs, output = case[1:] + [1], case[0]  # t is expected output
    t = [0 for i in range(10)]
    t[output] = 1
    result = feedforward(inputs, weights)[1]
    accuracy += check(t, result)
  return accuracy*100/count

def backpropagation(xVal, t, weight): #err is the value of err(t-result)
  x = xVal[1:]
  x = x[::-1]
  k = 0.3 #learning rate
  errors = [[*i] for i in x]
  weights = [[i for i in j] for j in weight]
  weights = weights[::-1]
  for i in range(len(x)): #extra layer of errors
    if i == 0:
      for j in range(len(t)):
        errors[i][j] = (t[j] - x[i][j])
      continue
    if i == 1: #change for test 11
      for j in range(len(t)):
        errors[i][j] = (errors[0][j])*weights[i-1][j]*deriv(x[i][j])
      continue
    for j in range(len(x[i])):
      errors[i][j] = deriv(x[i][j]) * sum(weights[i-1][len(x[i])*k+j]*errors[i-1][k] for k in range(len(x[i-1])))
  partial = [[] for i in weights]
  weights = weights[::-1]
  x = x[::-1]
  errors = errors[::-1]
  for i in range(len(weights)):
    for j in range(len(weights[i])):
      if i + 1 == len(weights): #if last layer
        partial[i].append(xVal[i][j % len(xVal[i])] * errors[i][j])
      else:
        partial[i].append(xVal[i][j%len(xVal[i])] * errors[i][j//len(xVal[i])])
  return [[weights[i][j] + k*partial[i][j] for j in range(len(weights[i]))] for i in range(len(weights))]

def main():
  global nodes, t_output, errLst, wSample, testLst, t # weights list of list
  wSample = [[random.uniform(-1, 1) for i in range((28**2+1)*300)],
             [random.uniform(-1, 1) for i in range(30000)],
             [random.uniform(-1, 1) for i in range(1000)],
             [random.uniform(-1, 1) for i in range(10)]]
  count = 0
  accuracy = 0
  trainLst = list()
  testLst = list()
  newW = None
  with open(args[0]) as train:
    for line in train:
      trainLst.append([int(line[0])] + [float(i) / 255 for i in line[2:].split(',')])
  with open(args[1]) as test:
    for line in test:
      testLst.append([int(line[0])] + [float(i) / 255 for i in line[2:].split(',')])
  for epoch in range(10):
    count = 0
    for case in trainLst:
      count+= 1
      inputs, output = case[1:] + [1], case[0] #t is expected output
      t = [0 for i in range(10)]
      t[output] = 1
      x, result = feedforward(inputs, wSample)
      x.append(result)
      newW = backpropagation(x, t, wSample)
      accuracy += check(t, result)
      wSample = [[w for w in weight] for weight in newW]
      if count % 100 == 0:
        print('training...')
        print(f"RUN #{count}, Accuracy: {(accuracy/count)*100:.4g}%")
      # if count % 10000 == 0:
      #   print('\nFINAL---------')
      #   print(f"RUN #{count}, Accuracy: {run(newW)}%")
    print(f"EPOCH #{epoch}, Accuracy: {run(newW)}");


if __name__ == '__main__':
  main()

#feed forward then back prop
#60,000 digits in training set (1 epoch is to go through all of this)
# Evelyn Li, pd 7, 2024