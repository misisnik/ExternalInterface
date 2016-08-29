import os
import time
import sys
import random

from display import Display

import random

# display.status= 'koniciva'
# display.message = 'koniciva'
# display.error_win = 'koniciva'

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
                    display.message = "Získaný počet bodů činí: {0}".format(snake.snakeLenght - 4)
                    display.error_win = "Pro spuštění hry stiskněte horní tlačítko, pro hlavní menu spodní tlačítko"
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
            text = "Had se ovládá natáčením joysticku do stran. Pokud joystick zamáčknete, had se bude posunovat rychleji. Po podržení rozsvícených tlačítek ukončíte hru, respektive i nápovědu."
            display.textArea(text)
            display.resetBuffer()
        elif menu_choosed == 2:
            return

def help():
    display.font = ['Arial', 10]
    text = "Následující text informuje o funkčnosti zařízení. Celkové ovládání se provádí za pomocí Joysticku. Pokud je zapotřebí ovládat tlačítky, vždy pro tuto možnost budete informováni jejich rozsvícením. Například pro odchod z nápovědy stačí současně zmáčknout obě rozsvícená tlačítka."
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
    display.image("{0}/display/img/vut_logo.bmp".format(ph))
    display.rewrite()
    while 1:
        #to menu
        if display.buttons() == 'BOTH':
            display.readyButtons('BOTH', False)
            return True

def buzzer():
    #zapiskej
    tones = display.checkbox('Zvolte tony',['Ton 1', 'Ton 2', 'Ton 3', 'Ton 4'])

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
    display.lineText('Počítač se restartuje', align = 'center')
    display.rewrite()
    os.system("sudo reboot")

def off():
    display.led(True)
    import os
    display.resetBuffer()
    display.fotn = ['Arial', 20]
    display.lineText('Počítač se vypíná', align = 'center')
    display.rewrite()
    os.system("sudo poweroff")

while 1:
    menu_choosed = display.menu("Hlavní nabídka", ["Nápověda", "Hrát hru", "Zobrazit hodiny", "Zobrazit obrázek", "Zapískat", "Restartovat počítač", "Vypnout počítač"])
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
        restart()
    elif menu_choosed == 6:
        off()

    display.resetBuffer()
