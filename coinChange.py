import sys
sys.setrecursionlimit(10000)

CACHE = {}

def change(n, coinLst):
  if n < 0 or not coinLst: return 0
  elif n == 0: return 1
  key = (n, *coinLst)
  #if key in CACHE: return CACHE[key]
  if key not in CACHE:
    CACHE[key] = change(n-coinLst[0], coinLst) + change(n, coinLst[1:])
  return CACHE[key]

def main():
  print(change(100*100, [100, 50, 25, 10, 5, 1]))

if __name__ == '__main__':
  main()

# Evelyn Li, pd 7, 2024