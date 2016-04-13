"""Top part of whole display software. There are mostly GUI commands"""

from controll import Controll
from matrix_orbital import MatrixOrbital
from window import GUI
import time

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
	def __init__(self):
		"""
			initialization for hw controll and gui part
		"""
		self.window = GUI(180)	#window degree
		self.defineWin()
		self.controll = Controll(self.window)
		#self.controll = MatrixOrbital(self.window, 'COM5')
		self.font = ['Arial', 10]
		#write on display first screen 
		self.rewrite()

	def defineWin(self):
		for win, opts in\
			[('main_win',   {'rect':      ((0, 0),  (192,64)),
				'font':      ['Arial', 10],
				'alignment': ('left', 'top')}),
			(	'status',     {'rect':      ((0, 0),  (192, 19)),
				'font':      ['Arial', 10],
				'alignment': ('center', 'center')}),
			(	'message',    {'rect':      ((0, 20), (192, 44)),
				'font':      ['Arial', 10],
				'alignment': ('left', 'top')}),
			('error_win',  {'rect':      ((0, 45), (192, 64)),
			'font':      ['Arial', 10],
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
		return self.controll.RewriteDisplay()

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

	def lineText(self, text, position = [0, 0], align = 'left', fill = 1):
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
		return self.window.addText(text, self.font[1], position[0], position[1], align, self.font[0], fill)

	def rectangle(self, position, fill = True):
		"""
			add rectangle to screen buffer
				position - [[x0, y0], [x1, y1]]
				fill - True -> is filled px, False -> is doesn't filled just borderline has
		"""
		return self.window.addRectangle(position[0], position[1], fill)

	def elipse(self, position, fill = True):
		"""
			add elipse to screen buffer
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
		return self.controll.Joystick()

	def led(self, status):
		"""
			this function care about led
				status - True or False
		"""
		return self.controll.setErrorLed(status)

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

	def textArea(self, text, position = [0, 0], align = "left"):
		"""
			Create text area into gui buffer -> it can be more pages, and its remote by joystick
				text - multiline text string
				position - [x, y]
				align - left, center, right
		"""
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

			self.rectangle([[-1,60], [int((192/len(text_array))*(c + printed_lines)), 62]])

			self.rewrite()

			#parse new text 
			while 1:
				joy = self.joystick()
				#can down
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
		while 1:
			#load buttons and w8 for push OK or NG
			# buttons = self.buttons()
			# if buttons != None:
			# 	return buttons
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
				# if self.buttons():
				# 	return data_result
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

	def test(self):
		"""
			just main part of this class - usually add text and so on.... for testing
		"""
		pass

display = Display()

display.selectNumber("select number", 1 , 1)
display.textArea('Text bakalářské práce je tištěn jednostranně na bílé stránky kancelářského papíru formátu A4. Pro základní text se používá písmo Times New Roman velikosti maximálně 12 (minimálně 11 bodů). Okraje stránek se volí 25 mm ze všech stran textu s jednoduchým řádkováním. Velikost písma u nadpisů různých úrovní je použita podle standardních typografických doporučení, např. 24 bodů tučně v nadpisech hlavních kapitol, 14 bodů tučně v nadpisech podkapitol první úrovně, 12 bodů tučně v nadpisech druhé úrovně apod. Uspořádání jednotlivých částí textu musí být přehledné a logické. Je třeba odlišit názvy kapitol a podkapitol - píše se malými písmeny kromě velkých začátečních písmen. Jednotlivé odstavce textu jsou odsazeny mezerou, první řádek odstavce můžeme být odsazen vždy o stejnou, předem zvolenou hodnotu. ')
display.status = ("Status jak svina")
display.message = ("Message jak svina")
display.error_win = ("Error jak svina")
time.sleep(2)
for i in range(5000):
	display.message.clear()
	display.message ="aaaaa {0}".format(i)
	time.sleep(1)

