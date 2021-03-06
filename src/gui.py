import os
import tkinter as tk
from PIL import Image, ImageTk
from game_logic import GameLogic, GameStatus
from globals import *
import time




# Creating the root (window)
root = tk.Tk()

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

def create_circle(canvasName,x, y, r, outline, fill, width = 1):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, outline=outline, fill=fill, width=width)



class Images():
    def __init__(self) -> None:
        thisFilePath = __file__
        # print("This is the file path:", thisFilePath)

        parentPath = os.path.dirname(thisFilePath)
        # print("This is the parent path:", parentPath)

        picsPath = parentPath + "\\pics"
        # print("This is the pics path:", picsPath)
        picsPath = picsPath.replace("\\", "/") 

        self.picsPathFSlash = picsPath
        self.woodImage = ImageTk.PhotoImage(Image.open(picsPath + "/menuUIBackgroundBW.png"))
        self.woodImage2 = ImageTk.PhotoImage(Image.open(picsPath + "/wood2-3.jpg"))
        
        diskWidth = int (windowWidth/2/boardSize-8)
        self.blackDisk = ImageTk.PhotoImage(Image.open(picsPath + "/blackCircle.png").resize((diskWidth,diskWidth)))
        self.whiteDisk = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((diskWidth,diskWidth)))
        self.emptyPNG = ImageTk.PhotoImage(Image.open(picsPath + "/empty.png").resize((diskWidth,diskWidth)))
        self.blackDiskLarge = ImageTk.PhotoImage(Image.open(picsPath + "/blackCircle.png").resize((100,100)))
        self.whiteDiskLarge = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((100,100)))
        self.blackDiskMedium = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((70,70)))
        self.whiteDiskMedium = ImageTk.PhotoImage(Image.open(picsPath + "/whiteCircle.png").resize((70,70)))


class MenuUI():
    def __init__(self, images : Images) -> None:
        
        self.images=images
        
        # Create reference to GameUI
        self.game_ui : GameUI

        #Create a frame
        self.frame = tk.Frame(root, bg=darkish, padx = 0, pady=10)
        #create a label that holds the picture
        self.imgLabel = tk.Label(root, image=self.images.woodImage, borderwidth=0, highlightthickness=0)

         # Create button
        PVC_text = """PLAYER V COMPUTER
        """
        self.button1 = tk.Button(self.frame, background=darkGreyish, foreground='white',text= PVC_text, font=('Arial', 12),
            width=25, pady=30, borderwidth=20, command=self.PvCButtonReact)
        
        # Create button2
        PVP_text = """PLAYER V PLAYER
        """
        self.button2 = tk.Button(self.frame, background=darkGreyish, foreground='white',text= PVP_text, font=('Arial', 12),
            width=25, pady=30, borderwidth=20, command=self.PvPButtonReact)
        
        self.button1.grid(row=0, column=0, padx=80)
        
        self.button2.grid(row=0, column=1, padx=32)

    def clearScreen(self):
        # Clear all the widgets in the frame
            # clear_frame(self.frame) (Unnecessary here)
            # forgetting the frame (clears it from screen but reference to it is held)
        self.frame.pack_forget()
            # Clear the title picture
        self.imgLabel.pack_forget()

        # self.button1.grid_forget()
        # self.button1.grid_forget()

        # self.frame.destroy() 
        # self.imgLabel.destroy()

    def PvCButtonReact(self):
        self.clearScreen()
        self.game_ui.initialSetup("PVC")
    
    def PvPButtonReact(self):
        self.clearScreen()
        self.game_ui.initialSetup("PVP")


    def show(self):
        # Pack the frame to the left
        self.frame.pack(side="bottom", fill = "x", padx=0) # , expand=True, fill="both" '''
        self.imgLabel.pack(pady=0, padx=0)

class GameUI():
    # Static
    defaultHighlight = True
    highlightColor = lightBlue2
    tileColor = greenBlue
    colorCountHighlight = orangeish

    def __init__(self, images:Images) -> None:
        # GameUi shall contain a reference to GameLogic
        self.game_logic:GameLogic

        self.game_status = GameStatus()
        self.mode = ""  
        self.images = images
        self.background = images.woodImage2
        self.menu_ui = None
        self.highlightOn = self.defaultHighlight
        self.firstTimeOpen = True

        # canvas and helper buttons
        self.canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
            # Set image in canvas as background
        self.background = self.canvas.create_image(0, 0, image=self.background, anchor="nw") 
        
        menuButton = tk.Button(self.canvas, text = "Menu", command=self.returnToMenu, 
            background=darkGreyish, foreground='white', font=('Fixedsys',10))
        self.menuButtonWindow = self.canvas.create_window(10, 10, anchor="nw", window=menuButton)

        highLightButton = tk.Button(self.canvas, text = "Toggle Highlight", command=self.highlightButtonCallBack, 
            background=darkGreyish, foreground='white', font=('Fixedsys',10))
        self.highlightButtonWindow = self.canvas.create_window(70, 10, anchor="nw", window=highLightButton)

        # board background
        frame = tk.Frame(self.canvas, bg="black", width=windowWidth/2 + 18, height=windowWidth/2 + 18, highlightthickness=5, highlightbackground=greyish)
        frameWindow = self.canvas.create_window(windowWidth/4 - 9, windowHeight/4 - 9, anchor="nw", window=frame)
        
        # Empty board
        tileSpacing = windowWidth/2/boardSize
        tileWidth = int(tileSpacing - 4) 
        self.uiBoard = [[None for j in range(boardSize)] for i in range(boardSize)]
        for i in range(boardSize):
            for j in range(boardSize):
                # use png for button without a disk
                # when using images, width and height will be using pixel scale
                button = tk.Button(self.canvas, command=lambda i=i, j=j: self.tileClicked(i, j), image=self.images.emptyPNG, 
                    bg=self.tileColor, borderwidth=0, width=tileWidth, height=tileWidth)
                self.uiBoard[i][j] = button

        # Color info
        whiteCountLocX = windowWidth/4-50
        whiteCountLocY = windowHeight - 100
        blackCountLocX = windowWidth*3/4+50
        blackCountLocY = whiteCountLocY
        self.canvas.create_image(whiteCountLocX, whiteCountLocY, image = self.images.whiteDiskLarge)
        self.whiteCountHighlight = create_circle(self.canvas, windowWidth/4-50, windowHeight - 100, r=50, outline='orange', width=2, fill='') 
        self.canvas.create_image(blackCountLocX, blackCountLocY, image = self.images.blackDiskLarge)
        self.blackCountHighlight = create_circle(self.canvas, blackCountLocX, blackCountLocY, r=50, outline=self.colorCountHighlight, fill='') 
        

        self.whiteCount = tk.Label(self.canvas, text="", bg=almostWhite, font=('Fixedsys',17))
        self.blackCount = tk.Label(self.canvas, text="", bg='black', foreground='white', font=('Fixedsys',17))
        self.whiteCount.place(x=whiteCountLocX, y=whiteCountLocY, anchor="center")
        self.blackCount.place(x=blackCountLocX, y=blackCountLocY, anchor="center")

        # Turn info (currently unused)
        # self.whiteTurn = self.canvas.create_text(whiteCountLocX, whiteCountLocY-70, text="Turn", fill='grey', font=('Fixedsys',17))
        # self.blackTurn = self.canvas.create_text(blackCountLocX, blackCountLocY-70, text="Turn", fill='white', font=('Fixedsys',17))
    
    def forgetBoard(self):
        for i in range(boardSize):
            for j in range(boardSize):
                self.uiBoard[i][j].place_forget()
     
    def deleteCanvas(self):

        ''' The following also works
        # self.canvas.pack_forget()
        # self.canvas.delete()
        '''
        self.canvas.delete("all")
        self.canvas.destroy()
        

    def returnToMenu(self):
        self.canvas.pack_forget()
        self.menu_ui.show()

    def highlightButtonCallBack(self):
        if self.highlightOn:
            self.game_logic.removeBoardHighlights()
            self.highlightOn = False
            self.game_logic.highlightOn = False
            self.changeBoardAndInfo()
            return
        else:
            self.game_logic.setBoardHighlights()
            self.highlightOn = True
            self.game_logic.highlightOn = True
            self.changeBoardAndInfo()
            return

        
    def initialSetup(self, mode):
        self.mode = mode
        self.highlightOn = self.defaultHighlight
        self.firstTimeOpen = True
        self.game_status = self.game_logic.boardSetUp(mode, self.highlightOn)
        
        if (mode == 'PVP'):
            self.PVPUserSetup()
        elif (mode == 'PVC'):
            self.PVCUserSetup()

    def PVPUserSetup(self):
        self.canvas.pack(fill="both", expand="True") 
        self.canvas.itemconfig(self.whiteCountHighlight, state='hidden')

        self.changeBoardAndInfo()

    def PVCUserSetup(self):
        pass

    def changeBoardAndInfo(self):
        # Draw color count
        self.whiteCount.config(text=str(self.game_status.colorCount['white']))
        self.blackCount.config(text=str(self.game_status.colorCount['black']))
        if self.game_logic.thisTurnColor == 'B':
            self.canvas.itemconfig(self.blackCountHighlight, state='normal')
            self.canvas.itemconfig(self.whiteCountHighlight, state='hidden')
        else:
            self.canvas.itemconfig(self.blackCountHighlight, state='hidden')
            self.canvas.itemconfig(self.whiteCountHighlight, state='normal')
        # Draw whose move

        # Draw game board
        self.drawBoard()
    
    def addButtons(self):
        menuButton = tk.Button(root, text = "Menu", command=self.returnToMenu)
        menuButtonWindow = self.canvas.create_window(10, 10, anchor="nw", window=menuButton)
        

    def drawBoard(self):
        # Create Tiles and disks
        tileSpacing = windowWidth/2/boardSize
        tileWidth = int(tileSpacing - 4) 
        # startPos = int(windowWidth/4 + tileWidth/2 + 2)
        startPos = int(windowWidth/4 + 1)
        board = self.game_logic.board
        tempi = startPos
        
        for i in range(boardSize):
            tempj = startPos    
            for j in range(boardSize):
                
                if board[i][j].color == "U":
                    # use png to fix
                    # when using images, width and height will be using pixel scale
                    self.uiBoard[i][j].config(image=self.images.emptyPNG, 
                        bg=self.tileColor if board[i][j].highlight == False else self.highlightColor)
                
                elif board[i][j].color == "W":                
                    self.uiBoard[i][j].config(image=self.images.whiteDisk, 
                        bg=self.tileColor if board[i][j].highlight == False else self.highlightColor)

                else:
                    self.uiBoard[i][j].config(image=self.images.blackDisk, 
                        bg=self.tileColor if board[i][j].highlight == False else self.highlightColor)
                
                if self.firstTimeOpen:
                    self.uiBoard[i][j].place(x = tempj, y = tempi)

                
                tempj += tileSpacing
            tempi += tileSpacing
        self.firstTimeOpen = False


    def tileClicked(self, i, j):
        print((i,j))
        # load info about this placement including whether move is legal, the tiles that can be flipped,
        # and the current turn's color (needed to set next turn's color, or not)
        curColor = self.game_logic.thisTurnColor
        moveMade, game_status = self.game_logic.actToTileClicked(i, j)
        self.game_status = game_status
        
        if not moveMade:
            return
        
        # Otherwise, a move has been made in gamelogic
        # Place disk        
        board = self.game_logic.board
        self.uiBoard[i][j].config(image=self.images.blackDisk if board[i][j].getColor() == 'B' else self.images.whiteDisk, 
            bg=self.tileColor)
        root.update_idletasks()
        # delay and then flip disks
        root.after(200, self.changeBoardAndInfo())    
        
        # Act if enemy can't make moves or game over
        if game_status.gameOver:
            self.gameOverScreen()
        
        if curColor == game_status.thisTurnColor:
            # This means enemy cannot make a move, and the current player must keep playing
            pass


        
        if self.mode == "PVP":
            return    
        else:
            # mode is player vs AI
        
            # Call AI to make move and change gameboard
            # then draw board
            # use timer for delay
            pass
        
    def gameOverScreen(self):
        game_status = self.game_status
        if game_status.gameOverReason == game_status.NOMOVES:
            pass
        if game_status.gameOverReason == game_status.BOARDFULL:
            pass
