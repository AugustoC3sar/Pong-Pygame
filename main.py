from tkinter import *


root = Tk()
root.title('PONG')

class Pong(Canvas):
    def __init__(self):
        super().__init__(width=600,height=420,bg='#111111',highlightthickness=0)
        self.p1_score = 0
        self.p2_score = 0
        self.players_y_positions = [[170,250],[170,250]]
        self.bind_all('<KeyPress>',self.player_move)

        self.create_objects()


    def create_objects(self):
        self.create_rectangle(10,170,30,250, fill='#FFFFFF', tag='player1')
        self.create_rectangle(570,170,590,250, fill='#FFFFFF', tag='player2')

        self.create_line(300,0,300,420, fill='#FFFFFF')
        self.create_text(280,20, text=f'{self.p1_score}', fill='#FFFFFF', font=('Helvetica', 25, 'bold'))
        self.create_text(320,20, text=f'{self.p2_score}', fill='#FFFFFF',font=('Helvetica', 25, 'bold'))

    
    def player_move(self,event):
        if event.keysym == 'w':
            self.player1_move_top()
        elif event.keysym == 's':
            self.player1_move_bottom()


    def player1_move_top(self):
        currentPlayer = self.find_withtag('player1')
        y1,y2 = self.players_y_positions[0]
        y1 -= 10
        y2 -= 10
        self.coords(currentPlayer,10,y1,30,y2)
        root.after(500,self.player1_move_top)


    def player1_move_bottom(self):
        currentPlayer = self.find_withtag('player1')
        y1,y2 = self.players_y_positions[0]
        y1 += 10
        y2 += 10
        self.coords(currentPlayer,10,y1,30,y2)






mainScreen = Pong()
mainScreen.grid(row=0,column=0)



root.resizable(0,0)
root.mainloop()
