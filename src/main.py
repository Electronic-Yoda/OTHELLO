import tkinter as tk
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

    
    # Make UI objects point (have reference) to each other
    menu_ui.game_ui = game_ui
    game_ui.menu_ui = menu_ui

    # The relationship between classes is as follows:
        # MenuUI <-'reference'-> GameUI -'has'-> GameLogic 
        #                           -'has'-> GameAI -'has or inherites from'-> GameLogic


    # Draw menu 
    menu_ui.drawAndReact() 
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()