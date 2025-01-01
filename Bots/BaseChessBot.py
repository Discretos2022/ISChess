# SV
#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#
import time
from random import Random

import numpy as np
from PyQt6 import QtCore

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot


#   Simply move the pawns forward and tries to capture as soon as possible
def chess_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    for x in range(board.shape[0] - 1):
        for y in range(board.shape[1]):
            if board[x, y] != "p" + color:
                continue
            if y > 0 and board[x + 1, y - 1] != '' and board[x + 1, y - 1][-1] != color:
                return (x, y), (x + 1, y - 1)
            if y < board.shape[1] - 1 and board[x + 1, y + 1] != '' and board[x + 1, y + 1][1] != color:
                return (x, y), (x + 1, y + 1)
            elif board[x + 1, y] == '':
                return (x, y), (x + 1, y)

    time.sleep(1)
    return (0, 0), (0, 0)


def chess_bot_tower(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    for x in range(board.shape[0] - 1):
        for y in range(board.shape[1]):
            if board[x, y] != "r" + color:
                continue
            if y > 0 and board[x + 1, y] != '' and board[x + 1, y][-1] != color:
                return (x, y), (x + 1, y)
            if y < board.shape[1] - 1 and board[x + 1, y] != '' and board[x + 1, y][1] != color:
                return (x, y), (x + 1, y)
            elif board[x + 1, y] == '':
                return (x, y), (x + 1, y)

    time.sleep(1)
    return (0, 0), (0, 0)


def printBoard(board):
    print("—————————————————————————————————————————")
    for i in range(board.shape[0]):
        line = ""
        line += "| "
        for j in range(board.shape[1]):
            if board[i, j] == "":
                line += "   | "
            else:
                line += board[i, j] + " | "
        print(line)
        print("—————————————————————————————————————————")


def printBoardWithDisplacement(board, disp: tuple, color):
    print("—————————————————————————————————————————")
    for i in range(board.shape[0]):
        line = ""
        line += "| "
        for j in range(board.shape[1]):
            if board[i, j] == "":
                if disp[1].__contains__((i, j)):
                    line += "[] | "
                else:
                    line += "   | "
            else:
                if board[i, j][-1] != color and disp[1].__contains__((i, j)):
                    line += ">< | "
                else:
                    line += board[i, j] + " | "
        print(line)
        print("—————————————————————————————————————————")


def nextBoard(board, start, end):
    result = board.copy()

    x: int = start[0]
    y: int = start[1]
    p = result[x, y]
    result[x, y] = ""

    x: int = end[0]
    y: int = end[1]
    result[x][y] = p

    return result


def nextBoardWithRotation(board, start, end):
    result = board.copy()

    x: int = start[0]
    y: int = start[1]
    p = result[x, y]

    if p[0] == "p":
        p = "q" + p[1]

    result[x, y] = ""

    x: int = end[0]
    y: int = end[1]
    result[x][y] = p

    newBoard = np.rot90(result, 2)
    # printBoard(newBoard)

    return newBoard


def getRookDisplacement(board, pos: tuple, color):  # (x, y)

    x = pos[0]
    y = pos[1]

    disp = []

    # v
    for i in range(x + 1, board.shape[0]):

        if board[i, y] != '' and board[i, y][-1] == color:
            break
        if board[i, y] != '' and board[i, y][-1] != color:
            disp.append((i, y))
            break
        if board[i, y] == '':
            disp.append((i, y))

    # ^
    for i in range(x - 1, -1, -1):

        if board[i, y] != '' and board[i, y][-1] == color:
            break
        if board[i, y] != '' and board[i, y][-1] != color:
            disp.append((i, y))
            break
        if board[i, y] == '':
            disp.append((i, y))

    # <
    for i in range(y - 1, -1, -1):
        if board[x, i] == '':
            disp.append((x, i))
        if board[x, i] != '' and board[x, i][-1] == color:
            break
        if board[x, i] != '' and board[x, i][-1] != color:
            disp.append((x, i))
            break

    # >
    for i in range(y + 1, board.shape[1]):
        if board[x, i] == '':
            disp.append((x, i))
        if board[x, i] != '' and board[x, i][-1] == color:
            break
        if board[x, i] != '' and board[x, i][-1] != color:
            disp.append((x, i))
            break

    return disp


def getPawnDisplacement(board, pos: tuple, color):
    x = pos[0]
    y = pos[1]

    disp = []

    if x < (board.shape[0] - 1) and board[x + 1, y] == '':
        disp.append((x + 1, y))
    if x < (board.shape[0] - 1) and y > 0 and board[x + 1, y - 1] != '' and board[x + 1, y - 1][1] != color:
        disp.append((x + 1, y - 1))
    if x < (board.shape[0] - 1) and y < (board.shape[1] - 1) and board[x + 1, y + 1] != '' and board[x + 1, y + 1][
        1] != color:
        disp.append((x + 1, y + 1))

    return disp


def getQueenDisplacement(board, pos: tuple, color):  # (x, y)

    x = pos[0]
    y = pos[1]

    disp = []

    # v
    for i in range(x + 1, board.shape[0]):

        if board[i, y] != '' and board[i, y][-1] == color:
            break
        if board[i, y] != '' and board[i, y][-1] != color:
            disp.append((i, y))
            break
        if board[i, y] == '':
            disp.append((i, y))

    # ^
    for i in range(x - 1, -1, -1):

        if board[i, y] != '' and board[i, y][-1] == color:
            break
        if board[i, y] != '' and board[i, y][-1] != color:
            disp.append((i, y))
            break
        if board[i, y] == '':
            disp.append((i, y))

    # <
    for i in range(y - 1, -1, -1):
        if board[x, i] == '':
            disp.append((x, i))
        if board[x, i] != '' and board[x, i][-1] == color:
            break
        if board[x, i] != '' and board[x, i][-1] != color:
            disp.append((x, i))
            break

    # >
    for i in range(y + 1, board.shape[1]):
        if board[x, i] == '':
            disp.append((x, i))
        if board[x, i] != '' and board[x, i][-1] == color:
            break
        if board[x, i] != '' and board[x, i][-1] != color:
            disp.append((x, i))
            break

    #  / haut
    for i in range(1, board.shape[0]):
        if x - i >= 0 and y + i < board.shape[0]:
            if board[x - i, y + i] == '':
                disp.append((x - i, y + i))
            if board[x - i, y + i] != '' and board[x - i, y + i][-1] == color:
                break
            if board[x - i, y + i] != '' and board[x - i, y + i][-1] != color:
                disp.append((x - i, y + i))
                break

    #  / bas
    for i in range(1, board.shape[0]):
        if x + i < board.shape[0] and y - i >= 0:
            if board[x + i, y - i] == '':
                disp.append((x + i, y - i))
            if board[x + i, y - i] != '' and board[x + i, y - i][-1] == color:
                break
            if board[x + i, y - i] != '' and board[x + i, y - i][-1] != color:
                disp.append((x + i, y - i))
                break

    #  \ haut
    for i in range(1, board.shape[0]):
        if x + i < board.shape[0] and y + i < board.shape[0]:
            if board[x + i, y + i] == '':
                disp.append((x + i, y + i))
            if board[x + i, y + i] != '' and board[x + i, y + i][-1] == color:
                break
            if board[x + i, y + i] != '' and board[x + i, y + i][-1] != color:
                disp.append((x + i, y + i))
                break

    #  \ bas
    for i in range(1, board.shape[0]):
        if x - i >= 0 and y - i >= 0:
            if board[x - i, y - i] == '':
                disp.append((x - i, y - i))
            if board[x - i, y - i] != '' and board[x - i, y - i][-1] == color:
                break
            if board[x - i, y - i] != '' and board[x - i, y - i][-1] != color:
                disp.append((x - i, y - i))
                break

    return disp


def getBishopDisplacement(board, pos: tuple, color):
    x = pos[0]
    y = pos[1]

    disp = []

    #  / haut
    for i in range(1, board.shape[0]):
        if x - i >= 0 and y + i < board.shape[0]:
            if board[x - i, y + i] == '':
                disp.append((x - i, y + i))
            if board[x - i, y + i] != '' and board[x - i, y + i][-1] == color:
                break
            if board[x - i, y + i] != '' and board[x - i, y + i][-1] != color:
                disp.append((x - i, y + i))
                break

    #  / bas
    for i in range(1, board.shape[0]):
        if x + i < board.shape[0] and y - i >= 0:
            if board[x + i, y - i] == '':
                disp.append((x + i, y - i))
            if board[x + i, y - i] != '' and board[x + i, y - i][-1] == color:
                break
            if board[x + i, y - i] != '' and board[x + i, y - i][-1] != color:
                disp.append((x + i, y - i))
                break

    #  \ haut
    for i in range(1, board.shape[0]):
        if x + i < board.shape[0] and y + i < board.shape[0]:
            if board[x + i, y + i] == '':
                disp.append((x + i, y + i))
            if board[x + i, y + i] != '' and board[x + i, y + i][-1] == color:
                break
            if board[x + i, y + i] != '' and board[x + i, y + i][-1] != color:
                disp.append((x + i, y + i))
                break

    #  \ bas
    for i in range(1, board.shape[0]):
        if x - i >= 0 and y - i >= 0:
            if board[x - i, y - i] == '':
                disp.append((x - i, y - i))
            if board[x - i, y - i] != '' and board[x - i, y - i][-1] == color:
                break
            if board[x - i, y - i] != '' and board[x - i, y - i][-1] != color:
                disp.append((x - i, y - i))
                break

    return disp


def getKingDisplacement(board, pos: tuple, color):
    x = pos[0]
    y = pos[1]
    disp = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + i >= board.shape[0] or y + j >= board.shape[1]:
                continue
            elif (x >= 0 and y >= 0) and (x < board.shape[0] and y < board.shape[1]) and (
                    board[x + i, y + j] == '' or board[x + i, y + j][1] != color):
                if x + i >= 0 and y + j >= 0 and x + i <= board.shape[0] and y + j <= board.shape[1]:
                    disp.append((x + i, y + j))
    return disp


def getKnightDisplacement(board, pos: tuple, color):
    x = pos[0]
    y = pos[1]
    disp = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i) + abs(j) == 3 and abs(abs(i) - abs(j)) == 1 and (
                    0 <= x + i <= board.shape[0] and 0 <= y + j <= board.shape[1]):
                if (x + i >= 0 and y + j >= 0 and x + i < board.shape[0] and y + j < board.shape[1]) and (
                        board[x + i, y + j] == '' or board[x + i, y + j][1] != color):
                    disp.append((x + i, y + j))

    return disp


def getAllDisplacement(player_sequence, board):
    color = player_sequence[1]

    disp = []  # tuple  :  [ (xPion, yPion), [Displacement] , ... ]

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x, y] == "r" + color:  # r
                possibleDisp = getRookDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "p" + color:  # r
                possibleDisp = getPawnDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "q" + color:  # r
                possibleDisp = getQueenDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "b" + color:  # r
                possibleDisp = getBishopDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "k" + color:  # r
                possibleDisp = getKingDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "n" + color:  # r
                possibleDisp = getKnightDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))

    return disp


piece = {"k": 1000, "q": 50, "b": 10, "n": 10, "r": 10, "p": 1}

memoization = {}
branches = []

def evaluatePath1Level(board, player_sequence, startX, startY, endX, endY, pond, baseColor, level, maxLevel):
    color = player_sequence[1]
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ " + level.__str__() + " " + color + " / " + baseColor)
    # print(player_sequence)

    branches.append("1")

    if board[endX, endY] != "":
        if board[endX, endY][-1] != color:
            if baseColor == color:
                pond += piece[board[endX, endY][0]]

                # Stop si le roi adverse peut être éliminé
                if board[endX, endY][0] == "k":
                    return pond

            else:
                pond -= piece[board[endX, endY][0]]

                # Stop si notre roi peut être éliminé
                if board[endX, endY][0] == "k":
                    return pond

    level -= 1

    """
    print(len(memoization))
    if len(memoization) > 0 and memoization.__contains__((str(board), level)): # , startX, startY, endX, endY
        print("MEMOIZATION")
        print(str(board))
        return memoization[(str(board), level)] #, startX, startY, endX, endY)]  # pond +
    """

    if level > 0:
        newBoard = nextBoardWithRotation(board, (startX, startY), (endX, endY))
        nextPlayerSequence = player_sequence[3:6] + player_sequence[0:3]
        disp = getAllDisplacement(nextPlayerSequence, newBoard)

        scores = []

        # """ memoization
        if MEMOIZATION:
            memBoard = newBoard.data.tobytes()
            #memDisp = (disp)

            if len(memoization) > 0 and memoization.__contains__((memBoard, level)): # memDisp
                pond += memoization[(memBoard, level)] # memDisp
                disp.clear()
        # """

        if len(disp) > 0:

            for i in disp:

                x = i[0][0]
                y = i[0][1]

                for d in i[1]:
                    # Evaluate the ponderation of the path
                    scores.append(
                        evaluatePath1Level(newBoard, nextPlayerSequence, x, y, d[0], d[1], 0, baseColor, level,
                                           maxLevel))

            # print(scores.__str__() + " " + level.__str__() + " " + nextPlayerSequence[1] + " / " + baseColor + " / " + color)

            if baseColor == nextPlayerSequence[1]:
                pond += max(scores)
                #memoization[(str(board), level)] = pond # max(scores)   , startX, startY, endX, endY
                if MEMOIZATION:
                    memoization[(memBoard, level)] = max(scores) # memDisp
            else:
                pond += min(scores)
                #memoization[(str(board), level)] = pond # min(scores)    , startX, startY, endX, endY
                if MEMOIZATION:
                    memoization[(memBoard, level)] = min(scores)  # memDisp

    # print(pond)
    return pond


LEVEL: int = 4
MEMOIZATION: bool = True

def siedel_bot(player_sequence, board, time_budget, **kwargs):
    print("__________________________________________________________________________________________________________")

    t = time.process_time()

    printBoard(board)
    print("")

    disp = getAllDisplacement(player_sequence, board)
    color = player_sequence[1]

    dispPond = []  # (startX, startY, endX, endY, pond)

    memoization.clear()

    for i in disp:

        x = i[0][0]
        y = i[0][1]

        for d in i[1]:
            # Evaluate the ponderation of the path
            # print("------------------------------------------------------------------------------------------------" + x.__str__(), y, d[0], d[1])
            dispPond.append(
                (x, y, d[0], d[1], evaluatePath1Level(board, player_sequence, x, y, d[0], d[1], 0, color, LEVEL, LEVEL)))

    for i in dispPond:
        print(i)

    print("Possible displacement : ")

    # for i in disp:
    # print(i)
    # printBoardWithDisplacement(board, i, color)

    # Prendre les déplacements avec les plus hautes pondérations
    lastDisp = []
    lastDisp.append(dispPond[0])
    for i in range(1, len(dispPond)):

        if dispPond[i][4] > lastDisp[0][4]:
            lastDisp.clear()
            lastDisp.append(dispPond[i])
        elif dispPond[i][4] == lastDisp[0][4]:
            lastDisp.append(dispPond[i])

    print()
    print("ELAPSED TIME : " + (time.process_time() - t).__str__())
    print("BRANCH       : " + (len(branches)).__str__())
    print("MAX LEVEL    : " + LEVEL.__str__())
    print("MEMOIZATION  : " + (len(memoization)).__str__())
    print()

    if len(lastDisp) == 1:
        return (lastDisp[0][0], lastDisp[0][1]), (lastDisp[0][2], lastDisp[0][3])

    r = Random()
    n = r.randint(0, len(lastDisp) - 1)
    return (lastDisp[n][0], lastDisp[n][1]), (lastDisp[n][2], lastDisp[n][3])

    time.sleep(5)
    return (0, 0), (0, 0)


#   Example how to register the function
register_chess_bot("SiedelSystem", siedel_bot)
register_chess_bot("PawnMover", chess_bot)
register_chess_bot("TowerMover", chess_bot_tower)

"""

0w01b2
--,--,--,qw,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,pw
rb,--,--,--,--,--,pb,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,kb,--,--,--,--

--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
pb,--,--,qw,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,rb,--,rb,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--


--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,pw,--,--,--,--,--,--
--,--,--,--,--,--,--,--
kb,bw,kw,--,--,--,--,--
--,--,--,--,--,--,--,--


--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,bw,--,pw,kw
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,kb

--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,kw,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,pw,--
--,--,--,--,--,kb,--,bb

--,--,--,kw,--,--,--,rb
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,kb,--,--,--,qw,--
--,--,--,--,--,--,--,--

"""
