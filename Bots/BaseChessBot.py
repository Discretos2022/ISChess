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


# Print le plateau
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

# Print le plateau avec une modélisation d'un déplacement
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

# Retourne le futur plateau
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

# Retourne le futur plateau avec la rotation
def nextBoardWithRotation(board, start, end):
    result = board.copy()

    x: int = start[0]
    y: int = start[1]
    p = result[x, y]

    if p[0] == "p" and x == 7:
        p = "q" + p[1]

    result[x, y] = ""

    x: int = end[0]
    y: int = end[1]
    result[x][y] = p

    newBoard = np.rot90(result, 2)
    # printBoard(newBoard)

    return newBoard


######### DEPLACEMENT DES PIECES #########
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
            if board[x, y] == "p" + color:  # p
                possibleDisp = getPawnDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "q" + color:  # q
                possibleDisp = getQueenDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "b" + color:  # b
                possibleDisp = getBishopDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "k" + color:  # k
                possibleDisp = getKingDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))
            if board[x, y] == "n" + color:  # n
                possibleDisp = getKnightDisplacement(board, (x, y), color)
                if len(possibleDisp) != 0:
                    disp.append(((x, y), possibleDisp))

    return disp


# Evalue récursivement et retourne le score final du déplacement
def evaluatePath2_0(board, player_sequence, startX, startY, endX, endY, baseColor, level, maxLevel, scoreBefore, opt = 0):
    branches.append("1")

    color = player_sequence[1]

    MIN = False
    MAX = False
    if color == baseColor:
        MIN = True
    else:
        MAX = True

    score = 0

    if board[endX, endY] != "":
        if board[endX, endY][-1] != color:
            if baseColor == color:
                score += piece[board[endX, endY][0]] * level

                # Stop si le roi adverse peut être éliminé
                if board[endX, endY][0] == "k":
                    if level == maxLevel:
                        return score * 1000
                    else:
                        return score

            else:
                score -= piece[board[endX, endY][0]] * level

                # Stop si notre roi peut être éliminé
                if board[endX, endY][0] == "k":
                    if level == maxLevel:
                        return score * 1000
                    else:
                        return score

    if level > 1:
        newBoard = nextBoardWithRotation(board, (startX, startY), (endX, endY))
        nextPlayerSequence = player_sequence[3:6] + player_sequence[0:3]
        disp = getAllDisplacement(nextPlayerSequence, newBoard)

        # """ memoization
        if MEMOIZATION:
            memBoard = newBoard.data.tobytes()

            if len(memoization) > 0 and memoization.__contains__((memBoard, level)):
                return score + memoization[(memBoard, level)]
        # """

        scores = []

        if len(disp) > 0:
            for i in disp:
                x = i[0][0]
                y = i[0][1]
                for d in i[1]:
                    # Evaluate the score of the path       if min < max -> END

                    if ALPHABETA:
                        val = 0
                        if MIN:

                            val = 0
                            if len(scores) > 0:
                                val = evaluatePath2_0(newBoard, nextPlayerSequence, x, y, d[0], d[1], baseColor, level-1, maxLevel, score + scoreBefore, max(scores))

                                minVal = min(scores)
                                if minVal < opt:
                                    return score + minVal
                            else:
                                val = evaluatePath2_0(newBoard, nextPlayerSequence, x, y, d[0], d[1], baseColor, level-1, maxLevel, score + scoreBefore)

                            scores.append(val)

                        if MAX:

                            val = 0
                            if len(scores) > 0:
                                val = evaluatePath2_0(newBoard, nextPlayerSequence, x, y, d[0], d[1], baseColor, level-1, maxLevel, score + scoreBefore, min(scores))

                                maxVal = max(scores)
                                if maxVal > opt:
                                    return score + maxVal
                            else:
                                val = evaluatePath2_0(newBoard, nextPlayerSequence, x, y, d[0], d[1], baseColor, level-1, maxLevel, score + scoreBefore)

                            scores.append(val)
                    else:
                        val = evaluatePath2_0(newBoard, nextPlayerSequence, x, y, d[0], d[1], baseColor, level - 1,
                                              maxLevel, score + scoreBefore)
                        scores.append(val)

            if len(scores) > 0:
                if baseColor != color:
                    maxVal = max(scores)
                    if MEMOIZATION: memoization[(memBoard, level)] = maxVal
                    return maxVal
                else:
                    minVal = min(scores)
                    if MEMOIZATION: memoization[(memBoard, level)] = minVal
                    return minVal

    return score + scoreBefore

# CONSTANT
LEVEL: int = 4
MEMOIZATION: bool = True
ALPHABETA: bool = True

# Score de chaque pièce
piece = {"k": 10000, "q": 500, "b": 100, "n": 100, "r": 200, "p": 10}

# Mémoire pour la memoization
memoization = {}

# Espèce de compteur pour le nombre de branche
branches = []

# Fonction d'entrée du bot
def ISChess_bot(player_sequence, board, time_budget, **kwargs):
    print("__________________________________________________________________________________________________________")

    t = time.process_time()

    printBoard(board)
    print("")

    disp = getAllDisplacement(player_sequence, board)
    color = player_sequence[1]

    dispPond = []  # (startX, startY, endX, endY, pond)

    memoization.clear()
    branches.clear()

    for i in disp:

        x = i[0][0]
        y = i[0][1]

        for d in i[1]:
            # Evaluate the score of the path
            dispPond.append((x, y, d[0], d[1], evaluatePath2_0(board, player_sequence, x, y, d[0], d[1], color, LEVEL, LEVEL, 0)))

            if time.process_time() - t > 1.8:
                break

        if time.process_time() - t > 1.8:
            break


    print("Possible displacement : ")

    for i in dispPond:
        print(i)

    # Prendre les déplacements avec les plus hautes pondérations
    lastDisp = []
    lastDisp.append(dispPond[0])
    for i in range(1, len(dispPond)):

        if dispPond[i][4] > lastDisp[0][4]:
            lastDisp.clear()
            lastDisp.append(dispPond[i])
        elif dispPond[i][4] == lastDisp[0][4]:
            lastDisp.append(dispPond[i])

    # Printer des statistiques
    print()
    print("ELAPSED TIME : " + (time.process_time() - t).__str__())
    print("BRANCH       : " + (len(branches)).__str__())
    print("MAX LEVEL    : " + LEVEL.__str__())
    print("MEMOIZATION  : " + (len(memoization)).__str__())
    print("DISPLACEMENT : " + len(dispPond).__str__())
    print()

    if len(lastDisp) == 1:
        return (lastDisp[0][0], lastDisp[0][1]), (lastDisp[0][2], lastDisp[0][3])

    # Prendre aléatoirement un des meilleurs déplacements si il y en a plusieurs
    r = Random()
    n = r.randint(0, len(lastDisp) - 1)
    return (lastDisp[n][0], lastDisp[n][1]), (lastDisp[n][2], lastDisp[n][3])

    # Si il n'y a pas de bon coup (n'arrive normalement jamais)
    time.sleep(5)
    return (0, 0), (0, 0)


#   Example how to register the function
register_chess_bot("SV", ISChess_bot)