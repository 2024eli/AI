import math, random

#eval function x*(50-x-y-z-w) <-- maximize this

def eval(x, y, z, w):
  return x*(50-x-y-z-w)

def run(x):
  bestX = 0
  maxVal = 0
  avg = 0
  for i in range(10000):
    y = random.randint(0, 15)
    z = random.randint(0, 15)
    w = random.randint(0, 15)
    # print(x, y, z, w)
    val = eval(x, y, z, w)
    avg += val
  return avg/10000

sum = 0
for i in range(50):
  print(i, ':', run(i))
