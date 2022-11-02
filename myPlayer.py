# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

from time import time
import Goban 
from random import choice, shuffle
from playerInterface import *

#---------- Heuristics ------------
def opponementColor(b, color):
    """
    This function returns the opposite color of the value color.
    """
    if color == b._BLACK:
        return b._WHITE
    return b._BLACK

def stoneDiff(b,color):
    """
    A simple evaluation function that returns the difference of stone's number in board `b` depending on the color `color`.
    """
    if color == b._BLACK:
        return b.diff_stones_board()
    return - b.diff_stones_board()

def captureDiff(b, color):
    """
    A simple evaluation function that return the difference of captured stones in the board `b` depending on the color `color`
    """
    if color == b._BLACK:
        return b._capturedWHITE - b._capturedBLACK
    return b._capturedBLACK - b._capturedWHITE

def surround(b, color):
    """
    This is our main evaluation funtion, It gives the player the ability to surrond the enemy's stones in order to take them.
    """
    score = 0
    # Our opposite color, it is used to know who to surrond.
    otherColor = opponementColor(b, color)
    for i in range(b.__len__()): # Iterate on every place in the board
        item = b.__getitem__(i) # Get the item of the place indexed by `i`
        if item == color: # In case the place is occupied by us.
            score += 45
            neighbors = 0
            for j in b._get_neighbors(i): # Look at the neighbors of our stone
                if b.__getitem__(j) == otherColor:
                    neighbors += 1 # Number of enemy neighbors
            if neighbors == 2: # if 2 we are in danger but not losing 
                score -= 20
            elif neighbors == 3: # if 3 we are in danger
                score -= 50
        elif item == otherColor:  # In case the place is occupied by the enemy.
            score -= 45
            for j in b._get_neighbors(i):# Look at the neighbors of the enemy's stone
                neighbors = 0
                if b.__getitem__(j) == color:
                    neighbors += 1 # Number ally neighbors
                    score += 10
                elif b.__getitem__(j) == otherColor:
                    score -= 10 # decrease the score id the enemy has a lot of stones next to each other
            if neighbors == 2: # if 2 we have a good opportunity
                score += 20
            elif neighbors == 3: # if 3 we are great
                score += 50
            elif neighbors == 4: #if 4 we are having a stone
                score += 100
    return score


def playMiddle(b,color):
    """
    This evaluation function tries to make the player avoid the edges
    """
    score = 0
    for i in range(b.__len__()):
        item = b.__getitem__(i)
        if (i + 1) % b._BOARDSIZE == 0 or i % b._BOARDSIZE == 0 or i <= b._BOARDSIZE or i > (b._BOARDSIZE**2) - b._BOARDSIZE:
            if item == color:
                score -= 5
            elif item == opponementColor(b, color):
                score += 5
    return score


def heuristic(b, color):
    """
    our heuristic is the sum of the 4 evaluation functions above.
    """
    return playMiddle(b,color) + surround(b,color) + stoneDiff(b,color) + captureDiff(b, color)

#-----------  MiniMax  ------------

def MiniMax(isMax, b, alpha, beta, color, depth=3):
    if b.is_game_over():
        res = b.result()
        if res == "1-0":
            return 1000000000
        elif res == "0-1":
            return - 1000000000
        else:
            return 0

    elif depth == 0:
        return heuristic(b, color)

    if isMax:
        bestValue = - 1000000000
        for move in b.generate_legal_moves():
            b.push(move)
            bestValue = max(bestValue, MiniMax(False, b, alpha, beta, color, depth - 1))
            b.pop()
        return bestValue
    else:
        bestValue = 1000000000
        for move in b.generate_legal_moves():
            b.push(move)
            bestValue = max(bestValue, MiniMax(True, b, alpha, beta, opponementColor(b, color), depth - 1))
            b.pop()
        return bestValue

def MiniMaxPlay(b, color, depth=3):
    """
    Returns the best move using minimax algorithm and the heuristic function.
    """
    bestMove = None
    bestVal = - 1000000000
    for move in b.generate_legal_moves():
        b.push(move)
        if depth == 0:
            eval = heuristic(b, color)
        else:
            eval = MiniMax(True, b, -1000000000, 1000000000, color, depth - 1)
        b.pop()
        if eval > bestVal:
            bestVal = eval
            bestMove = move
    if bestMove == None:
        return -1
    return bestMove

#------------Alpha Beta------------

def AlphaBeta(isMax, b, alpha, beta, color, depth=3):
    if b.is_game_over():
        res = b.result()
        if res == "1-0":
            return 1000000000
        elif res == "0-1":
            return - 1000000000
        else:
            return 0

    elif depth == 0:
        return heuristic(b, color)

    if isMax:
        bestValue = - 1000000000
        for move in b.generate_legal_moves():
            b.push(move)
            bestValue = max(bestValue, AlphaBeta(False, b, alpha, beta, color, depth - 1))
            b.pop()
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
        return bestValue
    else:
        bestValue = 1000000000
        for move in b.generate_legal_moves():
            b.push(move)
            bestValue = min(bestValue, AlphaBeta(True, b, alpha, beta, opponementColor(b, color), depth - 1))
            b.pop()
            beta = min(alpha, bestValue)
            if beta <= alpha:
                break
        return bestValue

def AlphaBetaPlay(b, color, depth=3):
    """
    Returns the best move using alpha-beta algorithm and the heuristic function.
    """
    bestMove = None
    bestVal = - 1000000000
    legal_moves = b.generate_legal_moves()
    legal_moves.pop()
    shuffle(legal_moves)
    for move in legal_moves:
        b.push(move)
        if depth == 0:
            eval = heuristic(b, color)
        else:
            eval = AlphaBeta(True, b, -1000000000, 1000000000, color, depth - 1)
        b.pop()
        if eval > bestVal:
            bestVal = eval
            bestMove = move
    if bestMove == None:
        return -1
    return bestMove

def get_raw_data_go():
    ''' Returns the set of samples from the local file or download it if it does not exists'''
    import gzip
    import json

    with open("games_pro.json") as fz:
        data = json.loads(fz.read())
    return data

import numpy as np

def name_to_coord(s):
    assert s != "PASS"
    indexLetters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'J':8}
    col = indexLetters[s[0]]
    lin = int(s[1:]) - 1
    return col, lin

def coord_to_name(coord):
    indexLetters = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'J'}
    return indexLetters[coord[0]] + str(coord[1])

#----------- Player Class ------------

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        ## Les 'open_depth' premiers coups vont être joués avec la bibli d'ouverture et pas avec alpha beta
        self._open_depth = 8
        data = get_raw_data_go()
        self._openMoveFrequency = np.zeros((self._open_depth, 9, 9), dtype="int64")
        for d in data:
            for k in range(self._open_depth):
                lin, col = name_to_coord(d["moves"][k])
                self._openMoveFrequency[k][lin][col] += 1
        print(self._openMoveFrequency)
        self._depth = 1
        

    def getPlayerName(self):
        return "l7wat"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!

        # Pass if the moves are lower that 15. Their is no need to play more because it's risky
        if len(moves) <= 15:
            if (self._mycolor == self._board._BLACK):
                if (self._board._nbBLACK > self._board._nbWHITE):
                    return "PASS"
            else:
                if(self._board._nbWHITE > self._board._nbBLACK):
                    return "PASS"

        ## Bibliothèque d'ouverture 
        move = ""
        print("I will choose my move")
        # Play an opening move if the  the depth of the game is lower than open_depth
        if self._depth <= self._open_depth:
            move = self.getOpenMove(self._board)
        else: ## Else Apha beta
            move = AlphaBetaPlay(self._board, self._mycolor, 2)
        print(move)
        print("Chosen move", move)
        self._board.push(move)
        if move == -1:
            return "PASS"
        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        self._depth += 1
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def getOpenMove(self, board):
        moves = self._board.legal_moves()
        while (True):
            move = np.argmax(self._openMoveFrequency[self._depth - 1])
            if move in moves:
                return move
            else:
                self._openMoveFrequency[self._depth - 1][move // 9][move % 9] = 0
        

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._depth += 1
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)


    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



