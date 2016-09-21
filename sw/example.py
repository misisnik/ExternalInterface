import os
import time
import sys
import random
from display import Display
from tkinter import *

class Snake(object):
    def __init__(self, display):
        self.display = display
        self.array = []
        #buffering array
        # 0 is space
        # 1 is snakes head
        # 2,3,4... is snake
        # f is food
        # b is border
        self.defineArray()

        #push snake on the middle
        self.array[10][53] = 1 #head
        self.array[10][52] = 2 #head
        self.array[10][51] = 3 #head
        self.array[10][50] = 4 #head

        self.snakeLenght = 4
        self.direction = "right"

    def defineArray(self):
        #set borderline
        for r in range(32): #64
            self.array.append([0]*96) #192
            for c in range(96): #192
                if r == 0 or r == 31 or c == 0 or c == 95: # 63 191
                    self.array[r][c] = "b"
                else:
                    self.array[r][c] = 0
        self.generateFood()


    def generateFood(self):
        while 1:
            food_position_x = random.randint(2,93) # 190
            food_position_y = random.randint(2,28) # 62
            if self.array[food_position_y][food_position_x]  == 0:
                #put food
                self.array[food_position_y][food_position_x] = "f"
                break

    def redrawDisplay(self):
        #just add point
        self.display.resetBuffer()
        self.display.rectangle([[0,0],[191,63]], False)
        self.display.rectangle([[1,1],[190,62]], False)
        for row, r in enumerate(self.array):
            for cell, c in enumerate(r):
                if c != 'b' and c != 0:
                    #self.display.point([cell, row])
                    self.display.rectangle([[(cell) * 2,(row) * 2],[(cell + 1)  * 2,(row + 1) * 2]], False)
        self.display.rewrite()

    def move(self):
        def get(param):
            for row, i in enumerate(self.array):

                try:
                    return([i.index(param), row])
                except:
                    continue

        def recalculate():
            #we know that snake is self.snakeLenght point length
            for i in range(2, self.snakeLenght+1):
                #first we have to find snake body by id in i
                body = get(i)
                #now change body - we have to search p
                pointer = get('p')
                self.array[pointer[1]][pointer[0]] = i
                if body == None:
                    break
                if i == self.snakeLenght:
                    self.array[body[1]][body[0]] = 0
                else:
                    self.array[body[1]][body[0]] = 'p'

        def isFood(position):
            if (self.array[position[0]][position[1]] == 'f'):
                #snake ate food
                self.array[position[0]][position[1]] = 0
                self.generateFood()
                self.snakeLenght += 1

        head = get(1) #x and y position snakes head is 1
        #move by direction
        if self.direction == "right":
            #we have to move to right
            isFood([head[1], head[0]+1])
            if self.array[head[1]][head[0]+1] == 0: #192
                # we can move to right
                self.array[head[1]][head[0]+1] = self.array[head[1]][head[0]]
                self.array[head[1]][head[0]] = 'p' #set pointer next next to head
            else:
                return False

        elif self.direction == "left":
            #we have to move to right
            isFood([head[1], head[0]-1])
            if self.array[head[1]][head[0]-1] == 0:
                # we can move to right
                self.array[head[1]][head[0]-1] = self.array[head[1]][head[0]]
                self.array[head[1]][head[0]] = 'p' #set pointer next next to head
            else:
                return False

        elif self.direction == "up":
            #we have to move to right
            isFood([head[1]-1, head[0]])
            if self.array[head[1]-1][head[0]] == 0:
                # we can move to right
                self.array[head[1]-1][head[0]] = self.array[head[1]][head[0]]
                self.array[head[1]][head[0]] = 'p' #set pointer next next to head
            else:
                return False

        elif self.direction == "down":
            #we have to move to right
            isFood([head[1]+1, head[0]])
            if self.array[head[1]+1][head[0]] == 0:
                # we can move to right
                self.array[head[1]+1][head[0]] = self.array[head[1]][head[0]]
                self.array[head[1]][head[0]] = 'p' #set pointer next next to head
            else:
                return False
        #and move
        recalculate()
        return True

    def control(self):
        dr = self.display.joystick()
        if dr:
            if dr == 'center':
                self.move()
                self.move()
            elif (self.direction == 'right' and dr != 'left') or (self.direction == 'up' and dr!= 'down') or (self.direction == 'left' and dr != 'right') or (self.direction == 'down' and dr != 'up'):
                self.direction = dr

display = Display(orientation = 0)
def game():
    for i in range(11):
        display.rectangleLoader('Snake loader', fill = i*10)

    while 1:
        display.resetBuffer()
        menu_choosed = display.menu("Snake", ["Spustit hru", "Ovládání", "Ukončit hru"])
        if menu_choosed == 0:
            snake = Snake(display)

            display.readyButtons('BOTH')
            while 1:
                if display.buttons() == 'BOTH':
                    display.readyButtons('BOTH', False)
                    break
                snake.redrawDisplay()
                snake.control()
                if not snake.move():
                    #game over
                    display.resetBuffer()
                    display.status = "GAME OVER"
                    display.message = " Your score: {0}".format(snake.snakeLenght - 4)
                    display.error_win = " For retry -press green button, for exit press read"
                    display.led(True)
                    display.sound('a')
                    display.sound(False)
                    display.sound('b')
                    display.sound(False)
                    display.sound('a')
                    display.sound(False)
                    display.sound('c')
                    display.sound(False)
                    display.readyButtons('BOTH')
                    while 1:
                        if display.buttons() == 'OK':
                            snake.__init__(display)

                            br = False
                            break

                        elif display.buttons() == 'NG':
                            display.readyButtons('BOTH', False)
                            br = True
                            break
                    display.led(False)
                    if br == True:
                        break

        elif menu_choosed == 1:
            text = "Snake is controlling via joystick. If joystick is pressed, snake is faster. To exit game and this help just press both of buttons."
            display.textArea(text)
            display.resetBuffer()
        elif menu_choosed == 2:
            return

def help():
    display.font = ['Arial', 10]
    text = "Menu is controlling via joystick and buttons. For leave this help pres both of buttons."
    display.textArea(text)

from datetime import datetime
def clock():
    display.readyButtons('BOTH')
    while 1:
        display.resetBuffer()
        tm = datetime.now().strftime('%H:%M:%S')
        display.font = ['Arial', 45]
        display.lineText(tm, [0, 7], align = 'center')
        display.rewrite()
        #to menu
        if display.buttons() == 'BOTH':
            display.readyButtons('BOTH', False)
            return True

import os

def logo():
    display.readyButtons('BOTH')
    display.resetBuffer()
    ph = os.path.dirname(os.path.realpath(__file__))
    display.image("{0}/display/img/alps_logo.bmp".format(ph))
    display.rewrite()
    while 1:
        #to menu
        if display.buttons() == 'BOTH':
            display.readyButtons('BOTH', False)
            return True

def buzzer():
    #zapiskej
    tones = display.checkbox('Select tone',['Tone 1', 'Tone 2', 'Tone 3', 'Tone 4'])

    tones_data = ""
    for i in tones:
        if i:
            tones_data += '1'
        else:
            tones_data += '0'
    display.control.shift_register[4] = tones_data
    display.control.SetShiftRegister()
    time.sleep(2)
    display.control.shift_register[4:] = "0000"
    display.control.SetShiftRegister()

def restart():
    display.led(True)
    import os
    display.resetBuffer()
    display.fotn = ['Arial', 20]
    display.lineText('Coputer is restarting', align = 'center')
    display.rewrite()
    os.system("sudo reboot")

def off():
    display.led(True)
    import os
    display.resetBuffer()
    display.fotn = ['Arial', 20]
    display.lineText('Computer is going to off', align = 'center')
    display.rewrite()
    os.system("sudo poweroff")

def demo():
    while 1:
        menu_choosed = display.menu("Main menu", ["Helo", "Play game", "Show time", "Show picture", "Beep", "Stop demo"])
        if menu_choosed == 0:
            help()
        elif menu_choosed == 1:
            game()
        elif menu_choosed == 2:
            clock()
        elif menu_choosed == 3:
            logo()
        elif menu_choosed == 4:
            buzzer()
        elif menu_choosed == 5:
            display.reset()
            return

        display.resetBuffer()




def show_text(text, text_style, text_size):
    text = text.get("1.0",END)
    font = text_style.get()
    size = text_size.get()

    display.font = [font, int(size)]
    display.resetBuffer()
    display.text(str(text))
    display.rewrite()

master = Tk()
master.title('Aladin introduction software')
stitek=Label(master, text=u"Alladin test programme", font="Arial 10")
stitek.pack(padx=20, pady=10)




b = Button(master, text="Start introduction demo", command=demo)
b.pack()



f=Frame(master,height=1,width=300,bg="black")
f.pack(padx=20, pady=20)

stitek=Label(master, text=u"Send text into display", font="Arial 10")
stitek.pack()

text=Text(height=1, width=30)
text.pack(padx=20, pady=20)

#familly
text_style = StringVar(master)
text_style.set(u"Please choose font") # standardní hodnota

family = OptionMenu(master, text_style, "Arial", "Big", "Tiny", "Japan1", "Japan2", "Japan3")
family.pack()

#size
text_size = StringVar(master)
text_size.set(u"Please select font size") # standardní hodnota

size = OptionMenu(master, text_size, "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22")
size.pack()
b = Button(master, text="Show on Aladin display", command= lambda: show_text(text, text_style, text_size))
b.pack()

f=Frame(master,height=1,width=300,bg="black")
f.pack(padx=20, pady=20)


mainloop()