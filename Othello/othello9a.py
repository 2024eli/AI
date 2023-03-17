import sys; args = sys.argv[1:]
import math
#Evelyn Li, Samarth Bhargav
args = ['P----CI----OR----AA----TC----EY----D']
b = args[0]
w = int(args[1]) if len(args)>1 else (min(i for i in range(math.ceil(len(b)**(1/2)), len(b)) if len(b)%i == 0))

L = [b, "".join(b[rs:rs+w][::-1] for rs in range(0, len(b), w))]
L += ["".join(d[cs::w][::-1] for cs in range(w)) for d in L]
L += ["".join(d[::-1]) for d in L]
print(L)
LL = {L[7]:"VF|90CW|180",L[6]:"1|90CW|180",L[5]:"VF|180",L[4]:"1|180",L[3]:"VF|90CW",
        L[2]: "1|90CW",L[1]: "VF",L[0]:"1"}
# L = [*{*L}]

def printpz(solved):
  for i in range(1, len(b)+1):
    if (i-1) % w == 0 and i != 0:
      print()
    print(solved[i - 1], end="")
  print()

for i in LL:
  print(i, LL[i])
print("\n".join(r for r in L))
for r in LL:
  printpz(r)
  print(LL[r])

#Evelyn Li, 7, 2024