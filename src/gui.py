import os
import tkinter as tk
from PIL import Image, ImageTk
from game_logic import GameLogic
from globals import *



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
        thisFilePath = __file__
        print("This is the file path:", thisFilePath)

        parentPath = os.path.dirname(thisFilePath)
        print("This is the parent path:", parentPath)

        picsPath = parentPath + "\\pics"
        print("This is the pics path:", picsPath)
        picsPath = picsPath.replace("\\", "/") 
    
        self.woodImage = ImageTk.PhotoImage(Image.open(picsPath + "/woodPaint5.jpg"))
        self.woodImage2 = ImageTk.PhotoImage(Image.open(picsPath + "/wood2-3.jpg"))
        
        diskWidth = int (windowWidth/2/boardSize-8)
        self.blackDisk = ImageTk.PhotoImage(Image.open(picsPath + "/blackCircle.png").resize((diskWidth,diskWidth)))
        self.whiteDisk = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((diskWidth,diskWidth)))
        self.emptyPNG = ImageTk.PhotoImage(Image.open(picsPath + "/empty.png").resize((diskWidth,diskWidth)))

        

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
        self.game_ui.initialSetup("PVC")
    
    def PvPButtonReact(self):
        self.clearScreen()
        self.game_ui.initialSetup("PVP")


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

class GameUI():
    def __init__(self, images) -> None:
        self.mode = ""  
        self.images = images
        self.background = images.woodImage2
        self.menu_ui = None
        self.highlightOn = True
        
        # GameUi shall contain GameLogic class as a component (composition)
        self.game_logic = GameLogic()

     
    def deleteCanvas(self):

        ''' The following also works
        # self.canvas.pack_forget()
        # self.canvas.delete()
        '''
        self.canvas.destroy()
        

    def returnToMenu(self):
        self.deleteCanvas()
        self.menu_ui.drawAndReact()
        
    def initialSetup(self, mode):
        self.canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
        self.mode = mode
        self.game_logic.boardSetUp()

        if (mode == 'PVP'):
            self.drawAndReact()
        elif (mode == 'PVC'):
            self.PVPUserSetup()

    def PVPUserSetup(self):
        self.canvas.pack(fill="both", expand="True") 
        # Set image in canvas as background
        self.canvas.create_image(0, 0, image=self.background, anchor="nw")

        # Add UI Buttons
        self.addButtons()


    def drawAndReact(self):

        self.canvas.pack(fill="both", expand="True") 
        # Set image in canvas as background
        self.canvas.create_image(0, 0, image=self.background, anchor="nw")

        # Add UI Buttons
        self.addButtons()
        
        # Draw game board
        self.drawBoard()
    
    def addButtons(self):
        menuButton = tk.Button(root, text = "Menu", command=self.returnToMenu)
        menuButtonWindow = self.canvas.create_window(10, 10, anchor="nw", window=menuButton)
        

    def drawBoard(self):
        # Create frame for board
        frame = tk.Frame(root, bg="black", width=windowWidth/2 + 10, height=windowWidth/2 + 10, highlightthickness=4, highlightbackground=greyish)
        frameWindow = self.canvas.create_window(windowWidth/4 -5, windowHeight/4 -5, anchor="nw", window=frame)
        
        # pre-calculate which tiles are to be highlighted, if the option is on
        if (self.highlightOn):
            self.game_logic.setBoardHighlights()

        # Create Tiles and disks
        tileSpacing = windowWidth/2/boardSize
        tileWidth = int(tileSpacing - 4) 
        startPos = int(windowWidth/4 + tileWidth/2 + 2)
        board = self.game_logic.board
        pixel = tk.PhotoImage(width=tileWidth, height=tileWidth)
        tempi = startPos
        for i in range(boardSize):
            tempj = startPos    
            for j in range(boardSize):
                if board[i][j].color == "U":
                    # use png to fix
                    # when using images, width and height will be using pixel scale
                    button = tk.Button(root, command=lambda i=i, j=j: self.tileClicked(i, j), image=self.images.emptyPNG, 
                        bg='green' if board[i][j].highlight == False else lightGreen, borderwidth=0, width=tileWidth, height=tileWidth)
                
                elif board[i][j].color == "W":                
                    button = tk.Button(root, command=lambda i=i, j=j: self.tileClicked(i, j), image=self.images.whiteDisk, 
                        bg='green' if board[i][j].highlight == False else lightGreen, borderwidth=0, width=tileWidth, height=tileWidth)

                else:
                    button = tk.Button(root, command=lambda i=i, j=j: self.tileClicked(i, j), image=self.images.blackDisk, 
                        bg='green' if board[i][j].highlight == False else lightGreen, borderwidth=0, width=tileWidth, height=tileWidth)
                
                # ButtonWindow = self.canvas.create_window(startPos + j*tileSpacing, startPos + i*tileSpacing, window=button)
                ButtonWindow = self.canvas.create_window(tempj, tempi, window=button)
                tempj += tileSpacing
            tempi += tileSpacing

    def tileClicked(self, i, j):
        print((i,j))
        # load info about this placement including whether move is legal, the tiles that can be flipped,
        # and the current turn's color (needed to set next turn's color, or not)

        info = self.game_logic.getPlacementInfo(i, j, self.game_logic.thisTurnColor)
        print(info)
        legal = False
        if not legal:
            return

        if self.mode == "PVP":
            pass
        elif self.mode == "PVC":
            pass
    

    


