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

    if x < board.shape[0] and board[x + 1, y] == '':
        disp.append((x + 1, y))
    if x < board.shape[0] and y > 0 and board[x + 1, y - 1] != '' and board[x + 1, y - 1][1] != color:
        disp.append((x + 1, y - 1))
    if x < board.shape[0] and y < board.shape[1] - 1 and board[x + 1, y + 1] != '' and board[x + 1, y + 1][1] != color:
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
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if x+i>=board.shape[0] or y+j>=board.shape[1]:
                continue
            elif (x >= 0 and y >= 0) and (x < board.shape[0] and y < board.shape[1]) and (board[x + i, y + j] == '' or board[x + i, y + j][1] != color):
                if x+i>=0 and y+j>=0 and x+i<=board.shape[0] and y+j<=board.shape[1]:
                    disp.append((x + i, y + j))
    return disp


def getKnightDisplacement(board, pos: tuple, color):
    x = pos[0]
    y = pos[1]
    disp = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i)+abs(j) == 3 and abs(abs(i)-abs(j)) == 1 and (0 <= x+i <= board.shape[0] and 0 <= y+j <= board.shape[1]):
                if (x+i>=0 and y+j>=0 and x+i<=board.shape[0] and y+j<=board.shape[1]) and (board[x + i, y + j] == '' or board[x + i, y + j][1] != color):
                    disp.append((x + i, y + j))
    return disp


def siedel_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]

    print(
        "____________________________________________________________________________________________________________")

    printBoard(board)
    print("")

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

    # printBoard(nextBoard(board, (1, 0), (2, 0)))
    # print("")

    print("Possible displacement : ")

    for i in disp:
        print(i)
        printBoardWithDisplacement(board, i, color)

    ## RETOUR ALEATOIRE

    r = Random()
    n = 0

    if len(disp) > 0:
        n2 = r.randint(0, len(disp) - 1)
        if len(disp[n2][1]) != 0: n = r.randint(0, len(disp[n2][1]) - 1)
        if len(disp[n2][1]) != 0: return (disp[n2][0]), (disp[n2][1][n][0], disp[n2][1][n][1])
        # if len(disp[0][1]) != 0: n = r.randint(0, len(disp[0][1]) - 1)
        # if len(disp[0][1]) != 0: return (disp[0][0]), (disp[0][1][n][0], disp[0][1][n][1])

    time.sleep(5)
    return (0, 0), (0, 0)


#   Example how to register the function
register_chess_bot("SiedelSystem", siedel_bot)
register_chess_bot("PawnMover", chess_bot)
register_chess_bot("TowerMover", chess_bot_tower)

"""

0w01b2
--,--,--,--,--,--,--,--
--,pw,--,--,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,rw,--,--,--,--
--,--,--,--,--,--,--,--
--,--,--,--,--,--,--,--
pb,--,--,--,--,--,rw,--
--,--,--,--,--,--,--,--

"""
