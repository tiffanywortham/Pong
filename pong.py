'''
Tiffany Wortham
Trace Folder: Tiffany373
lab9.py: Dope pong game complete with a nice menu

Extra Features:

1. Menu bar with -New Game, -Options, -Toggle Monster Shower, & -Quit
2. New Game: starts a new game
3. Options: User can control -Animation Speed -Paddle Speed & -Theme
4. Toggle Monster Shower: Toggles Monster Shower
5. Quit: DESTROYS window (Though not gracefully)
6. Powerup that adds 250 points to score and restores a life
7. Points system
'''

from tkinter import *
import random

class Bounce(Frame):
      
    def __init__(self):
        #Creates frame
        Frame.__init__(self)
        self.master.title("Tiffany's Pong Game")
        self.grid()
        
        #1. Menu bar with New Game, Options, Toggle Monster Shower & Quit
        menu = Menu(self.master)
        
        #2. New Game starts a new game
        newGame = Menu(menu)
        menu.add_command(label = "New Game", command = self.newGame)
        
        #3. Speed menu for paddle which cascades under Options
        speedMenu = Menu(menu)
        speedMenu.add_command(label = "Slow", command = self.slowPaddle)
        speedMenu.add_command(label = "Medium", command = self.mediumPaddle)
        speedMenu.add_command(label = "Fast", command = self.fastPaddle)
        speedMenu.add_command(label = "Fast af", command = self.fastAfPaddle)
        
        #3. Speed menu for animation which cascades under Options
        animationMenu = Menu(menu)
        animationMenu.add_command(label = "Normal",
                                  command = self.normalAnimation)
        animationMenu.add_command(label = "Speedy",
                                  command = self.speedyAnimation)
        animationMenu.add_command(label = "Real Speedy",
                                  command = self.realSpeedyAnimation)
        #3. Theme menu changes colors which cascades under Options
        themeMenu = Menu(menu)
        themeMenu.add_command(label = "Terminal", command = self.termTheme)
        themeMenu.add_command(label = "Spooky", command = self.spookyTheme)
        themeMenu.add_command(label = "Tux", command = self.tuxTheme)
        
        #3. Adds paddle's speedMenu and animation speed's animationMenu to
        #Options
        options = Menu(menu)
        options.add_cascade(label = "Paddle Speed", menu = speedMenu)
        options.add_cascade(label = "Animation Speed", menu = animationMenu)
        options.add_cascade(label = "Theme", menu = themeMenu)
        menu.add_cascade(label = "Options", menu = options)
        
        #4. ToggleMonsterShower toggles monster shower
        toggleMonsterShower = Menu(menu)
        menu.add_command(label = "Toggle Monster Shower",
                         command = self.toggleMonsterShower)
        scoreMenu = Menu(menu)
        
        #5. Quits game
        quitMenu = Menu(menu)
        menu.add_command(label = "Quit", command = self.quitGame)
        
        #1. Adds entire menu to window
        self.master.config(menu = menu)
        
        #Frame width and height
        cWidth = 800
        cHeight = 400

        #self.shapeColor is for both the ball and the paddle
        self.bgColor = "black"
        self.shapeColor = "#00e600"
        
        #Creates canvas
        self.canvas = Canvas(width = cWidth, height = cHeight,
                             bg = self.bgColor)
        self.canvas.grid()
        
        #Ball diameter and top left coordinates
        self.ballD = 20
        self.topX = 2
        self.topY = 2

        #Paddle coordinates
        self.pTopX = 360
        self.pTopY = 380
        self.pBottomX = 440
        self.pBottomY = 400

        #2. Animation speed vairable that can be changed in
        #Options > Animation Speed
        self.animationSpeed = 15

        #Keeps track of and displays lives
        self.livesCount = 5
        self.livesVar = StringVar()
        self.livesVar.set("Lives Left: " + str(self.livesCount))
        self.livesFont = font.Font(family = "fixedsys", size = 18)
        self.livesLabel = Label(self, textvariable = self.livesVar,
                                font = self.livesFont)
        self.livesLabel.grid()

        #7. Initialize score at 0 and multiplier at 1
        self.pointsCount = 0
        self.pointsMultiplier = 1
        #7. Keep track of and display current score
        self.pointsVar = StringVar()
        self.pointsVar.set("Score: " + str(int(self.pointsCount)))
        self.pointsFont = font.Font(family = "fixedsys", size = 14)
        self.pointsLabel = Label(self, textvariable = self.pointsVar,
                                 font = self.pointsFont)
        self.pointsLabel.grid()

        #Creates ball
        self.canvas.create_oval(self.topX, self.topY, self.topX + self.ballD,
                                self.topY + self.ballD, fill = self.shapeColor,
                                tags = "ball")
        #Creates paddle
        self.canvas.create_rectangle(self.pTopX, self.pTopY, self.pBottomX,
                                     self.pBottomY, fill = self.shapeColor,
                                     tags = "paddle")
        #Ball's intitial direction
        self.horizontalD = "east"
        self.verticalD = "south"
        
        #Move ball
        dx = dy = 2
        
        #Move paddle
        self.pDx = 5

        #Move powerup
        self.powerDx = 2

        #Monster shower is not default
        self.monsterShower = False

        #6. Initializes gameTimer at 1000 and makes sure the powerup isn't moved
        #until timer is up by setting self.movePowerup to False
        self.gameTimer = 1000
        self.movePowerup = False

        while True:    
            #Move ball and check for keyboard input constantly
            
            self.canvas.focus_set()
            #6. Decrement game timer by 1 every update
            self.gameTimer -= 1
            
            if self.horizontalD == "east":
                #Takes care of horizontal movement when moving east
                self.topX += dx
                if self.topX >= (cWidth - self.ballD):
                    self.topX = cWidth - self.ballD
                    self.horizontalD = "west"
                self.canvas.move("ball", dx, 0)
            else:
                #Takes care of horizontal movement when moving west
                self.topX -= dx
                if self.topX <= 0:
                    self.topX = 0
                    self.horizontalD = "east"
                self.canvas.move("ball", -dx, 0)

            if self.verticalD == "south":
                #Takes care of vertical movement when moving south
                self.topY += dy

                if self.topY >= (cHeight - self.ballD):
                    self.topY = cHeight - self.ballD
                    self.verticalD = "north"
                
                    if self.topY + self.ballD >= cHeight:
                        #If the ball hits the south wall, reduce lives by 1
                        self.livesCount -= 1
                        self.livesVar.set("Lives Left: " + str(self.livesCount))
                        #And reset the points multiplier
                        self.pointsMultiplier = 1
                        
                self.canvas.move("ball", 0, dy)
                
            else:
                #Takes care of vertical movement when moving north
                self.topY -= dy
                if self.topY <= 0:
                    self.topY = 0
                    self.verticalD = "south"
                self.canvas.move("ball", 0, -dy)

            if (self.topX >= self.pTopX and self.topX + self.ballD <= self.pTopX
                + 80):
                if self.topY + self.ballD >= self.pTopY:
                    #Takes care of paddle and ball collision
                    self.verticalD = "north"
                    
                    if (self.topY <= self.pTopY and self.topY + self.ballD <=
                        self.pTopY):
                        #7. Only add to score if ball is at or above paddle
                        #height (Prevents adding to score if ball hits side of
                        #paddle)
                        self.score()

            #Control paddles with left and right arrow keys
            self.canvas.bind("<Left>", self.moveLeft)
            self.canvas.bind("<Right>", self.moveRight)

            if self.monsterShower == True:
                #4. If user selects Toggle Monster Shower in the menu,
                #self.monsterShower == True and a monster shower commences
                self.powerX = random.randrange(800)
                self.powerY = random.randrange(400)
                self.monsterImage = PhotoImage(file = "monster.png")
                self.canvas.create_image(self.powerX, self.powerY, tags =
                                     "monster", image = self.monsterImage)

            if self.livesCount <= 0:
                #If lives run out, player dies and game starts over
                self.newGame()

            #Check to see if timer has run out, if so, create powerup and
            #make self.movePowerup = True
            self.powerups()

            if self.movePowerup == True:
                #Move the powerup down the screen
                self.powerTopY += self.powerDx
                self.powerBotY += self.powerDx
                self.canvas.move("powerup1", 0, self.powerDx)
                
                if self.powerTopY == 400:
                    #If powerup hits the ground, stop moving it and delete it
                    self.movePowerup = False
                    self.canvas.delete("powerup1")
                    
                if (self.powerBotY >= self.pTopY and self.powerBotX >=
                    self.pTopX and self.powerTopX <= self.pBottomX):
                    #If powerup hits paddle, stop moving it, delete it, and add
                    #250 points to the score
                    self.movePowerup = False
                    self.canvas.delete("powerup1")
                    self.pointsCount += 250
                    self.pointsVar.set("Score: " + str(int(self.pointsCount)))

                    if self.livesCount < 5:
                        #If a life has been lost, add a life
                        self.livesCount += 1
                        self.livesVar.set("Lives Left: " + str(self.livesCount))
              
            #3. Update canvas every 15, 10, or 5 milliseconds depending on what
            #user has selected from Options > Animation Speed, or default 15
            self.canvas.after(self.animationSpeed)
            self.canvas.update()

    def moveLeft(self, event):
        #Move paddle left by pDx, which dictates the speed
        if self.pTopX > 0:
            self.pTopX -= self.pDx
            self.pBottomX -= self.pDx
            self.canvas.move("paddle", -self.pDx, 0)

    def moveRight(self, event):
        #Move paddle right by pDx, which dictates the speed
        if self.pTopX + 80 < 800:
            self.pTopX += self.pDx
            self.pBottomX += self.pDx
            self.canvas.move("paddle", self.pDx, 0)
            
    def newGame(self):
        #2. If user selects New Game from the menu, this function is called and
        #the game is reset. This also happens if the player dies.

        #Reset variables, except for self.animationSpeed,
        #since I think it should stay as selected even when the game is reset
        self.livesCount = 5
        self.livesVar.set("Lives Left: " + str(self.livesCount))
        self.horizontalD = "east"
        self.verticalD = "south"
        self.canvas.delete("ball")
        self.canvas.delete("paddle")
        self.topX = 2
        self.topY = 2
        self.pTopX = 360
        self.pTopY = 380
        self.pBottomX = 440
        self.pBottomY = 400
        self.pDx = 5
        self.monsterShower = False
        self.canvas.delete("monster")
        self.pointsCount = 0
        self.pointsVar.set("Score: " + str(int(self.pointsCount)))
        self.gameTimer = 1000
        self.canvas.delete("powerup1")
        self.canvas.movePowerup = False
        
        #Create new ball and paddle in their initial positions
        self.canvas.create_oval(self.topX, self.topY, self.topX + self.ballD,
                                self.topY + self.ballD, fill = self.shapeColor,
                                tags = "ball")
        self.canvas.create_rectangle(self.pTopX, self.pTopY, self.pBottomX,
                                     self.pBottomY, fill = self.shapeColor,
                                     tags = "paddle")

    def slowPaddle(self):
        #3. Changes paddle speed variable, this function is called from
        #Options > Paddle Speed > Slow
        self.pDx = 5

    def mediumPaddle(self):
        #3. Changes paddle speed variable, this function is called from
        #Options > Paddle Speed > Medium
        self.pDx = 10

    def fastPaddle(self):
        #3. Changes paddle speed variable, this function is called from
        #Options > Paddle Speed > Fast
        self.pDx = 20

    def fastAfPaddle(self):
        #3. Changes paddle speed variable, this function is called from
        #Options > Paddle Speed > Fast af
        self.pDx = 50
            
    def normalAnimation(self):
        #3. Changes Animation speed variable, this function is called from
        #Options > Animation Speed > Normal
        self.animationSpeed = 15

    def speedyAnimation(self):
        #3. Changes Animation speed variable, this function is called from
        #Options > Animation speed > Speedy
        self.animationSpeed = 10

    def realSpeedyAnimation(self):
        #3. Changes Animation speed variable, this function is called from
        #Options > Animation speed > Real Speedy
        self.animationSpeed = 5

    def termTheme(self):
        #3. Changes color of ball and paddle and starts a new game this function
        #if called from Options > Theme > Terminal
        self.shapeColor = "#00e600"
        self.newGame()

    def spookyTheme(self):
        #3. Changes color of ball and paddle and starts a new game this function
        #if called from Options > Theme > Spooky
        self.shapeColor = "orange"
        self.newGame()

    def tuxTheme(self):
        #3. Changes color of ball and paddle and starts a new game this function
        #if called from Options > Theme > Tux
        self.shapeColor = "white"
        self.newGame()
                            
    def toggleMonsterShower(self):
        #4. Turn self.monsterShower on and off. This function is called from
        #Toggle Monster Shower
        self.monsterShower = True if self.monsterShower == False else False
        if self.monsterShower == False:
            self.canvas.delete("monster")

    def quitGame(self):
        #5. Quits window. This function is called from Quit
        self.master.quit()
        self.master.destroy()

    def powerups(self):
        #6. After 1000 updates, create a square to appear at the top of the
        #screen at a random X coordinate on the screen and reset the timer.
        if self.gameTimer == 0:
            self.powerTopX = random.randrange(800)
            self.powerTopY = 0
            self.powerBotX = self.powerTopX + 25
            self.powerBotY = 25
            self.gameTimer = 1000
            self.canvas.create_rectangle(self.powerTopX, self.powerTopY,
                                             self.powerBotX, self.powerBotY,
                                             fill = "#ff1ac6",
                                             tags = "powerup1")
            #6. Allow powerup code in init to run
            self.movePowerup = True   

    def score(self):
        #7. Add a base number of 50 points * the multiplier which starts at 1
        #and is incremented by .2 each time the ball is hit to the player's
        #score. Once a life is lost the streak is dropped and the multiplier
        #resets to 1
        self.addPoints = 50 * self.pointsMultiplier
        self.pointsCount += self.addPoints
        self.pointsMultiplier += .2
        self.pointsVar.set("Score: " + str(int(self.pointsCount)))
                  
def main():
    Bounce().mainloop()

main()                       
