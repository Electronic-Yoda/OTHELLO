import pygame
import tkinter as tk
import math
from game_logic import*
from gui import *

# -------- Main Program -----------
def main():
    # print("this file is located at:" + __file__)
    # Create an images object storing images from the subdirectory
    images = Images()

    # create UI objects
    menu_ui = MenuUI(images)
    game_ui = GameUI(images)

    # Create game logic object
    game_logic = GameLogic()

    # Make objects point to each other
    # menu_ui <-> game_ui -> game_logic -> game_ai
    menu_ui.game_ui = game_ui
    game_ui.menu_ui = menu_ui
    game_ui.game_logic = game_logic
    

    # Draw menu 
    menu_ui.drawAndReact() 
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()