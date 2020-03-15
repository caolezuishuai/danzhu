# created by Gabriel version 1.0
from tkinter import *
import random
import math
import tkinter.messagebox
import tkinter.simpledialog

Radius = [25, 40, 60, 80] # radius list for ball generation
buffLocation = list(range(30, 590, 20))
xspeed = 4 # left-right speed
acce = 0.5 # acceleration

def dist(x1, y1, x2, y2):
    return math.sqrt( (x1-x2) ** 2 + (y1-y2) ** 2)

def collision(rx, ry, w, h, r): # rx ry the circle's center(in comparison to the rectangle's center placed at 0 0), width height radius
    dx = min(rx, w * 0.5)
    dx1 = max(dx, -w * 0.5)
    dy = min(ry, h * 0.5)
    dy1 = max(dy, -h * 0.5)

    return (dx1-rx) ** 2 + (dy1-ry) ** 2 <= r ** 2



class Ball:
    def __init__(self, tier, number):

        # generating initial x coordinate
        temp = random.randint(1,2) # 1 represents left side, 2 represents right side
        if temp == 1:
            self.x = random.randint(16,80) # x in 16 to 80
        elif temp == 2:
            self.x = random.randint(520,584) # x in 520 to 584

        self.y = 20
        
        self.tier = tier # the tier of ball, 1 2 3 4 
        self.radius = Radius[self.tier - 1]
        
        self.maxnum = number # max number saved here
        self.number = self.maxnum # recording the remaining health of the ball

        self.yspeed = 0 # initial y speed 0
        if temp == 1:
            self.xdirection = 1 # 1 for moving right
        elif temp == 2:
            self.xdirection = 2 # 2 for moving left
        self.ydirection = 1 # 1 for moving down and 2 for moving up

    def death(self):
        if self.number <= 0:
            return True
        else:
            return False

    def update(self):

        # update x position and speed
        if self.xdirection == 1:
            if self.x+self.radius+xspeed > 600:
                self.xdirection = 2
                self.x -= xspeed
            else:
                self.x += xspeed
        elif self.xdirection == 2:
            if self.x-self.radius-xspeed < 0:
                self.xdirection = 1
                self.x += xspeed
            else:
                self.x -= xspeed

        # update y position and speed
        if self.ydirection == 1:
            distance = self.yspeed * 1 + 0.5 * acce # acce represents acceleration, could be altered!
            if self.y+distance+self.radius > 600:
                self.y = 600-self.radius
                self.ydirection = 2
                self.yspeed += acce
            else:
                self.y += distance
                self.yspeed += acce
        elif self.ydirection == 2:
            distance = self.yspeed * 1 - 0.5 * acce # acce represents accleration, could be altered!
            if self.y-distance-self.radius < 0:
                self.y = self.radius
                self.ydirection = 1
                self.yspeed = 0
            else:
                if self.yspeed < acce:
                    self.y -= distance
                    self.yspeed = 0
                    self.ydirection = 1
                else:
                    self.y -= distance
                    self.yspeed -= acce

class Bullet:
    def __init__(self, x): # x is the place where bullet is shot
        self.x = x
        self.y = 540

    def update(self):
        if self.y - 10 < 0:
            return False # the bullet is destroyed
        else:
            self.y -= 10 # the speed of bullet movement, could be altered!
            return True

class Buff:
    def __init__(self):
        where = random.randint(0, 27)
        self.x = buffLocation[where]
        self.y = 30
        temp = random.randint(1,3) # 1 for power buff 2 for rate buff
        self.type = "p"
        if temp == 1:
            self.type = "r"
        else:
            self.type = "p"
        self.radius = 5

class BallGame:
    def __init__(self): # initial interface
        
        self.window = Tk()
        self.window.title("game")
        self.window.maxsize(700,1000)
        
        self.labelTitle = Label(self.window, text = "Ball Game v1.0 by Gabriel Ham", width = 60, height = 1, font = "Times 16 bold") # title of game

        self.btNewGame = Button(self.window, text = "New Game", command = self.processGame, bg = "red", width = 20, height = 1, font = "Times 16 bold")
        self.btInstructions = Button(self.window, text = "Instructions", command = self.processInstructions, bg = "pink", width = 20, height = 1, font = "Times 16 bold")
        self.btHighScore = Button(self.window, text = "High Score", command = self.processHighScore, bg = "yellow", height = 1, width = 20, font = "Times 16 bold") 
        self.btCreator = Button(self.window, text = "Creator", command = self.processCreator, bg = "green", width = 20, height = 1, font = "Times 16 bold") 
        self.btExit = Button(self.window, text = "Exit", command = self.processExit, bg = "blue", width = 20, height = 1, font = "Times 16 bold")

        # packing main interface buttons
        self.labelTitle.pack(ipadx = 50, ipady = 50)
        self.btNewGame.pack(ipadx = 50, ipady = 50)
        self.btInstructions.pack(ipadx = 50, ipady = 50)
        self.btHighScore.pack(ipadx = 50, ipady = 50)
        self.btCreator.pack(ipadx = 50, ipady = 50)
        self.btExit.pack(ipadx = 50, ipady = 50)

        # a collection of variables
        self.point = IntVar() # current point indicator
        self.point = 0
        self.car_pos = IntVar() # current car coordinate, 300 for centered ranging from 30 to 570
        self.car_pos = 300
        # the car is a rectangle, centering at (car_pos, 570) which has a span of 30 pixels
        self.difficulty = DoubleVar() # represents the frequency of ball generation and number on balls
        self.difficulty = 1.0 # whenever touched an upgrade difficulty + 0.1
        self.firePower = IntVar() # how much damage each bullet does
        self.firePower = 1 # every upgrade touched + 0.5
        self.fireRate = DoubleVar() # how fast it shoots: 1 for 1 time every 0.1 seconds; 1.1 for one in ten shots give 2 bullets others 1
        self.fireRate = 1.0 # every upgrade + 0.2
        
        # loop for handling events
        self.window.mainloop()

    def processInstructions(self):
        tkinter.messagebox.showinfo("Instructions", "Move away from balls, use bullets to destroy them, pick up buffs, good luck!")

    # define processHighScore to display highscore list
    def processHighScore(self):

        # read file and get highscore
        file1 = open("highscore.txt", "r")
        name = []
        point = []
        for line in file1:
            temp = line.split()
            name.append(temp[0])
            point.append(temp[1])

        # invisiblize old window
        self.btNewGame.master.state("withdrawn") # set to "normal" to retrieve

        # display new window
        self.window2 = Tk()
        self.window2.title("High score")

        labelHigh = Label(self.window2, text = "High Score", width = 30, height = 2, font = "Times 14 bold")
        label1 = Label(self.window2, text = name[0] + "    " + point[0], bg = "red", width = 30, height = 2, font = "Times 14 bold")
        label2 = Label(self.window2, text = name[1] + "    " + point[1], bg = "yellow", width = 30, height = 2, font = "Times 14 bold")
        label3 = Label(self.window2, text = name[2] + "    " + point[2], bg = "blue", width = 30, height = 2, font = "Times 14 bold")
        btDone = Button(self.window2, text = "Done", command = self.processDone)

        labelHigh.pack(fill = "both", ipadx = 50, ipady = 50)
        label1.pack(fill = "both", ipadx = 50, ipady = 50)
        label2.pack(fill = "both", ipadx = 50, ipady = 50)
        label3.pack(fill = "both", ipadx = 50, ipady = 50)
        btDone.pack(fill = "both", ipadx = 50, ipady = 50)

        self.window2.mainloop()

        # redisplay the main interface
        self.btNewGame.master.state("normal")
        
        file1.close()
        

    def processCreator(self):
        tkinter.messagebox.showinfo("Creator", "This Ball Game v1.0 is created by Gabriel Ham")

    def processExit(self):
        self.window.quit()
        self.window.destroy()

    def processGame(self):

        # creating list of balls, bullets and buff
        self.ballList = [] # list of balls
        self.bulletList = [] # list of bullets
        self.buffList = [] # list of buffs

        self.sleepTime = 10 # refresh interval 100
        
        self.btNewGame.master.state("withdrawn") # set to "normal" to retrieve

        self.window3 = Tk() # create the game window
        self.window3.title("Game")
        self.window3.maxsize(600,630)

        self.labelPoint = Label(self.window3, text = "Point: " + str(self.point))
        self.canvas = Canvas(self.window3, bg = "white", width = 600, height = 600)

        self.labelPoint.pack(fill = "both")
        self.canvas.pack(fill = "both")

        self.canvas.bind("<Left>", self.processKeyA)
        self.canvas.bind("<Right>", self.processKeyD)
        self.canvas.focus_set()
        self.displayCar()


        self.animate()

        self.window3.mainloop()

    def processDone(self):
        self.window2.quit() # terminate high score display window
        self.window2.destroy() # invisiblize the highscore display window

    def processKeyA(self, event):
        self.car_pos = max(30, self.car_pos - 20)
        self.displayCar()

    def processKeyD(self, event):
        self.car_pos = min(570, self.car_pos + 20)
        self.displayCar()

    def displayCar(self):
        self.canvas.delete("car")
        self.canvas.create_rectangle(self.car_pos-30,540,self.car_pos+30,600, fill = "blue", tags = "car") # tag is car

    def animate(self): # self is the BallGame object here
        breakFlag = False
        time = 0
        while not breakFlag :
            self.canvas.after(self.sleepTime)
            self.canvas.update()
            time += 0.1 # update universal game time
            
            # handle car position update
            self.displayCar()

            # handle bullet position update
            for i in range(len(self.bulletList)-1, -1, -1):
                if self.bulletList[i].update() == False:
                    self.bulletList.pop(i)

            # handle ball position update
            for b in self.ballList:
                b.update()

            # test bullet touching ball conditions
            for i in range(len(self.bulletList)-1, -1, -1):
                for ball in self.ballList:
                    if dist(self.bulletList[i].x, self.bulletList[i].y, ball.x, ball.y) < ball.radius + 2:
                        self.point += self.firePower
                        ball.number -= self.firePower
                        self.bulletList.pop(i)
                        break
            self.labelPoint["text"] = "Point: " + str(self.point)

            # test bullet touching buff conditions
            for i in range(len(self.bulletList)-1, -1, -1):
                for j in range(len(self.buffList)-1, -1, -1):
                    if dist(self.bulletList[i].x, self.bulletList[i].y, self.buffList[j].x, self.buffList[j].y) < self.buffList[j].radius + 2:
                        print(self.fireRate)
                        if self.buffList[j].type == "p":
                            self.firePower += 0.5
                        elif self.buffList[j].type == "r":
                            self.fireRate += 0.2
                        self.bulletList.pop(i)
                        self.buffList.pop(j)
                        break

            # test for ball death and split
            for i in range(len(self.ballList)-1, -1, -1):
                if self.ballList[i].death():
                    if ball.tier == 1:
                        self.ballList.pop(i)
                    else:
                        temp = ball.maxnum / 2
                        self.ballList.append(Ball(ball.tier-1, temp))
                        self.ballList.append(Ball(ball.tier-1, temp))
                        self.ballList.pop(i)

            # test for ball hit car:
            for ball in self.ballList:
                if collision(ball.x-self.car_pos, ball.y-570, 60, 60, ball.radius):
                    self.endGame() 
                    breakFlag = True
                    break

            # generate new bullet:
            bulletAm = 0
            bulletAm += int(self.fireRate)
            temp = random.randint(1,10)
            if temp <= (self.fireRate - int(self.fireRate)) * 10:
                bulletAm += 1
            if bulletAm % 2 == 1:
                start = int(self.car_pos - ((bulletAm - 1) / 2) * 10) # start position of bullets
                for i in range(start, start + 10 * bulletAm, 10):
                    self.bulletList.append(Bullet(i))
            elif bulletAm % 2 == 0:
                start = int(self.car_pos - 2 - ((bulletAm - 2) / 2) * 10) # start position of bullets
                for i in range(start, start + 10 * bulletAm, 10):
                    self.bulletList.append(Bullet(i))

            # draw new bullet
            self.canvas.delete("bullet")
            for b in self.bulletList:
                self.canvas.create_rectangle(b.x - 2, b.y - 2, b.x + 2, b.y + 2, tags = "bullet", fill = "blue")

            # generate new ball:
            temp = random.randint(1,4)
            if time % 15 <= 0.1:
                self.ballList.append(Ball(temp, int(time * 2 / temp)))

            # draw new ball
            self.canvas.delete("ball", "text")
            for b in self.ballList:
                if b.number <= 50:
                    self.canvas.create_oval(b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius, fill = "pink", tags = "ball")
                elif b.number <= 150:
                    self.canvas.create_oval(b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius, fill = "yellow", tags = "ball")
                elif b.number <= 500:
                    self.canvas.create_oval(b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius, fill = "green", tags = "ball")
                else:
                    self.canvas.create_oval(b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius, fill = "red", tags = "ball")
                
                self.canvas.create_text(b.x, b.y, text = str(b.number), font = "Times 14", tags = "text")
                

            # generate new buff:
            if time % 25 <= 0.1:
                self.buffList.append(Buff())

            # draw new buff
            self.canvas.delete("buff", "text2")
            for b in self.buffList:
                self.canvas.create_rectangle(b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius, fill = "green", tags = "buff")
                self.canvas.create_text(b.x, b.y, text = "buff", font = "Times 14", tags = "text2")

    def endGame(self):
        self.window3.quit()
        self.window3.destroy()

        # read file and get highscore
        file1 = open("highscore.txt", "r")
        name = []
        point = []
        for line in file1:
            temp = line.split()
            name.append(temp[0])
            point.append(temp[1])
        file1.close()

        if self.point >= eval(point[2]):
            names = tkinter.simpledialog.askstring("New High Score", "Wow! You did it so well! Enter your name")
            if self.point >= eval(point[0]):
                point[2] = point[1]
                name[2] = name[1]
                point[1] = point[0]
                name[1] = name[0]
                point[0] = self.point
                name[0] = names
            elif self.point >= eval(point[1]):
                point[2] = point[1]
                name[2] = name[1]
                point[1] = self.point
                name[1] = names
            else:
                point[2] = self.point
                name[2] = names
        else:
            tkinter.messagebox.showinfo("Game Report", "You scored " + str(self.point))

        file1 = open("highscore.txt", "r+")
        for i in range(3):
            file1.write(name[i] + " " + str(point[i]) + "\n")
        file1.close()
        # refresh game-tracking variables
        self.point = 0
        self.car_pos = 300
        self.firePower = 1 # every upgrade touched + 0.5
        self.fireRate = 1.0 #

        # restore the main interface
        self.btNewGame.master.state("normal") # set to "normal" to retrieve
    
BallGame()
