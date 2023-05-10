#NOT MY CODE

import sys; args = sys.argv[1:]

args =[3, '01121223', 'AHBCDGFE', 'training.txt']
# args order: # of inputs, compacted outputs, file order, filename to write
# for example: 3 11010011 EACBFDHG training.txt
def main():
    count = int(args[0])
    val = args[1]
    out_count = len(bin(int(max(val)))[2:])
    order = args[2]
    f = open(args[3], 'w')
    vals = {}
    for i in range(len(val)):
        vals[chr(ord('A')+i)] = f'{" ".join(bin(i)[2:].zfill(count))} => {" ".join(bin(int(val[i]))[2:].zfill(out_count))}\n'
    for c in order:
        if c == order[-1]:
            f.write(vals[c].strip())
        else:
            f.write(vals[c])
    f.close()
    print('done')


if __name__ == '__main__':
    main()
