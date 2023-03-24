def bandit(testNum, armIdx, pullVal):
  global TODO,
  if testNum == 0:
    #reset globals
  if 1 <= testNum <= 999: #report on results of an arm pull
    #gives the value obtained upon the most recent pull of armIdx
    return testNum
  #in all circumstances the return val is the next arm to be pulled