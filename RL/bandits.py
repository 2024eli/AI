import math, random

def bandit(testNum, armIdx, pullVal):
  global avg, times, ucb, c
  if testNum == 0:
    c = 0.96
    times = [1 for i in range(10)]
    avg = [0 for i in range(10)]
    ucb = [5 for i in range(10)]
    return 0
  times[armIdx] += 1
  avg[armIdx] += (1 / times[armIdx]) * (pullVal - avg[armIdx])
  maxArm = 0
  maxVal = 0
  for i in range(10):
    ucb[i] = avg[i] + c * (math.log(testNum) / times[i])**0.5
    if ucb[i] > maxVal:
      maxVal = ucb[i]
      maxArm = i
  return maxArm

# Evelyn Li, pd 7, 2024