#2. print 2d puzzles
print("".join([solved[i-1] + ("\n")*(i%WIDTH==0)*(i!=0) for i in range(1, SIZE+1)]))
#3. symbolSet
SYMLST = {i for i in pzl} - {'.'}
other = list('0ZYXWVUTSRQPONMLKJIHGFEDCBA987654321')
while (len(SYMLST) != WIDTH):
  SYMLST.append(other.pop())
#4. CS for row and col
rowcs = [{i for i in range(r*WIDTH, (r+1)*WIDTH)} for r in range(WIDTH)]
colcs = [{i for i in range(c, c+SIZE-miniW*miniH+1, miniW*miniH)} for c in range(WIDTH)]
#5a. isInvalid looping through the cs.
CSTR = rowcs + colcs + subcs
#5b. isInvalid looping thorugh last pos cs.
posToCS = {i: [rowcs[i//WIDTH], colcs[i%WIDTH], *(j for j in subcs if i in j)] for i in range(SIZE)}
#5c. isInvalid neighbors so no dupes
NBRS = {i: posToCS[i][0] | posToCS[i][1] | posToCS[i][2] for i in posToCS}
#6. Best dot
sum((pzl[i] == pzl[pos])*(i!=pos) for s in posToCS[pos] for i in s) > 0
bestDot = sorted([(sum(1 for i in NBRS[c] if pzl[i] != '.'), c) for c, it in enumerate(pzl) if it == "."],reverse=True)
#diagonal
diagonal = [i for i in range(SIZE) if (r:=i//WIDTH) == (c:=i%WIDTH) or r+c == WIDTH-1]