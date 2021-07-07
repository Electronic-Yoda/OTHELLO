import pygame
import tkinter as tk
import math
from global_setup import *




def menuLoop():
    global menuOn, programOn, GameTitle
    
    '''screen.fill(BLACK)
    screen.blit(GameTitle, [120, 0])
    pygame.display.flip() '''
    while programOn and menuOn:
        pass






def drawMenu():
    label = tk.Label(text="Python rocks!")
    label.pack()



# -------- Main Program -----------
def main():

    
    global programOn, menuOn
    programOn = True
    menuOn = True

    menu.drawMenu()
    
    
    root.mainloop()
    '''
    while programOn:
       if menuOn:
           menuLoop()
    '''       


    # Close the window and quit.
    # pygame.quit()

if __name__ == "__main__":
    main()