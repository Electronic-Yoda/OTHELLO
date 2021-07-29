
from typing import Dict
from gui import *

class TileStatus:
    def __init__(self) -> None:
        self.color = ""
        self.isLegal = False
    

class GameLogic:
    def __init__(self) -> None:
        self.board = [[TileStatus() for j in range(boardSize)] for i in range(boardSize)]
        self.thisTurnColor = None
    
    def boardSetUp(self):
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].color = "U"
        
        self.board[3][3].color = "B"
        self.board[4][3].color = "W"
        self.board[3][4].color = "W"
        self.board[4][4].color = "B"

    def getPlacementInfo(self, i, j, color) -> dict:
        board = self.board
        info = dict({'legal': None, 'tileList': None, 'color': None})
        
        if board[i][j].color != "U":
            info['legal'] = False
            return info
        
        # Loop through each direction
        for delta_i in range(-1,2):
            for delta_j in range(-1, 2):
                if delta_i != 0 and delta_j != 0:
                    pass
                

    
    def directionInfo(self, i, j, delta_i, delta_j, color):
        
        for i in range(boardSize):
            pass

    def inBounds(self, i, j) -> bool:
        if 0 <= i and i < boardSize and 0 <= j and j < boardSize:
            return True
        else:
            return False