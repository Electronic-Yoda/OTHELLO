
from globals import *

class TileStatus:
    def __init__(self) -> None:
        self.color = ""
        self.isLegal = False
        self.highlight = False

    def getColor(self) -> str:
        return self.color

    def setColor(self, color): 
        self.color = color


class PlacementInfo:
    def __init__(self, infoDict) -> None:
        self.legal = infoDict['legal']
        self.tileList = infoDict['tileList']
        

class GameLogic:
    def __init__(self) -> None:
        self.board = [[TileStatus() for j in range(boardSize)] for i in range(boardSize)]
        self.thisTurnColor = str()
        self.colorInfo = dict()
    
    def boardSetUp(self):
        self.thisTurnColor = 'B'
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].setColor("U")
        
        self.board[3][3].setColor("B") 
        self.board[4][3].setColor("W")
        self.board[3][4].setColor("W") 
        self.board[4][4].setColor("B")

        self.colorInfo = self.countColors(self.board)

    def getPlacementInfo(self, board, i, j, color) -> PlacementInfo:
        infoDict = self.getPlacementInfoDict(board, i, j, color)
        return PlacementInfo(infoDict)
        

    def getPlacementInfoDict(self, board, i, j, color) -> dict:

        # Note the tileList index shall store a list of (i,j) pairs 
        # of all the tiles that can be flipped
        info = dict({'legal': False, 'tileList': [], 'color': color})
        
        if board[i][j].color != "U":
            info['legal'] = False
            return info
        
        # Loop through each direction and get each direction's info
        for delta_i in range(-1,2):
            for delta_j in range(-1, 2):
                if not (delta_i == 0 and delta_j == 0):
                    # Call directionInfo
                    dirInfo = self.directionInfo(board, i, j, delta_i, delta_j, color)
                    if dirInfo['legal'] == True:
                        info['legal'] = True
                        # add tileList into existing list
                        info['tileList'] = info['tileList'] + dirInfo['tileList']
        return info


                
    def directionInfo(self, board, i, j, delta_i, delta_j, color) -> dict:
        dirInfo = dict({'legal': False, 'tileList': []})

        # Check if first color beside is an opposite color
        cur_i = i + delta_i
        cur_j = j + delta_j
        if not self.inBounds(cur_i, cur_j):
            dirInfo['legal'] = False
            return dirInfo
        if board[cur_i][cur_j].getColor() != self.oppColor(color):
            dirInfo['legal'] = False
            return dirInfo
        
        # if opposite color, check the rest of the line
        tileList = []
        for a in range(boardSize):
            if not self.inBounds(cur_i, cur_j):
                dirInfo['legal'] = False
                return dirInfo
            if board[cur_i][cur_j].getColor() == 'U':
                dirInfo['legal'] = False
                return dirInfo
            if board[cur_i][cur_j].getColor() == color:
                dirInfo['legal'] = True
                dirInfo['tileList'] = tileList
                return dirInfo
            
            tileList.append((cur_i, cur_j))
            cur_i += delta_i  
            cur_j += delta_j
            
                
    def inBounds(self, i, j) -> bool:
        if 0 <= i and i < boardSize and 0 <= j and j < boardSize:
            return True
        else:
            return False

    def oppColor(self, color) -> str:
        if color == 'B':
            return 'W'
        elif color == 'W':
            return 'B'
        else:
            print("oppColor Error")

    def setBoardHighlights(self):
        for i in range(boardSize):
            for j in range(boardSize):
                tileInfo = self.getPlacementInfo(self.board, i, j, self.thisTurnColor)
                if tileInfo.legal == True:
                    self.board[i][j].highlight = True
            
    def countColors(self, board) -> dict:
        colorInfo = dict({'black': 0, 'white': 0, 'empty': 0})
        for i in range(boardSize):
            for j in range(boardSize):
                if (board[i][j].getColor() == 'B'):
                    colorInfo['black'] += 1
                elif (board[i][j].getColor() == 'W'):
                    colorInfo['white'] += 1 
                elif (board[i][j].getColor() == 'U'):
                    colorInfo['empty'] += 1 
        if (colorInfo['black'] + colorInfo['white'] + colorInfo['empty']) != boardSize*boardSize:
            print("colorInfo function error: numbers don't add up")
        return colorInfo
    
    def ActToTileClicked(self, i, j):
        info = self.getPlacementInfo(self.board, i, j, self.thisTurnColor)
        if info.legal == False:
            return
        

    def actToMoveMade(self):
        pass # need to check if game finished, if enemy can't make move, etc

