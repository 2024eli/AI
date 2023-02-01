import sys; args = sys.argv[1:]
from time import process_time

START = process_time()

#NEED TO ADD 0 TO FORNT OF HEAP ESSENTIAL!!!!

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

#test whatever
l1 = [7, 90, 990, 8]

print(l1)

#Gen new sequence of # as follows. Read f1, if see mult of 53, add smallest seen number that isnt alr in sequence to the list
def problem6():
  seen = [0]
  seenSet = set()
  sum = 0
  #l1.insert(0, 0)
  for i in l1:
    if i not in seenSet:
      seenSet.add(i)
      #print(f"Before: {seen}")
      insertVal(seen, i)
      #print(f"After: {seen}")
    if i % 53 == 0:
      sum += removeVal(seen)
  return sum


def main():
  print(f"#6: {problem6()}; {(process_time() - START):.3g}s")
  ELAPSE = process_time() - START
  print(f"Total time: {ELAPSE:.3g}s")

if __name__ == '__main__': main()
#Evelyn Li, pd 7, 2024