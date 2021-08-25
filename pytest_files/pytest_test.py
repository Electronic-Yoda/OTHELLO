

import sys, os


filePath = __file__
dirPath = os.path.dirname(filePath)
srcPath = os.path.dirname(dirPath) + '\\src'
sys.path.insert(1, srcPath) 

from add_test import *

def test_add():
    assert add(4, 28) == 32
    
