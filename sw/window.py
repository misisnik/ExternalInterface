from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

system_fonts = {'Arial' : 'arial.ttf'}
display_width = 192
display_height = 64

class GUI(object):
	"""
		There is class for support graphic part of display
	"""
	def __init__(self):
		"""
			inicialization of gui class
		"""
		#visualisation data - default is blank screen -> every px is off
		self.reset()
		self.changed = False

	def reset(self):
		"""
			Reset all screen 
		"""
		self.data = [0x00] * 1536
		#create new image object
		self.image = Image.new('1', (display_width, display_height))
		self.draw = ImageDraw.Draw(self.image)

	def getBitmap(self):
		"""
			Get finish picture which has to show on display - generating bitmap array
		"""
		d = [""]*1536
		dat = self.image.load()
		page = 0
		for i in range(0, 64):
			if i%8 == 0 and i != 0:
				page += 1
			for c in range(0, 192):
				d[(page * 192) + c] += str(dat[(c,i)])
		self.data = [int(i,2) for i in d]

	def addMultilineText(self, text, size = 10, x = 0, y = 0, align = "left", f = 'Arial', spacing = 1, fill = 1):
		"""
			Add multiline text to picture 
				text - data of text
				size - px size of letter
				x	 - x position
				y	 - y position
		"""
		#get width of text
		text_width, text_height = self.getMultilineTextSize(text, size, f)

		#multiline text - parse to more line
		if text_width > display_width:
			longest = 0
			lines = 0
			new_text = [""]
			for i in text:
				wn, hn = self.getMultilineTextSize(new_text[-1], size, f)
				if wn > display_width:
					#check if we're not in the midle of world
					last = new_text[-1]
					for count, l in enumerate(last[::-1]):
						if l == " ":
							break;
					if count > 0 and count < 10:
						del new_text[-1]
						new_text.append(last[0:len(last) - count])
						new_text.append(last[len(last) - count:])
					else:
						new_text.append("")

				if i == "\n":
					new_text.append("")
				else:
					new_text[-1] += i

			text = "\n".join(new_text)
			text_width, text_height = self.getMultilineTextSize(text, size, f)
		#align setting if is just 1line text -> smaller than display_width
		if text_width < display_width and x == 0:
			if align == "center":
				x = (display_width - text_width)/2
			elif align == "right":
				x = display_width - text_width

		#define font
		font = ImageFont.truetype('fonts/{0}'.format(system_fonts[f]), size)
		self.changed = True
		self.draw.multiline_text((x,y), str(text), font=font, fill = fill, align = align, spacing = spacing)

	def addText(self, text, size, x = 0, y = 0, align = "left", f = 'Arial', fill = 1):
		"""
			Add text
		"""
		#get width of text
		text_width, text_height = self.getTextSize(text, size, f)

		#align setting if is just 1line text -> smaller than display_width
		if text_width < display_width and x == 0:
			if align == "center":
				x = (display_width - text_width)/2
			elif align == "right":
				x = display_width - text_width

		text = textwrap.wrap(text, width=display_width)
		font = ImageFont.truetype('fonts/{0}'.format(system_fonts[f]), size)
		self.changed = True
		self.draw.text((x,y), str(text), font=font, fill = fill)	#can be draw.text....

	def addArc(self, start, end, first = [0, 0], second = [0, 0], fill = 1):
		"""
			Add an arc (a portion of a circle outline) between the start and end angles, inside the given bounding box.
				start	-	starting angle in degrees
				end		-	ending angle in degrees
		"""
		self.changed = True
		self.draw.arc([first[0], first[1], second[0], second[1]], start, end, fill = fill)

	def addChord(self, start, end, first = [0, 0], second = [0, 0], fill = 1):
		"""
			Same as addArc but the end points with a straight line
		"""
		self.changed = True
		self.draw.chord([first[0], first[1], second[0], second[1]], start, end, fill = fill)

	def addEllipse(self, first = [0, 0], second = [0, 0], fill = True):
		"""
			Add ellipse
				fill == True then elipse is filled (1)
				fill == False then elipse is not filled (0)
				first 	 == array of x0 and y0
				second	 == array of x1 and y1
		"""
		self.changed = True
		self.draw.ellipse([first[0], first[1], second[0], second[1]], fill = fill, outline = not fill)

	def addLine(self, first = [0, 0], second = [0, 0], width = 0, fill = 1):
		"""
			Add line
				first 	 == array of x0 and y0
				second	 == array of x1 and y1
				width = width of line
		"""
		self.changed = True
		self.draw.line([first[0], first[1], second[0], second[1]], fill = fill, width = width)

	def addPoint(self, position = [(0,0)], fill = 1):
		"""
			Add points
				position array of (x,y) position of points
		"""
		self.changed = True
		self.draw.point(position, fill = fill)

	def addPolygon(self, position = [(0,0)], fill = True):
		"""
			Add polygon 
			The polygon outline consists of straight lines between the given coordinates, plus a straight line between the last and the first coordinate.
		"""
		self.changed = True
		self.draw.polygon(position, fill = fill, outline = not fill)

	def addRectangle(self, first = [0, 0], second = [0, 0], fill = True):
		"""
			Add rectangle 
		"""
		self.changed = True
		self.draw.rectangle([first[0], first[1], second[0], second[1]], fill = fill, outline = not fill)

	#finally get some information
	def getMultilineTextSize(self, text, size, font):
		"""
			get text size
		"""
		font = ImageFont.truetype('fonts/{0}'.format(system_fonts[font]), size)
		return self.draw.multiline_textsize(str(text), font)

	def getTextSize(self, text, size):
		"""
			get text size
		"""
		font = ImageFont.truetype('fonts/{0}'.format(system_fonts[font]), size)
		return self.draw.textsize(str(text), font)
