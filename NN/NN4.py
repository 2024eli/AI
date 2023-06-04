import sys;args = sys.argv[1:]
import math;
import random
import time;

# args = ['weights1.txt', 'x*x+y*y>=1']

def deriv(x): return x*(1-x)
def getLayerCt(weight):
  weights = weight[::-1]
  layerCt = [1]
  prev = 1
  for w in weights:
    layerCt.append(len(w)//prev)
    prev = len(w)//prev
  return layerCt[::-1]
def getWCt(layer):
  weight = []
  for i, num in enumerate(layer[:-1]):
    weight.append(layer[i+1]*num)
  return weight

def derive(weights):
  #double the amt of weights
  #fill in empty spots with zeroes to eliminate cross talk
  #add last layer of weights to combine into one output and then tranFunc into final
  newW = [[] for w in range(len(weights)+1)]
  #layer 1 special case -------
  i = 0
  while i < len(weights[0]):
    newW[0] += [weights[0][i], 0, weights[0][i+1]]
    i+=2
  i = 0
  while i < len(weights[0]):
    newW[0] += [0, weights[0][i], weights[0][i+1]]
    i+=2
  #hidden layers ----------
  hiddenLayer = layerCt[1:]
  for layerNum in range(len(layerCt[1:-3])): #is it [1:-2] or [1:-1]
    i = hiddenLayer[layerNum]//2 #number of nodes in sq weight
    j = hiddenLayer[layerNum+1]//2 #splice the weight list
    for k in range(j):
      newW[layerNum+1] += [w for w in weights[layerNum+1][k*i:(k+1)*i]] + [0 for w in range(i)]
  for layerNum in range(len(layerCt[1:-3])):  # is it [1:-2] or [1:-1]
    i = hiddenLayer[layerNum] // 2  # number of nodes in sq weight
    j = hiddenLayer[layerNum + 1] // 2  # splice the weight list
    for k in range(j):
      newW[layerNum+1] += [0 for w in range(i)]+[w for w in weights[layerNum+1][k*i:(k+1)*i]]
  #penultimate layer special case -------
  k = -1 if inequality == '<' else 1
  newW[-2] = [k*i for i in weights[-1]]*2
  #ultimate layer special case ----------
  c = (1+math.exp(1))/(2) if inequality == '<' else (1+math.exp(1))/(2*math.exp(1))
  newW[-1] = [c]
  return newW

def main():
  global weights, wSample, layerCt, inequality# weights list of list
  wSample = []
  cases = []
  numInput = 2
  #args--------------
  with open(args[0]) as f:
    # for line in f: print(line)
    wSample = [[float(i) for i in line.split(', ')] for line in f if line.find('#') == -1]
  print('INEQUALITY:', args[1])
  argStr = args[1].replace('=', '')
  inequalityInd = argStr.find('<') if argStr.find('>') == -1 else argStr.find('>')
  inequality = argStr[inequalityInd]
  limit = float(argStr[inequalityInd+1:])
  #------------------
  sqlayerCt = getLayerCt(wSample)
  layerCt = [3]+ [i*2 for i in sqlayerCt[1:-1]] + [1, 1]
  print('weight count', getWCt(layerCt))
  #--------code goes here
  # adjust r
  secondLayerNum = sqlayerCt[1]*2
  wSample[0][::2] = [i/math.sqrt(limit) for num, i in enumerate(wSample[0][::2])]
  weights = derive(wSample)
  #--------code ends here
  print('\nFINAL---------')
  print(f"Weight counts {[len(w) for w in weights]}")
  print(f"Layer counts {layerCt}")
  for l in weights:
    print(l)


if __name__ == '__main__':
  main()

#feed forward then back prop
#things to change: transfer function, output, etc
# Evelyn Li, pd 7, 2024