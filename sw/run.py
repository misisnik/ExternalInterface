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
					if joy == 'down':
						c += printed_lines
						break
				#can up
				if c > 0:
					if joy == 'up':
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

new = Display()

new.checkbox('Checkbox test', ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6'])

#new.question("Are you OK ??")

# menu_title = "Menu title"
# menu_data = ['Kratka polozka v menu 1', 'Nejake cislo 2', 'Hodne moc dlouhatanska polozka 3', 'Polozka cislo 4']
# print(new.menu(menu_title, menu_data))
# #new.test()
# text = "From the very beginning of Android, Apple has been complaining that its Android competitors are ripping off its iPhone designs. Whether the culprit is the Samsung Galaxy S, the HTC One A9, or the ZTE Whatever, Apple is all too happy to remind the world that it's the leader and Android device makers are its followers. Well, things have been changing lately, and today's debut of the Huawei P9 adds momentum to a growing tide of distinctive new phones coming out of China — ones that aren't defined by a religious adherence to photocopying the iPhone. The Huawei P9 and the Xiaomi Mi 5 before it are the harbingers of a much more dangerous rival to Apple, a set of Chinese manufacturers capable of crafting their own, attractive, even premium designs.Don't get me wrong, I'm not here to argue that the entire mobile industry has suddenly developed scruples about ripping off Apple's design work. Just a glance or two at Oppo's F1 Plus or Meizu's Pro 5 will tell you that iPhone imitations are still very much alive and thriving. But the substantive change that's taken place in the mobile industry recently is the recognition of the paramount importance of high-quality industrial design. Xiaomi poured two years of development work into the Mi 5, while Huawei  outspent Apple on research and development last year by more than a billion dollars. Those investments are aimed at long-term technical innovations, an important subset of which is the development and refinement of standout designs. The P9 has a similar metal construction to the iPhone, but it feels different and, thanks to its idiosyncratic pair of camera eyes, looks different too.The copying of Apple has evolved. It's less literal now, as companies strive to recreate the essence of Apple's success, whether it be through vertical integration (as with Huawei and its in-house processor design), positive brand associations, or simple aesthetic and tactile appeal. Apple is still the Michael Jordan that every Chinese smartphone manufacturer looks up to, but instead of trying to dunk with their tongues sticking out or shoot fadeaway jumpers, these rising stars are developing their own ways of scoring points with consumers. Instead of imitating, they are emulating.There's no other way to interpret this development than as decidedly good news. Huawei has gone from routinely copying Sony's Xperia Z designs — culminating in the utterly anonymous Huawei P8 last year — to defining its own look and feel, as well as staking a claim for technological leadership with its unique camera setup. The dual-camera system on the Huawei P9 is not attempting to serve up fresh gimmicks, and is instead targeted at improving contrast, gathering more light, and generally making every photo look as good as it can possibly be. I'm not yet sure how well Huawei has executed this plan, but I can already say that the concept makes sense from a photographer's perspective and shows the right ambition to get ahead rather than chase from behind. Plus, Huawei is doing the whole two-camera trick without resorting to an unattractive camera wart. There's no Apple blueprint for making that happen, so what we're witnessing now is Huawei flexing its own engineering muscle."
# new.textArea(text)
print(new.selectNumber("Choose number", 1,2))
while 1:
	new.led(True)
	time.sleep(0.5)
	new.led(False)
	time.sleep(0.5)