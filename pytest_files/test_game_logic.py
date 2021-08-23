

import sys, os
import pandas
import pytest

# The following allows this file to see the src directory
filePath = __file__
dirPath = os.path.dirname(filePath)
srcPath = os.path.dirname(dirPath) + '\\src'
sys.path.insert(1, srcPath) 
print("This is the src path:", srcPath) 
from game_logic import *


# Create a gameLogicTest class that inherites from GameLogic
class gameLogicTest(GameLogic):
    def __init__(self) -> None:
        # Parent constructor
        super().__init__()

    def importBoardFromExcel(self):
        df = pandas.read_excel(dirPath + '\\board.xlsx')
        # print(df)
        # print(df.iloc[4][4])
        # print(df.iloc[4])

        
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j].color = df.iloc[i][j]
                print(self.board[i][j].color, end='')
            print()
        



def test_legality():
    test = gameLogicTest()
    test.importBoardFromExcel()
    
    print(test.getPlacementInfoDict(test.board, 0, 0, 'W'))
    print(test.countColors(test.board))
    # assert... ==

test_legality()


# Example test
from add_test import *

def test_add():
    assert add(4, 28) == 32