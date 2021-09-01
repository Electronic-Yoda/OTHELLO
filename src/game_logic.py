
from typing import Tuple, Union
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
    def __init__(self, placementInfoDict) -> None:
        self.legal = placementInfoDict['legal']
        self.tileList = placementInfoDict['tileList']


class GameStatus:
    # static variables
    BOARDFULL = "board full"
    NOMOVES = "no moves"
    def __init__(self, gameOver = False, gameOverReason = None, colorCount = {}, thisTurnColor = "") -> None:
        self.gameOver = gameOver
        self.gameOverReason = gameOverReason
        self.colorCount = colorCount
        self.thisTurnColor = thisTurnColor

        
class GameLogic:
    def __init__(self) -> None:
        self.board = [[TileStatus() for j in range(boardSize)] for i in range(boardSize)]
        self.thisTurnColor = ""
        self.colorInfo = {}
        self.mode = ""
        self.highlightOn = False
    

    def boardSetUp(self, mode, highlightOn) -> GameStatus:
        self.thisTurnColor = 'B'
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].setColor("U")
        
        self.board[3][3].setColor("B") 
        self.board[4][3].setColor("W")
        self.board[3][4].setColor("W") 
        self.board[4][4].setColor("B")

        self.mode = mode # Note mode = 'PVP' or 'PVC'
        self.highlightOn = highlightOn
        if self.highlightOn:
            self.setBoardHighlights()

        colorInfo = self.countColors(self.board)
        return GameStatus(gameOver=False, gameOverReason=None, colorCount=colorInfo)


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
                self.board[i][j].highlight = False
                if tileInfo.legal == True:
                    self.board[i][j].highlight = True

    def removeBoardHighlights(self):
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].highlight = False
                

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


    def newBoard(self, board, i, j, tileList, color) -> list:
        # Place the disk on the tile that is clicked on
        board[i][j].setColor(color)

        # Flip the disks that can be flipped 
        for loc in tileList:
            # Note loc[0] = i, loc[1] = j
            board[loc[0]][loc[1]].setColor(color)
        return board
        

    def actToTileClicked(self, i, j) -> Tuple[bool, GameStatus]: # moveMade, GameStatus
        curPlacementInfo = self.getPlacementInfo(self.board, i, j, self.thisTurnColor)
        game_status = GameStatus(gameOver=False, gameOverReason = None, colorCount={}, thisTurnColor=self.thisTurnColor)

        if curPlacementInfo.legal == False:
            moveMade = False
            return moveMade, game_status
        
        # At this point, curPlacementInfo.legal == True
        # 1. Update the board
        self.board = self.newBoard(self.board, i, j, curPlacementInfo.tileList, self.thisTurnColor)
        moveMade = True

        # 2. Check next move and update game_status
        game_status = self.checkNextMove(self.board, self.oppColor(self.thisTurnColor), self.highlightOn)
        
        # 3. If game not over, Set turn color to the color for the next turn
                # Note: could be either color, because if enemy cannot make move,
                # the current player must continue playing if they can make a move
        if not game_status.gameOver:
            self.thisTurnColor = game_status.thisTurnColor
        return moveMade, game_status
            

    def checkNextMove(self, board, turnColor, highlightOn) -> GameStatus:
        # 1. Need to check if gameOver 
            # two possibilities for gameOver:
                # board full (check using color count)
                # if no more moves can be made even if the turn is passed to original player
        # 2. set highlights
        # 3. return game_status
        game_status = GameStatus(gameOver=False, gameOverReason = None, colorCount={}, thisTurnColor=turnColor)
        colorInfo = {'black': 0, 'white': 0, 'empty': 0}
        canMakeMove = False
        for i in range(boardSize):
            for j in range(boardSize):
                if (board[i][j].getColor() == 'B'):
                    colorInfo['black'] += 1
                elif (board[i][j].getColor() == 'W'):
                    colorInfo['white'] += 1 
                elif (board[i][j].getColor() == 'U'):
                    colorInfo['empty'] += 1 

                placement = self.getPlacementInfo(self.board, i, j, turnColor)
                if highlightOn: 
                    board[i][j].highlight = False # Need to set to False first
                if placement.legal == True:
                    canMakeMove = True
                    board[i][j].highlight = True if highlightOn else False

        game_status.colorCount = colorInfo
        if colorInfo['empty'] == 0: # board full
            game_status.gameOver = True
            game_status.gameOverReason = game_status.BOARDFULL
            return game_status
        if canMakeMove == False:
            # nextPlacement = self.getPlacementInfo(self.board, i, j, self.oppColor(turnColor))
            nextIsLegal = False
            for i in range(boardSize):
                for j in range(boardSize):
                    nextPlacement = self.getPlacementInfo(self.board, i, j, self.oppColor(turnColor))
                    if nextPlacement.legal:
                        nextIsLegal = True
            if nextIsLegal == False:
                game_status.gameOver = True
                game_status.gameOverReason = game_status.NOMOVES
                return game_status
            else: # nextIsLegal == True
                # pass turn to original player
                # since this player cannot make move but original can
                game_status.thisTurnColor = self.oppColor(turnColor)
                return game_status
        else: # this turn's player can make move
            return game_status



        
        



