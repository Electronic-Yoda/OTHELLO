
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
        self.thisTurnColor = 'Black'
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

        color = self.thisTurnColor
        info['color'] = color
        info['tileList'] = []
        
        if board[i][j].color != "U":
            info['legal'] = False
            return info
        
        # Loop through each direction and get each direction's info
        for delta_i in range(-1,2):
            for delta_j in range(-1, 2):
                if delta_i != 0 and delta_j != 0:
                    # Call directionInfo
                    dirInfo = self.directionInfo(i, j, delta_i, delta_j, color)
                    if dirInfo['legal'] == True:
                        info['legal'] = True
                        # Load tileList
                        tileList = dirInfo['tileList']
                        info['tileList'].append(tileList)
        return info


                        
    
    def directionInfo(self, i, j, delta_i, delta_j, color):
        board = self.board
        dirInfo = dict({'legal': None, 'tileList': None})

        # Check if first color beside is an opposite color
        cur_i = i + delta_i
        cur_j = j + delta_j
        if not self.inBounds(cur_i, cur_j):
            dirInfo['legal'] = False
            return dirInfo
        if board[cur_i][cur_j].color != self.oppColor(color):
            dirInfo['legal'] = False
            return dirInfo
        
        # if opposite color, check the rest of the line
        tileList = []
        for a in range(boardSize):
            if not self.inBounds(cur_i, cur_j):
                dirInfo['legal'] = False
                return dirInfo
            if board[cur_i][cur_j].color == 'U':
                dirInfo['legal'] = False
                return dirInfo

            tileList.append((cur_i, cur_j))
            if board[cur_i][cur_j].color == color:
                dirInfo['legal'] = True
                dirInfo['tileList'] = tileList
                return dirInfo
            cur_i += delta_i  
            cur_j += delta_j
            

                
    def inBounds(self, i, j) -> bool:
        if 0 <= i and i < boardSize and 0 <= j and j < boardSize:
            return True
        else:
            return False

    def oppColor(self, color):
        if color == 'B':
            return 'W'
        elif color == 'W':
            return 'B'
        else:
            print("oppColor Error")
