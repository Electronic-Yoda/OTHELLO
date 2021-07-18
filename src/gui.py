from tkinter.constants import ANCHOR, LEFT, RIGHT
import math
import sys, os
import tkinter as tk
from PIL import Image
from PIL import ImageTk

# Global variables
reddish = '#6E4137'
yellowish = '#D1CFA6'
blueish = '#274098'
darkGreyish='#797D7F'
darkish = '#17202A'
greyish = '#A69E99'
windowWidth = 800
windowHeight = 800
boardSize = 8

# Creating the root (window)
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
        
        diskWidth = int (windowWidth/2/boardSize-8)
        self.blackDisk = ImageTk.PhotoImage(Image.open(picsPath + "/blackCircle.png").resize((diskWidth,diskWidth)))
        self.whiteDisk = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((diskWidth,diskWidth)))

class MenuUI():
    def __init__(self, images) -> None:
        
        self.images=images
        
        # Create empty game UI
        self.game_ui = None   

        self.Frame = None
        self.imgLabel = None

    def clearScreen(self):
        # Clear all the widgets in the frame
            # clear_frame(self.frame) (Unnecessary here)
            # forgetting the frame (clears it from screen but reference to it is held)
        # self.frame.pack_forget()
            # Clear the title picture
        # self.imgLabel.pack_forget()
        
        self.frame.destroy() 
        self.imgLabel.destroy()

    def PvCButtonReact(self):
        self.clearScreen()
        self.game_ui.mode = "PVC"
        self.game_ui.initialSetup()
    
    def PvPButtonReact(self):
        self.clearScreen()
        self.game_ui.mode = "PVP"
        self.game_ui.initialSetup()


    def drawAndReact(self):
        #Create a frame
        self.frame = tk.Frame(root, bg=darkish, padx = 0, pady=10)
        #create a label that holds the picture
        self.imgLabel = tk.Label(root, image=self.images.woodImage, borderwidth=0, highlightthickness=0)


        # Pack the frame to the left
        self.frame.pack(side="bottom", fill = "x", padx=0) # , expand=True, fill="both" '''
        
        # Create a text label
        '''label1 = tk.Label(self.frame,text="INSTRUCTIONS: Try to flip the opponent's tiles", font=('Helvetica',14))
        label1.grid(row=0, column=0)'''
        
        # Create button
        PVC_text = """PLAYER V COMPUTER
        """
        button1 = tk.Button(self.frame, background=greyish, foreground='white',text= PVC_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=self.PvCButtonReact)
        button1.grid(row=0, column=0, padx=80)
        
        # Create button2
        PVP_text = """PLAYER V PLAYER
        """
        button2 = tk.Button(self.frame, background=greyish, foreground='white',text= PVP_text, font=('Helvetica bold', 12),
            width=25, pady=30, borderwidth=20, command=self.PvPButtonReact)
        button2.grid(row=0, column=1, padx=32)
        
        # pack image from label
        self.imgLabel.pack(pady=0, padx=0)

class GameUI:
    def __init__(self, images) -> None:
        self.mode = ""  
        self.images = images
        self.background = images.woodImage2
        self.menu_ui = None
     
        
    
    def deleteCanvas(self):

        ''' The following also works
        # self.canvas.pack_forget()
        # self.canvas.delete()
        '''
        self.canvas.destroy()
        

    def returnToMenu(self):
        self.deleteCanvas()
        self.menu_ui.drawAndReact()
        
        

    def drawAndReact(self):
        self.canvas.pack(fill="both", expand="True") 
        # Set image in canvas as background
        self.canvas.create_image(0, 0, image=self.background, anchor="nw")
        # Add buttons
        menuButton = tk.Button(root, text = "Menu", command=self.returnToMenu)
        menuButtonWindow = self.canvas.create_window(10, 10, anchor="nw", window=menuButton)
        
        # Create frame for board
        frame = tk.Frame(root, bg="black", width=windowWidth/2 + 10, height=windowWidth/2 + 10, highlightthickness=4, highlightbackground=greyish)
        frameWindow = self.canvas.create_window(windowWidth/4 -5, windowHeight/4 -5, anchor="nw", window=frame)
        
        # Create Tiles and disks
        tileSpacing = windowWidth/2/boardSize
        tileWidth = tileSpacing - 4 
        startPos = windowWidth/4 + tileWidth/2 + 2
        
        for i in range(boardSize):
            for j in range(boardSize):
                button = tk.Button(root, image=self.images.whiteDisk, bg='green', borderwidth=0, width=tileWidth, height=tileWidth)
                ButtonWindow = self.canvas.create_window(startPos + j*tileSpacing, startPos + i*tileSpacing, window=button)
        
        '''
        testButton = tk.Button(root, image=self.images.blackDisk, bg='green', borderwidth=0, width=34, height = 34)
        testButtonWindow = self.canvas.create_window(windowWidth/2, windowHeight/2,  window=testButton)
        '''

    def initialSetup(self):
        self.canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
        self.drawAndReact()


