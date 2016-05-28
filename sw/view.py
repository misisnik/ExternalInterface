"""
display run
====================
.. moduleauthor:: Michal Sladecek <misisnik@gmail.com>
.. autoclass:: Display
.. autoclass:: Win
.. autofunction:: lib

"""
"""Top part of whole display software. There are mostly GUI commands"""

import os
import time

from control import Control
from window import GUI

class Win(object):
	"""
		class is under Display class
		main function of this class is creating and managing windows
		adding text and clear it
	"""
	def __init__(self, disp, win, opts):
		self.disp = disp
		self.win = win
		self.opts = opts

	def __set__(self, obj, value):
		"""
			in variable valus is text which has to show on display
		"""
		self.disp.font = self.opts['font']
		self.disp.text(value, [0, self.opts['rect'][0][1]], self.opts['alignment'][0], 1, 1)
		self.disp.rewrite()

	def clear(self):
		"""
			clear display
		"""
		self.disp.clearPartOfBuffer(self.opts['rect'], 0)
		self.disp.rewrite()

class Display(object):
	"""There are main library of display"""
	def __init__(self, orientation = 180):
		"""
			initialization for hw control and gui part
		"""
		self.window = GUI(orientation)	#window degree
		self.defineWin()
		self.control = Control(self.window)
		#self.control = MatrixOrbital(self.window, 'COM5')
		self.font = ['Arial', 10]
		#write on display first screen 
		self.rewrite()

	def defineWin(self):
		for win, opts in\
			[('main_win',   {'rect':      ((0, 0),  (192,64)),
				'font':      ['Arial', 10],
				'alignment': ('left', 'top')}),
			(	'status',     {'rect':      ((0, 0),  (192, 19)),
				'font':      ['Big', 12],
				'alignment': ('center', 'center')}),
			(	'message',    {'rect':      ((0, 20), (192, 44)),
				'font':      ['Arial', 10],
				'alignment': ('left', 'top')}),
			('error_win',  {'rect':      ((0, 45), (192, 64)),
			'font':      ['Tiny', 7],
			'alignment': ('left', 'top')})]:
			setattr(Display, win, Win(self, win, opts))

	def rotate(self, degree):
		"""
			rotate window
			input is just degree of rotating
		"""
		self.window.rotation = degree
		return True

	def rewrite(self):
		"""
			rewrite display from gui buffer
		"""
		return self.control.RewriteDisplay()

	def resetBuffer(self):
		"""
			reset (erase) window (GUI) buffer
		"""
		return self.window.reset()

	def clearPartOfBuffer(self, position = [[0,0], [192, 64]], fill = False):
		"""
			clear part of buffer
				position - [[x0,y0], [x1,y1]]
		"""
		return self.window.clear(position)

	def reset(self):
		"""
			Reset display - it means that reset array in window (gui) and those write via SPI
		"""
		return self.control.Reset()

	def image(self, img, position = [0, 0], reverse = False):
		"""
			add image to window buffer
				img - path of file
				reverse - reverse image
		"""
		self.window.addImage(img, position, reverse)

	def text(self, text, position = [0, 0], align = 'left', spacing = 1, fill = 1):
		"""
			add text to screen buffer
				text - string of text
				position - [x, y]
				align - left, center, right
				spacing - how many pixels has between lines
				fill - 1 px is ON 0 px is OFF
			font u can set before this function by variable
			Display.font = ['Arial', 10] -> means font name and font size
			and return number of total text lines, printed text - to height
		"""
		return self.window.addMultilineText(text, self.font[1], position[0], position[1], align, self.font[0], spacing, fill)

	def lineText(self, text, position = [0, 0], align = 'left', fill = 1, align_parameter = 0):
		"""
			add just one line text
				text - string of text
				position - [x, y] where we can start write
				align - left, center, right
				fill - 1 is that px is ON, 0 is that px is OFF
			this function return width and height in pixels of text
				return (width, height)
			also as usually font u can change beore this function by variable
			Display.font = ['Arial', 10] -> means font name and font size
		"""
		return self.window.addText(text, self.font[1], position[0], position[1], align, self.font[0], fill, align_parameter)

	def rectangle(self, position, fill = True):
		"""
			add rectangle to screen buffer
				position - [[x0, y0], [x1, y1]]
				fill - True -> is filled px, False -> is doesn't filled just borderline has
		"""
		return self.window.addRectangle(position[0], position[1], fill)

	def arc(self, position, first, second, fill = 1):
		"""
			add part of ellipse
		"""
		return self.window.addArc(first, second, position[0], position[1], fill)

	def ellipse(self, position, fill = True):
		"""
			add ellipse to screen buffer
				position - [[x0, y0], [x1, y1]]
				fill - True -> is filled px, False -> is doesn't filled just borderline has
		"""
		return self.window.addEllipse(position[0], position[1], fill)

	def line(self, position, width = 1, fill = 1):
		"""
			add line to screen buffer
				position - [[x0, y0], [x1, y1]]
				width - width of line (basicly height :D)
				fill - 1 px is ON, 0 px is OFF
		"""
		return self.window.addLine(position[0], position[1], width, fill)

	def point(self, position, fill = 1):
		"""
			add point to screen buffer
				position - array of (x,y) like [(x,y), (x,y), (x,y)] each point is just 1px width
				fill - 1 px is ON, 0 px is OFF
		"""
		return self.window.addPoint(position, fill)

	def textSize(self, text):
		"""
			this function returned width and height of text size in px
			example call: width, height = Display.textSize() ----- function return "(width, height)"
			font u can edit before this function by variable font -> Display.font = ["font name", font size in px]
		"""
		return self.window.getMultilineTextSize(text, self.font[1], self.font[0])

	def textLineSize(self, text):
		"""
			this function returned width and height of just one line of text in px
			return (width, height)
		"""
		return self.window.getTextSize(text, self.font[1], self.font[0])

	def joystick(self):
		"""
			this function maintenance of joystick
			return is: up, down, left, right, or center
		"""
		return self.control.Joystick()

	def buttons(self):
		"""
			this function case of 2 buttons OK and NG
		"""
		return self.control.Buttons()

	def readyButtons(self, data, s = '1'):
		"""
			this function trigger LED in OK and NG button
				data - 'OK' for ok, 'NG' for NG and 'BOTH' for BOTH
		"""
		if not s: s = '0'
		if data == 'OK':
			self.control.shift_register[3] = s
		elif data == 'NG':
			self.control.shift_register[2] = s
		elif data == 'BOTH':
			self.control.shift_register[2] = s
			self.control.shift_register[3] = s

		self.control.SetShiftRegister()

	def sound(self, data):
		"""
			this function trigger BUZZER
		"""
		if data == 'a':
			self.control.shift_register[4] = '1'
			self.control.shift_register[5] = '0'
			self.control.shift_register[6] = '0'
			self.control.shift_register[7] = '0'
		elif data == 'b':
			self.control.shift_register[4] = '0'
			self.control.shift_register[5] = '1'
			self.control.shift_register[6] = '0'
			self.control.shift_register[7] = '0'
		elif data == 'c':
			self.control.shift_register[4] = '0'
			self.control.shift_register[5] = '0'
			self.control.shift_register[6] = '1'
			self.control.shift_register[7] = '0'
		elif data == 'd':
			self.control.shift_register[4] = '0'
			self.control.shift_register[5] = '0'
			self.control.shift_register[6] = '0'
			self.control.shift_register[7] = '1'
		else:
			self.control.shift_register[4] = '0'
			self.control.shift_register[5] = '0'
			self.control.shift_register[6] = '0'
			self.control.shift_register[7] = '0'
		self.control.SetShiftRegister()


	def led(self, status):
		"""
			this function care about led
				status - True or False
		"""
		return self.control.setErrorLed(status)

	def title(self, title):
		"""
			add title to function
				title - title text
		"""
		self.font = ['Arial', 10]
		title_width, title_height = self.lineText(title, [0, 0], 'center')
		self.line([[0,title_height + 2], [self.window.display_width, title_height + 2]], 2)

	def menu(self, title, data):
		"""
			Menu function - create menu part
			inputs are:
				- string of menu item
				- array with menu items like ['item 1', 'item 2', 'item 3']
			function jus return key of choosen menu items
		"""
		#set font for menu
		self.font = ['Arial', 10]

		#variables
		menu_selected = 0		#selected imtem in menu
		while 1:
			counter = 0
			menu_count = 0			#actual
			#add menu title and underline 2x
			self.title(title)
			#helper
			if menu_selected > len(data) - 1 :
				menu_selected = len(data) -1
			if menu_selected < 2:
				counter = 0
			elif menu_selected > len(data) - 2 :
				counter = menu_selected - 2
			else:
				counter = menu_selected - 1
			#draw data on menu list
			for m in range(0,3): #just 3 files per page
				try:
					if menu_selected < 2:
						item = data[m]
					elif menu_selected > len(data) - 2:
						item = data[menu_selected -2  + m]
					else:
						item = data[menu_selected -1  + m]
				except:
					#end of line - exception - no more menu :D
					break
				#and finally create menu
				fill = True
				if menu_selected == counter:
					w,h = self.textLineSize(item)	#get size of item
					fill = False
					#add background rectangle
					self.rectangle([[0, 20+(menu_count*12)], [self.window.display_width, 20+(menu_count*12)+(h+1)]])

				#add text which could be multiline
				self.text(item, [0, 20+(menu_count*12)], 'center', 1, fill)
				counter += 1
				menu_count += 1
			self.rewrite()
			#get joystick seting
			joystick_old = self.joystick()
			while 1:
				new_joystick = self.joystick()
				if joystick_old != new_joystick or new_joystick:
					break
				#time.sleep(0.1)
			#joystick setting
			if new_joystick == 'up':
				menu_selected -= 1
			elif new_joystick == 'down':
				menu_selected +=1
			elif new_joystick == 'center':
				return menu_selected	#return choosed item...
			#finally check selected menu
			if menu_selected >= len(data):
				menu_selected = len(data) - 1
			elif menu_selected < 0:
				menu_selected = 0
			#and reset window -> erase window in GUI part
			self.resetBuffer()

	def textArea(self, text, position = [0, 0], align = "left", percent_style = False):
		"""
			Create text area into gui buffer -> it can be more pages, and its remote by joystick
				text - multiline text string
				position - [x, y]
				align - left, center, right
		"""
		self.readyButtons('BOTH')
		printed_text = text
		per_page = 0
		text_array  = []
		c = 0
		while 1:
			self.resetBuffer()
			lines, printed_lines, printed = self.text(printed_text, [0, 0], 'center')

			if text_array == []:
				text_array = printed
				per_page = printed_lines

			#print line
			self.rectangle([[0,59],[192,63]], False)
			#filling
			if percent_style:
				self.rectangle([[-1,60], [int((192/len(text_array))*(c + printed_lines)), 62]])
			else:
				self.rectangle([[int((192/len(text_array))*c), 60], [int((192/len(text_array))*(c + printed_lines)), 62]])
			self.rewrite()

			#parse new text 
			while 1:
				joy = self.joystick()
				#can down
				if self.buttons() == 'BOTH':
					return self.readyButtons('BOTH', False)
				if (c + printed_lines) < len(text_array):
					if joy == 'down' or joy == "right":
						c += printed_lines
						break
				#can up
				if c > 0:
					if joy == 'up' or joy == "left":
						c -= printed_lines
						if c < 0:
							c = 0
						break
				time.sleep(0.1)
			printed_text = " ".join(text_array[c: c + per_page])

	def selectNumber(self, title, start, step):
		"""
			selecting number from x step is step
				from
				step
			returned value of choosen number
		"""
		choosen = start
		while 1:
			self.resetBuffer()
			self.title(title)
			self.rectangle([[71, 20], [121, 55]])
			rectangle_width = 50

			win = (192 - rectangle_width) / 2
			#and two lines
			self.line([[0,29],[192 ,29]], 2)
			self.line([[0,45],[192 ,45]], 2)
			self.line([[win / 2,29],[win / 2 ,45]], 1)
			self.line([[win + rectangle_width + (win /2 ),29],[win + rectangle_width + (win / 2) ,45]], 1)

			self.font = ['Arial', 7]
			self.lineText(str('-{0}'.format(int(10/step) * step)), [0, 13], "center")
			self.lineText(str('+{0}'.format(int(10/step) * step)), [0, 56], "center")

			#show choosen 
			self.font = ['Arial', 17]
			choosen_width, choosen_height = self.lineText(str(choosen), [0,29], "center", 0)
			self.font = ['Arial', 10]

			count = 0
			for i in range(choosen - (2 * (step)), choosen + (step * 6), step):
				if choosen == i or i < 0 :
					continue
				tw, th = self.textLineSize(str(i))
				if i < choosen:
					if (i + step) != choosen:
						#first
						pos = ((win / 2) / 2) - (tw / 2)
					else:
						#second
						pos = (win/2) + 2 + ((win / 2) / 2) - (tw / 2)
				else:
					count +=1
					if (i - step) == choosen:
						#next one - after choosen
						pos = win + rectangle_width + 2 + ((win / 2) / 2) - (tw / 2)
					else:
						#second
						pos = win + rectangle_width + (win/2) + 2 + ((win / 2) / 2) - (tw / 2)
				self.lineText(str(i), [pos, 33])
				if count == 2:
					break
			self.rewrite()

			#joystick
			while 1:
				joy = self.joystick()
				if joy == "center":
					return choosen
				elif joy == "left" and choosen > start:
					choosen -= step
					break
				elif joy == "right":
					choosen += step
					break
				elif joy == "up" and choosen > 10:
					choosen -= int(10/step) * step
					break
				elif joy == "down":
					choosen += int(10/step) * step
					break
				time.sleep(0.005)

	def selectNumber2(self, title, start, step):
		"""
			selecting number 2 format -  from x step is step
				from
				step
			returned value of choosen number
		"""
		choosen = start
		while 1:
			self.resetBuffer()

			self.rectangle([[116, 17], [166, 48]])

			self.rectangle([[122, 0], [160, 18]], 0)
			self.rectangle([[122, 47], [160, 63]], 0)
			self.rectangle([[90, 20], [117, 45]], 0)
			self.rectangle([[165, 20], [191, 45]], 0)

			#and two lines
			self.font = ['Arial', 15]
			self.lineText('Select \nnumber', [0, 15], "left")
			self.font = ['Arial', 10]
			self.lineText(str('-{0}'.format(int(10/step) * step)), [0, 5], "center", align_parameter = 45)
			self.lineText(str('+{0}'.format(int(10/step) * step)), [0, 50], "center", align_parameter = 45)
			self.lineText(str('-{0}'.format(step)), [0, 27], "center", align_parameter = 10)
			self.lineText(str('+{0}'.format(step)), [0, 27], "right", align_parameter = -6)
			#show choosen 
			self.font = ['Arial', 17]
			choosen_width, choosen_height = self.lineText(str(choosen), [0,25], "center", 0, align_parameter = 45)
			self.font = ['Arial', 10]

			count = 0

			self.rewrite()

			#joystick
			while 1:
				joy = self.joystick()
				if joy == "center":
					return choosen
				elif joy == "left" and choosen > start:
					choosen -= step
					break
				elif joy == "right":
					choosen += step
					break
				elif joy == "up" and choosen > 10:
					choosen -= int(10/step) * step
					break
				elif joy == "down":
					choosen += int(10/step) * step
					break
				time.sleep(0.005)

	def question(self, text):
		"""
			add function to rendering question on display
				text - question text
			return is True when answer is OK or False when answer is NG
		"""
		self.resetBuffer()
		self.font = ['Arial', 11]
		question_width, question_height = self.lineText(text, [3, 25])

		self.font = ['Arial', 12]
		#button OK
		self.rectangle([[150,0],[192,20]], False)
		self.rectangle([[153,3],[192,17]], False)
		self.line([[150,0],[153,3]], 1)
		self.line([[150,20],[153,17]], 1)

		self.lineText('OK', [164, 4])
		#button NG
		self.rectangle([[150,43],[192,63]], False)
		self.rectangle([[153,46],[192,60]], False)
		self.line([[150,43],[153,46]], 1)
		self.line([[150,63],[153,60]], 1)
		self.lineText('NG', [164, 47])
		self.rewrite()

		#set buttons
		self.readyButtons('BOTH')
		while 1:
			#load buttons and w8 for push OK or NG
			buttons = self.buttons()
			if buttons in ['OK', 'NG']:
				self.readyButtons('BOTH', False)
				return buttons
			time.sleep(0.1)

	def checkbox(self, title, data):
		"""
			add checkboxs from data
			data - array of checkbox example: ['Question 1', 'Question 2', 'Question 3']
			return array of true or false example [True, False, False]....
			press center button to send
		"""
		position = 0
		page = 0
		self.readyButtons('OK')
		data_result = [False] * len(data)
		while 1:
			self.resetBuffer()
			self.title(title)
			self.textSize =  ['Arial', 10]

			for i in range(3):
				if position + i > len(data):
					break
				p = (i * 12)
				actual = int(position -1/3) + i
				if position - 1 < len(data) and position > 0 and i == 1:
					self.rectangle([[-1, 18 + p], [192, 28 + p]], False)
				elif position == 0 and i == 0:
					self.rectangle([[-1, 18 + p], [192, 28 + p]], False)

				#checkbox
				self.rectangle([[1,20 + p], [7,26 + p]], False)
				self.lineText(data[actual], [9,17 + p])
				#checked
				if data_result[actual] == True:
					self.line([[1,20 + p], [7,26 + p]], 1)
					self.line([[7,20 + p], [1,26 + p]], 1)
			self.rewrite()
			#joystick
			while 1:
				if self.buttons() == 'OK':
					self.readyButtons('OK', False)
					return data_result
				joy = self.joystick()
				if joy == 'up' and position > 0:
					position -= 1
				elif joy == 'down' and position + 1 < len(data):
					position += 1
				elif joy == 'center':
					data_result[position] = not data_result[position]
				else:
					time.sleep(0.1)
					continue
				break

	def circleLoader(self, title,  fill = 0):
		"""
			widget for circle circleLoader
				title - title
				fill - percent of filling
		"""
		pos = [129,0]
		self.resetBuffer()
		self.ellipse([[pos[0] + 0, 0], [pos[0] + 63, 63]], 0)
		self.ellipse([[pos[0] + 5, 5], [pos[0] + 58, 58]], 0)

		show = ((fill * 360)/100) - 90
		self.arc([[pos[0] + 2, 2], [pos[0] + 61, 61]], -90, show, 1)
		self.arc([[pos[0] + 3, 3], [pos[0] + 60, 60]], -90, show, 1)

		self.font = ['Arial', 20]
		self.lineText("{0}%".format(fill), [0, 20], "center", align_parameter = 66)

		self.lineText(title, [0, 20], "left")

		self.rewrite()

	def rectangleLoader(self, title, fill = 0):
		"""
			widget for rectangle loader
				title - title
				fill - percent of filling
		"""
		self.resetBuffer()
		self.title(title)
		self.rectangle([[3,40],[188,60]], 0)
		show = ((fill * 183)/100)
		self.rectangle([[4,41],[show+4,59]], 1)
		self.font = ['Arial', 10]
		self.lineText("{0}%".format(fill), [0, 26], 'center')
		self.rewrite()

	def quantity(self, title, pieces, done = 0, percent_line = True):
		"""
			widget for revew quantity blocks
				pieces - how manny pieces are in line
				done - how many pieces is filled (done)
				percent_line - show recangle in percent line
		"""
		if done>pieces:
			return False
		self.resetBuffer()
		self.title(title)
		self.rectangle([[-1,40],[192,60]], 0)

		self.font = ['Arial', 17]
		self.lineText("{0}/{1}".format(done,pieces), [0, 20], "center")

		if percent_line:
			pos = int((((done * 100)/pieces)/100)*192)
			self.rectangle([[0, 41],[pos,59]], 1)
		piece = int(192/pieces)
		for i in range(done):
			self.rectangle([[(i*piece),41],[(i*piece) + piece, 59]], 1)
		self.rewrite()

	def test(self):
		"""
			just main part of this class - usually add text and so on.... for testing
		"""
		self.readyButtons('BOTH')
		while 1:
			for i in range(ord('a'), ord('d')):
				self.sound(chr(i))
				time.sleep(0.1)
			if self.buttons() == 'BOTH':
				self.sound(False)
				break
		self.readyButtons('BOTH', False)
		self.window.addImage()
		self.rewrite()


import random
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

display = Display()

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
	display.image("{0}/img/vut_logo.bmp".format(ph))
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
