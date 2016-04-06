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
		#write on display first screen 
		self.controll.RewriteDisplay()

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

	def menu(self, title, data):
		"""
			Menu function - create menu part
			inputs are:
				- menu title
				- array with menu items like ['item 1', 'item 2', 'item 3']
			return is key of menu data
		"""
		#variables
		menu_selected = 0		#selected imtem in menu
		while 1:
			counter = 0
			menu_count = 0			#actual
			title_width, title_height = self.window.addText(title, 11, 0, 0, 'center')
			self.window.addLine([0,title_height + 2], [self.window.display_width, title_height + 2], 2)
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
					w,h = self.window.getTextSize(item, 10)
					fill = False
					self.window.addRectangle([0, 20+(menu_count*12)], [self.window.display_width, 20+(menu_count*12)+(h+1)])

				self.window.addMultilineText(item, 10, 0, 20+(menu_count*12), 'center', 'Arial', 1, fill)
				counter += 1
				menu_count += 1
			self.controll.RewriteDisplay()
			#get joystick seting
			joystick_old = self.controll.Joystick()
			while 1:
				new_joystick = self.controll.Joystick()
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
		while 1:
			self.window.addMultilineText('test jak svina \nahoj jak se mas jak jak se mas ja se mas mdlsam ldmal dmskla ah',9, 0, 0, 'center')
			self.window.addEllipse([0, 20], [50, 30], False)

			self.window.addLine([0,10],[100,10],2)

			#self.window.addArc(0,90,[0,10],[150,40])
			self.window.addChord(0,90,[0,10],[150,40])
			while 1:
				time.sleep(1)
				self.controll.Reverse(not self.controll.reverse)
				self.controll.RewriteDisplay()
				#self.window.addPolygon([(5,30),(100,30),(50,50)], False)
				#self.window.addRectangle([0,50], [40,60], False)

new = Display()
menu_title = "Menu title"
menu_data = ['Polozka cislo 1', 'Polozka cislo 2', 'Polozka cislo 3', 'Polozka cislo 4']
print(new.menu(menu_title, menu_data))
#new.test()
