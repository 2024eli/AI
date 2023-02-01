import sys; args = sys.argv[1:]
from time import process_time

START = process_time()

#HeapPQ functions
def heapUp(heap, k):
  parent = k//2
  if parent == 0:
    return
  if heap[parent] > heap[k]:
    heap[k], heap[parent] = heap[parent], heap[k]
    heapUp(heap, parent)

def heapDown(heap, k, last):
  l = 2*k
  r = 2*k+1
  if k > last or l > last:
    return
  if r > last:
    if heap[k] > heap[l]:
      heap[k], heap[l] = heap[l], heap[k]
  else:
    min = l if heap[l] < heap[r] else r
    if heap[k] > heap[min]:
      heap[k], heap[min] = heap[min], heap[k]
      heapDown(heap, min, last)

def removeVal(heap):
  heap[1], heap[-1] = heap[-1], heap[1]
  it = heap.pop()
  heapDown(heap, 1, len(heap)-1)
  return it

def insertVal(heap, val):
  heap.append(val)
  heapUp(heap, len(heap)-1)
  return True

def peekPQ(heap):
  if len(heap)!=1:
    return heap[1]
  return None

def dctOccur(lst):
  dct = dict()
  for i in lst:
    dct[i] = dct.get(i, 0) + 1
  return dct


with open(args[0]) as f:
  l1 = [int(line.strip()) for line in f]
with open(args[1]) as f:
  l2 = [int(line.strip()) for line in f]
with open(args[2]) as f:
  l3 = [int(line.strip()) for line in f]

#How many distinct values appear in both f1 and f2?
def problem1():
  return len({*l2} & {*l1})

#Reading f1 from top to bottom, find 100th unique value, 200th, 300th, etc and add all tgt. Find sum?
def problem2():
  #cant use deref set because set changes order
  lstSeen = set()
  lst = [i for i in l1 if i not in lstSeen and not lstSeen.add(i)]
  return sum([lst[i-1] for i in range(100, len({*l1}), 100)])

#Print the total number of times any value in f3 appears in f1 and/or f2.
def problem3():
  d1 = dctOccur(l1)
  d2 = dctOccur(l2)
  sum = 0
  for it in l3:
    if it in d1:
      sum += d1[it]
    if it in d2:
      sum += d2[it]
  return sum

#Print a list of the 10 smallest numbers that appear at least once in f1. Print a single list in increasing order
def problem4():
  return sorted({*l1})[:10]

#Print a list of the 10 largest numbers that appear at least twice in f2. Print in a single list in decreasing order
def problem5():
  lst = []
  l2.sort()
  rev2 = l2[::-1]
  for i in range(1, len(rev2)-1):
    if len(lst) == 10:
      break
    if rev2[i] != rev2[i+1] and rev2[i] == rev2[i-1]:
      lst.append(rev2[i])
  return lst

#Generate a new sequence of numbers: read f1 and everytime multiple of 53 is seen, add smallest number
#in all the ones that we've seen that isnt in the new sequence.
def problem6():
  seen = [0]
  seenSet = set()
  sum = 0
  for i in l1:
    if i not in seenSet:
      seenSet.add(i)
      insertVal(seen, i)
    if i % 53 == 0:
      sum += removeVal(seen)
  return sum


def main():
  print(f"#1: {problem1()}; {((first:=process_time()) - START):.3g}s")
  print(f"#2: {problem2()}; {((second:=process_time()) - first):.3g}s")
  print(f"#3: {problem3()}; {((third:=process_time()) - second):.3g}s")
  print(f"#4: {problem4()}; {((fourth:=process_time()) - third):.3g}s")
  print(f"#5: {problem5()}; {((fifth:=process_time()) - fourth):.3g}s")
  print(f"#6: {problem6()}; {(process_time() - fifth):.3g}s")
  ELAPSE = process_time() - START
  print(f"Total time: {ELAPSE:.3g}s")

if __name__ == '__main__': main()
#Evelyn Li, pd 7, 2024