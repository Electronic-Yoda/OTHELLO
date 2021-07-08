from tkinter.constants import LEFT, RIGHT
import pygame
import math
import sys, os
import tkinter as tk
from PIL import Image
from PIL import ImageTk

tempFilePath = os.path.abspath("Othello_AI")
# print("This is the file path:", tempFilePath)

OthelloAIPath = os.path.dirname(tempFilePath)
# print("This is the parent path:", OthelloAIPath)

picsPath = OthelloAIPath + "\src\pics"
# print("This is the pics path:", picsPath)
picsPath = picsPath.replace("\\", "/") 

# sys.path.insert(1, picsPath)
# On/off states
programOn = False
menuOn = False

PI = math.pi




reddish = '#6E4137'
yellowish = '#E8E4A0'
blueish = '#274098'
darkGreyish='#797D7F'
darkish = '#17202A'
greyish = '#A69E99'
root = tk.Tk()
root.title('OTHELLO')
root.geometry("800x800")
root['background'] = "black"

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

class Images():
    def __init__(self) -> None:
        self.titleImg = ImageTk.PhotoImage(Image.open(picsPath + "/woodPaint5.jpg"))
    

class Menu():
    def __init__(self, images) -> None:
        #Create a frame
        self.frame = tk.Frame(root, bg=darkish, padx = 0, pady=10)
        #create a label that holds the picture
        self.imgLabel = tk.Label(root, image=images.titleImg, borderwidth=0, highlightthickness=0)

    def PvCButtonReact(self):
        # Clear all the widgets in the frame
        clear_frame(self.frame)
        # forgetting the frame (clears it from screen but reference to it is held)
        self.frame.pack_forget()
        # Clear the title picture
        self.imgLabel.pack_forget()
    
    def PvPButtonReact(self):
        # Clear all the widgets in the frame
        clear_frame(self.frame)
        # forgetting the frame (clears it from screen but reference to it is held)
        self.frame.pack_forget()
        # Clear the title picture
        self.imgLabel.pack_forget()

    def drawMenu(self):
        # Pack the frame to the left
        self.frame.pack(side="bottom", fill = "x", padx=0) # , expand=True, fill="both" '''
        
        # Create a text label
        '''label1 = tk.Label(self.frame,text="INSTRUCTIONS: Try to flip the opponent's tiles", font=('Helvetica',14))
        label1.grid(row=0, column=0)'''
        
        # Create button
        PVC_text = """PLAYER V COMPUTER
        """
        button1 = tk.Button(self.frame, background=darkGreyish, foreground='white',text= PVC_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=self.PvCButtonReact)
        button1.grid(row=0, column=0, padx=80)
        
        # Create button2
        PVP_text = """PLAYER V PLAYER
        """
        button2 = tk.Button(self.frame, background=darkGreyish, foreground='white',text= PVP_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=self.PvPButtonReact)
        button2.grid(row=0, column=1, padx=32)
        
        # pack image from label
        self.imgLabel.pack(pady=0, padx=0)

        

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
