import re
import sys
import random

# crossword assignment

# inputs
input = sys.argv[1:]
#print('Input:', input)

height, width, numBlocks = 0, 0, 0
wordDict = ''
hWords, vWords = [], [] # [(vPos, hPos, word), ...]

# test for matches:
# 0 indicates HxW
# 1 indicated number of blocks
# 2 indicates horizontal words
# 3 indicates vertical words
matchTests = [r'^(\d+)x(\d+)$', r'^\d+$', r'^H(\d+)x(\d+)(.+)$', r'^V(\d+)x(\d+)(.+)$']

for arg in input:
    if '.txt' in arg.lower():
        wordDict = arg
        continue
    for testNum, matchTest in enumerate(matchTests):
        match = re.search(matchTest, arg, re.I)
        if not match: continue
        if testNum == 0:
            height = int(arg[:arg.lower().find('x')])
            width = int(arg[arg.lower().find('x')+1:])
        elif testNum == 1:
            numBlocks = int(arg)
        elif testNum == 2:
            vPos, hPos, word = int(match.group(1)), int(match.group(2)),\
                               match.group(3).lower()
            hWords.append((vPos, hPos, word))
        elif testNum == 3:
            vPos, hPos, word = int(match.group(1)), int(match.group(2)), \
                               match.group(3).lower()
            vWords.append((vPos, hPos, word))

#print('Inputs: \n Dictionary: {}\n HxW = {}x{}\n numBlocks = {}\n hWords = {}\n vWords = {}'
#      .format(wordDict, height, width, numBlocks, hWords, vWords))

##################
# HELPER METHODS #


def printXW(puzzle, width):
    for index in range(len(puzzle)):  # matr is a string in this case
        if index % width == 0:  # left side
            print('{} '.format(puzzle[index]), end='')
        elif index % width == width - 1:  # right side
            print('{}\n'.format(puzzle[index]), end='')
        else:
            print('{} '.format(puzzle[index]), end='')
    print('\n')


def addVword(xw, vPos, hPos, word, width):
    if xw == -1: return -1
    wordIndexes = []
    for k in range(len(word)):
        index = (vPos + k)*width + hPos
        if index > len(xw)-1:
            print('{} doesn\'t fit in location {}. (V)'.format(word, index))
            return -1
        wordIndexes.append(index)
    newXW = ''
    for k in range(len(wordIndexes)):
        if xw[wordIndexes[k]] not in ('-', '~'):
            if xw[wordIndexes[k]] == word[k]:
                continue
            else:
                print('Can\'t overlap {} from {} over {} at index {}.'.format(word[k], word, xw[wordIndexes[k]], wordIndexes[k]))
                return -1
        newXW = xw[:wordIndexes[k]] + word[k] + xw[wordIndexes[k]+1:]
    return newXW


def addHword(xw, vPos, hPos, word, width):
    #printXW(xw, width)
    # assumes that the word fits
    # (for now)
    if xw == -1: return -1
    startInd = vPos*width + hPos
    endInd = startInd + len(word)
    if startInd//width != (endInd-1)//width:
        print('Word {} doesn\'t fit in location (H).'.format(word))
        return -1
    for index in range(startInd, endInd + 1):
        if xw[index] not in ('-', '~'):
            if xw[index] == word[startInd - index]:
                continue
            else:
                return -1
    newXW = xw[:startInd] + word + xw[endInd:]
    return newXW


def setIndex(xw, index, character):
    if xw == -1:
        return xw
    if xw[index] == character:
        return xw
    if xw[index] in ('~', '#'):
        return -1
    return xw[:index] + character + xw[index + 1:]


def fillInputs(height, width, hWords, vWords):
     xw = ''.join(['-' for num in range(height*width)])
     for vWord in vWords:
        vPos, hPos, word = vWord
        xw = addVword(xw, vPos, hPos, word, width)
     for hWord in hWords:
         vPos, hPos, word = hWord
         xw = addHword(xw, vPos, hPos, word, width)
     return xw


def protectBoard(xw):
    for index in range(len(xw)):
        if xw[index] not in ('#', '-'):
            # if it's not one of those two its a letter
            xw = setIndex(xw, index, '~')
    return xw


def palindromize(xw):
    length = len(xw)
    for index in range(length):
        if xw[index] == '-' and xw[length - 1 - index] == '#':
            # if the mirror of the cell is blocked and the
            # current one isn't, block it
            xw = setIndex(xw, index, '#')
        elif xw[index] == '#' and xw[length - 1 - index] == '~':
            # if the cell is blocked and its mirror is protected
            # then it's an impossible blocking
            return -1 # impossible crossword
    return xw


def checkEdges(xw, width):
    for index in range(len(xw)):
        if index // width == 0:
            # top row
            if xw[index + width*2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index + width, '#')
                if xw == -1:
                    return xw
            elif xw[index + width] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
        elif index // width == width - 1:
            # bottom row
            if xw[index - width*2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index - width, '#')
                if xw == -1:
                    return xw
            elif xw[index - width] == '#':
                if xw == -1:
                    return xw
        if index % width == 0:
            # left column
            if xw[index + 2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index+1, '#')
                if xw == -1:
                    return xw
            elif xw[index + 1] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
        elif index % width == width - 1:
            # right column
            if xw[index - 2] == '#':
                xw = setIndex(xw, index, '#')
                xw = setIndex(xw, index - 1, '#')
                if xw == -1:
                    return xw
            elif xw[index - 1] == '#':
                xw = setIndex(xw, index, '#')
                if xw == -1:
                    return xw
    return xw


def checkRest(xw, width, blocks):
    # could be done better with a lookup table like I did in the othello
    # labs, but that would require more debugging and this works
    for index in blocks:
        checkInds = {index - width*3, index - width*2,
                     index + width*3, index + width*2}
        horizontal = [index - 3, index - 2,
                     index + 3, index + 2]
        for h in horizontal:
            if h//width == index//width: checkInds.add(h)
        for i in checkInds:
            if xw == -1: return -1
            if 0 <= i < len(xw):
                if xw[i] == '#':
                    if i == index-width*3:
                        xw = setIndex(xw, index - width*2, '#')
                        xw = setIndex(xw, index - width, '#')
                    elif i == index-width*2:
                        xw = setIndex(xw, index - width, '#')
                    elif i == index+width*3:
                        xw = setIndex(xw, index + width*2, '#')
                        xw = setIndex(xw, index + width, '#')
                    elif i == index+width*2:
                        xw = setIndex(xw, index + width, '#')
                    elif i  == index-3:
                        xw = setIndex(xw, index - 2, '#')
                        xw = setIndex(xw, index - 1, '#')
                    elif i == index-2:
                        xw = setIndex(xw, index - 1, '#')
                    elif i == index+3:
                        xw = setIndex(xw, index + 2, '#')
                        xw = setIndex(xw, index + 1, '#')
                    elif i == index+2:
                        xw = setIndex(xw, index + 1, '#')
    return xw


def checkConnected(xw, width, vPos, hPos, numSpaces):
    index = vPos*width + hPos
    if 0 <= index < len(xw) and xw[index] == '-':
        xw = setIndex(xw, index, '*')
        xw = checkConnected(xw, width, vPos + 1, hPos, numSpaces)
        xw = checkConnected(xw, width, vPos - 1, hPos, numSpaces)
        if (hPos + 1) % width:
            xw = checkConnected(xw, width, vPos, hPos + 1, numSpaces)
        if (hPos - 1) % width != width - 1:
            xw = checkConnected(xw, width, vPos, hPos - 1, numSpaces)
    return xw


def makeImplications(xw, width, numBlocks):
    prevBlocks = xw.count('#')
    currBlocks = 0
    while prevBlocks != currBlocks:
        prevBlocks = currBlocks
        if xw == -1: return -1
        xw = checkEdges(xw, width)
        if xw == -1: return -1
        blockInds = {i for i in range(len(xw)) if xw[i] == '#'}
        xw = checkRest(xw, width, blockInds)
        if xw == -1: return -1
        xw = palindromize(xw)
        if xw == -1: return -1
        if xw.count('#') > numBlocks: return -1
        currBlocks = xw.count('#')
    return xw


def addBlocks(xw, height, width, numBlocks):
    xw = makeImplications(xw, width, numBlocks)
    if height*width == numBlocks:
        xw = '#'*(height*width)
        return xw
    if height%2 + width%2 + numBlocks%2 == 3:
        # if height, width, and numBlocks are
        # odd, then you must place a block in the center
        xw = setIndex(xw, int((len(xw)-1)/2), '#')
    elif height%2 + width%2 == 2:
        # otherwise make sure not to put block at center
        xw = setIndex(xw, int((len(xw) - 1) / 2), '~')
    availableIndexes = [i for i in range(len(xw)) if xw[i] == '-']
    random.shuffle(availableIndexes)
    length = len(xw)
    blocksLeft = numBlocks - xw.count('#')
    while availableIndexes and blocksLeft:
        newIndex = availableIndexes.pop()
        if xw[newIndex] == '#':
            while xw[newIndex] == '#':
                newIndex = availableIndexes.pop()
        if len(availableIndexes) == 0:
            continue
            #print("EMPTIED AVAILABLE INDEXES")
        newXW = setIndex(xw, newIndex, '#')
        newXW = makeImplications(newXW, width, numBlocks)
        if newXW == -1:
            if length - newIndex - 1 in availableIndexes:
                availableIndexes.remove(length - newIndex - 1)
        else:
            xw = newXW
            if xw.count('#') == numBlocks:
                xw = xw.replace('~', '-')
                return xw
            blocksLeft = numBlocks - xw.count('#')
    return xw


def makeAttempts(xw, height, width, numBlocks):
    attempts = 100
    while attempts > 0:
        printXW(xw, width)
        newXW = addBlocks(xw, height, width, numBlocks)
        newXW = newXW.replace('~', '-')
        openSpaces = len(newXW) - numBlocks
        v, h = newXW.find('-') // width, newXW.find('-') % width
        numConnect = checkConnected(newXW, width, v, h, openSpaces)
        if numConnect.count('*') == openSpaces:
            return newXW
        attempts = attempts - 1
    return ''


# create structure
xw = fillInputs(height, width, hWords, vWords)
xw = protectBoard(xw)
xw = palindromize(xw)
printXW(xw, width)
if xw != -1:
    xw = makeAttempts(xw, height, width, numBlocks)
if xw != -1:
    printXW(xw, width)
else: print('Impossible')