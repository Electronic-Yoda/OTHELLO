import pygame
import tkinter as tk
import math
from UI import *


# -------- Main Program -----------
def main():

    # Create an images object storing images from the subdirectory
    images = Images()
    # create UI objects
    menu_ui = MenuUI(images)
    game_ui = GameUI(images)

    # Draw menu and pass in game_ui so that the menu buttons, when clicked, will call game_ui methods
    menu_ui.drawAndReact(game_ui) 
    
    
    root.mainloop()
    



if __name__ == "__main__":
    main()