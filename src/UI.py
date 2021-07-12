from tkinter.constants import ANCHOR, LEFT, RIGHT
import pygame
import math
import sys, os
import tkinter as tk
from PIL import Image
from PIL import ImageTk


PI = math.pi




reddish = '#6E4137'
yellowish = '#D1CFA6'
blueish = '#274098'
darkGreyish='#797D7F'
darkish = '#17202A'
greyish = '#A69E99'
windowWidth = 800
windowHeight = 800
root = tk.Tk()
root.title('OTHELLO')
root.geometry(str(windowWidth) + "x" + str(windowHeight))
root['background'] = "black"

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

class Images():
    def __init__(self) -> None:
        tempFilePath = os.path.abspath("Othello_AI")
        # print("This is the file path:", tempFilePath)

        OthelloAIPath = os.path.dirname(tempFilePath)
        # print("This is the parent path:", OthelloAIPath)

        picsPath = OthelloAIPath + "\src\pics"
        # print("This is the pics path:", picsPath)
        picsPath = picsPath.replace("\\", "/") 

        self.woodImage = ImageTk.PhotoImage(Image.open(picsPath + "/woodPaint5.jpg"))
        self.woodImage2 = ImageTk.PhotoImage(Image.open(picsPath + "/wood2-3.jpg"))

class MenuUI():
    def __init__(self, images) -> None:
        #Create a frame
        self.frame = tk.Frame(root, bg=darkish, padx = 0, pady=10)
        #create a label that holds the picture
        self.imgLabel = tk.Label(root, image=images.woodImage, borderwidth=0, highlightthickness=0)
    
    def clearScreen(self):
        # Clear all the widgets in the frame
        clear_frame(self.frame)
        # forgetting the frame (clears it from screen but reference to it is held)
        self.frame.pack_forget()
        # Clear the title picture
        self.imgLabel.pack_forget()

    def PvCButtonReact(self, game_ui):
        self.clearScreen()
        game_ui.mode = "PVC"
        game_ui.drawAndReact(self)
    
    def PvPButtonReact(self, game_ui):
        self.clearScreen()
        game_ui.mode = "PVP"
        game_ui.drawAndReact(self)


    def drawAndReact(self, game_ui):
        # Pack the frame to the left
        self.frame.pack(side="bottom", fill = "x", padx=0) # , expand=True, fill="both" '''
        
        # Create a text label
        '''label1 = tk.Label(self.frame,text="INSTRUCTIONS: Try to flip the opponent's tiles", font=('Helvetica',14))
        label1.grid(row=0, column=0)'''
        
        # Create button
        PVC_text = """PLAYER V COMPUTER
        """
        button1 = tk.Button(self.frame, background=greyish, foreground='white',text= PVC_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=lambda:self.PvCButtonReact(game_ui))
        button1.grid(row=0, column=0, padx=80)
        
        # Create button2
        PVP_text = """PLAYER V PLAYER
        """
        button2 = tk.Button(self.frame, background=greyish, foreground='white',text= PVP_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=lambda:self.PvPButtonReact(game_ui))
        button2.grid(row=0, column=1, padx=32)
        
        # pack image from label
        self.imgLabel.pack(pady=0, padx=0)

class GameUI:
    def __init__(self, images) -> None:
        self.mode = ""  
        self.background = images.woodImage2
        # Create canvas
        self.canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
    

    def drawAndReact(self, menu_ui):
        self.canvas.pack(fill="both", expand="True") 
        # Set image in canvas
        self.canvas.create_image(0, 0, image=self.background, anchor="nw")

        
'''
pygame.init()

# generate screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("OTHELLO")'''

# Used to manage how fast the screen updates
# clock = pygame.time.Clock()


# Load background image
   # replace the backslash with forward slash for image loading
# print(picsPath)

# GameTitle = pygame.image.load(picsPath + "/OthelloGameTitle501W.jpg").convert()
# GameTitle = pygame.image.load('OthelloGameTitle.jpg')
