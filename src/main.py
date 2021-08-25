import tkinter as tk
from game_logic import*
from gui import *

# -------- Main Program -----------
def main():
    # Create an images object storing images from the subdirectory
    images = Images()

    # create program objects
    menu_ui = MenuUI(images)
    game_ui = GameUI(images)
    game_logic = GameLogic()
    
    # Make program objects point (have reference) to each other
    menu_ui.game_ui = game_ui
    game_ui.menu_ui = menu_ui
    game_ui.game_logic = game_logic

    # The relationship between program components is as follows:
        # MenuUI <--> GameUI -----> GameLogic 
        #                --> GameAI -->
    # Draw menu 
    menu_ui.drawAndReact() 
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()