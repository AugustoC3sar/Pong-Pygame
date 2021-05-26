from tkinter import *
from tkinter import messagebox
from threading import Thread
import time
import random


root = Tk()
root.title('PONG')

#defining
p1_score = 0
p2_score = 0
p1_position = [10,170,30,250]
p2_position = [570,170,590,250]
ball_position = [290,200,310,220]
move_direction = 'DR'
directions = ('DR','DL','TR','TL')
enable = 1


def move_player(event):
    global player1,player2
    global p1_y_position,p2_y_position
    global canvas
    if event.keysym == 'w':
        y1 = p1_position[1]
        y2 = p1_position[3]
        if y1 == 10:
            pass
        else:
            y1 -= 10
            y2 -= 10
        p1_position[1] = y1
        p1_position[3] = y2
        canvas.coords(player1,10,y1,30,y2)
    elif event.keysym == 's':
        y1 = p1_position[1]
        y2 = p1_position[3]
        if y2 == 410:
            pass
        else:
            y1 += 10
            y2 += 10
        p1_position[1] = y1
        p1_position[3] = y2
        canvas.coords(player1,10,y1,30,y2)
    elif event.keysym == 'Up':
        y1 = p2_position[1]
        y2 = p2_position[3]
        if y1 == 10:
            pass
        else:
            y1 -= 10
            y2 -= 10
        p2_position[1] = y1
        p2_position[3] = y2
        canvas.coords(player2,570,y1,590,y2)
    elif event.keysym == 'Down':
        y1 = p2_position[1]
        y2 = p2_position[3]
        if y2 == 410:
            pass
        else:
            y1 += 10
            y2 += 10
        p2_position[1] = y1
        p2_position[3] = y2
        canvas.coords(player2,570,y1,590,y2)


def verifyBallColisions():
    global canvas
    global ball_position
    global p1_position,p2_position
    global p1_score,p2_score
    global move_direction
    bx1,by1,bx2,by2 = ball_position
    p1x1,p1y1,p1x2,p1y2 = p1_position
    p2x1,p2y1,p2x2,p2y2 = p2_position
    if by1 == 0:
        if move_direction == 'TR':
            move_direction = 'DR'
        elif move_direction == 'TL':
            move_direction = 'DL'
    elif bx2 == p2x1:
        if ((by1 in range(p2y1,p2y2+1)) or (by2 in range(p2y1,p2y2+1))):
            if move_direction == 'TR':
                move_direction = 'TL'
            elif move_direction == 'DR':
                move_direction = 'DL'
    elif by2 == 420:
        if move_direction == 'DL':
            move_direction = 'TL'
        elif move_direction == 'DR':
            move_direction = 'TR'
    elif bx1 == p1x2:
        if ((by1 in range(p1y1,p1y2+1)) or (by2 in range(p1y1,p1y2+1))):
            if move_direction == 'TL':
                move_direction = 'TR'
            elif move_direction == 'DL':
                move_direction = 'DR'
    elif bx1 == 600:
        p1_score += 1
        updateScores()
    elif bx2 == 0:
        p2_score += 1
        updateScores()


def ballMove():
    global move_direction
    global ball_position
    global canvas
    global enable
    while True:
        if enable == 1:
            time.sleep(0.1)
            if move_direction == 'TR':
                canvas.move(ball,10,-10)
            elif move_direction == 'DR':
                canvas.move(ball,10,10)
            elif move_direction == 'DL':
                canvas.move(ball,-10,10)
            elif move_direction == 'TL':
                canvas.move(ball,-10,-10)
            ball_position = canvas.coords(ball)
            verifyBallColisions()
        else:
            pass


def updateScores():
    global p1_score,p2_score
    global root
    global enable
    global ball_position
    ball_position = [290,200,310,220]
    enable = 0
    p1 = canvas.find_withtag('player1_score')
    canvas.itemconfig(p1,text=f'{p1_score}')
    p2 = canvas.find_withtag('player2_score')
    canvas.itemconfig(p2,text=f'{p2_score}')
    canvas.coords(ball,290,200,310,220)
    if p1_score == 5:
        restart = messagebox.askyesno('End Game','Game Over! Player 1 wins.\nPlay again?')
        if restart:
            resetGame()
        else:
            root.destroy()
    elif p2_score == 5:
        restart = messagebox.askyesno('End Game','Game Over! Player 2 wins.\nPlay again?')
        if restart:
            resetGame()
        else:
            root.destroy()
    else:
        root.after(1000,newDirection)


def newDirection():
    global move_direction
    global enable
    move_direction = random.choice(directions)
    enable = 1



def resetGame():
    global canvas
    global p1_position,p2_position
    global p1_score,p2_score
    global ball_position
    p1_score = 0
    p2_score = 0
    p1_position = [10,170,30,250]
    p2_position = [570,170,590,250]
    p1s = canvas.find_withtag('player1_score')
    p2s = canvas.find_withtag('player2_score')
    canvas.coords(player1,10,170,30,250)
    canvas.coords(player2,570,170,590,250)
    canvas.itemconfig(p1s, text=f'{p1_score}')
    canvas.itemconfig(p2s, text=f'{p2_score}')
    root.after(500,newDirection)


#canvas
canvas = Canvas(root, width=600,height=420, highlightthickness=0, bg='#000000')
player1 = canvas.create_rectangle(10,170,30,250, fill='#FFFFFF', tag='player1')
player2 = canvas.create_rectangle(570,170,590,250, fill='#FFFFFF', tag='player2')
canvas.create_line(300,0,300,420, fill='#FFFFFF')
canvas.create_text(280,20, text=f'{p1_score}', fill='#FFFFFF',font=('TkDefaultFont',24,'bold'),tag='player1_score')
canvas.create_text(320,20, text=f'{p2_score}', fill='#FFFFFF',font=('TkDefaultFont',24,'bold'),tag='player2_score')
ball = canvas.create_oval(290,200,310,220, fill='#FFFFFF')


#binding
canvas.bind_all('<Key>', move_player)


#on screen
canvas.grid(row=0,column=0)


#thread
ballThread = Thread(target=ballMove)
ballThread.daemon = True
ballThread.start()

root.resizable(0,0)
root.mainloop()
