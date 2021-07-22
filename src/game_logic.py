
from gui import *

class TileStatus:
    def __init__(self) -> None:
        self.color = ""
        self.isLegal = False
    

class GameLogic:
    def __init__(self) -> None:
        self.board = [[TileStatus() for j in range(boardSize)] for i in range(boardSize)]
        
    
    def boardSetUp(self):
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].color = "U"
        
        self.board[3][3].color = "B"
        self.board[4][3].color = "W"
        self.board[3][4].color = "W"
        self.board[4][4].color = "B"

