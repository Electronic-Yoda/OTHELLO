import pygame
import tkinter as tk
import math
from GUI import *


# -------- Main Program -----------
def main():

    # Create an images object storing images from the subdirectory
    images = Images()
    # create UI objects
    menu_ui = MenuUI(images)
    game_ui = GameUI(images)

    # Make objects point to each other
    menu_ui.game_ui = game_ui
    game_ui.menu_ui = menu_ui
    

    # Draw menu 
    menu_ui.drawAndReact() 
    
    
    root.mainloop()
    



if __name__ == "__main__":
    main()