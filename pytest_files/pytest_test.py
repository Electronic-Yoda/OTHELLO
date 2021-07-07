

import sys, os

srcPath = os.path.abspath("src")
sys.path.insert(1, srcPath) 
print("This is the src path:", srcPath)

from add_test import *

def test_add():
    assert add(4, 28) == 32
    