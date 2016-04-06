"""Top part of whole display software. There are mostly GUI commands"""

from controll import Controll
from window import GUI
import time

class Display(object):
	"""There are main library of display"""
	def __init__(self):
		"""
			initialization for hw controll and gui part
		"""
		self.window = GUI(180)	#window degree
		self.controll = Controll(self.window)
		self.font = ['Arial', 10]
		#write on display first screen 
		self.rewrite()

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
			title_width, title_height = self.lineText(title, [0, 0], 'center')
			self.line([[0,title_height + 2], [self.window.display_width, title_height + 2]], 2)
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
				time.sleep(0.1)
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

	def test(self):
		"""
			just main part of this class - usually add text and so on.... for testing
		"""
		pass

new = Display()
menu_title = "Menu title"
menu_data = ['Kratka polozka v menu 1', 'Nejake cislo 2', 'Hodne moc dlouhatanska polozka 3', 'Polozka cislo 4']
print(new.menu(menu_title, menu_data))
#new.test()
