from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

	def reset(self):
		"""
			Reset all screen 
		"""
		self.data = ['0x00'] * 1536
		#create new image object
		image = Image.new('1', (192, 64))
		self.draw = ImageDraw.Draw(image)

	def getBitmap(self):
		"""
			Get finish picture which has to show on display - generating bitmap array
		"""
		dat = self.image.load()
		page = 0
		for i in range(0, 64):
			if i%8 == 0 and i != 0:
				page += 1
			for c in range(0, 192):
				d[(page * 192) + c] += str(dat[(c,i)])
		self.data = [int(i,2) for i in d]

	def addMultilineText(self, text, size = 10, x = 0, y = 0):
		"""
			Add multiline text to picture 
				text - data of text
				size - px size of letter
				x	 - x position
				y	 - y position
		"""
		#define font
		font = ImageFont.truetype('fonts/arial.ttf', size)
		self.changed = True
		self.draw.multiline_text((x,y), str(text), font=font, fill = 1, align = "left")

	def addText(self, text, size, x = 0, y = 0):
		"""
			Add text
		"""
		font = ImageFont.truetype('fonts/arial.ttf', size)
		self.changed = True
		self.draw.text((x,y), str(text), font=font, fill = 1, align = "left")	#can be draw.text....

	def addArc(self, start, end, x = [0, 0], y = [0, 0]):
		"""
			Add an arc (a portion of a circle outline) between the start and end angles, inside the given bounding box.
				start	-	starting angle in degrees
				end		-	ending angle in degrees
		"""
		self.changed = True
		self.draw.arc([x[0], y[0], x[1], y[1]], start, end, fill = 1)

	def addChord(self, start, end, x = [0, 0], y = [0, 0]):
		"""
			Same as addArc but the end points with a straight line
		"""
		self.changed = True
		self.draw.chord([x[0], y[0], x[1], y[1]], start, end, fill = 1)

	def addEllipse(self, fill = True, x = [0, 0], y = [0, 0]):
		"""
			Add ellipse
				fill == True then elipse is filled (1)
				fill == False then elipse is not filled (0)
				x 	 == array of x0 and x1
				y	 == array of y0 and y1
		"""
		self.changed = True
		self.draw.ellipse([x[0], y[0], x[1], y[1]], fill = fill, outline = not fill)

	def addLine(self, x = [0, 0], y = [0, 0], width = 0):
		"""
			Add line
				x = array of x0 and x1
				y = array of y0 and y1
				width = width of line
		"""
		self.changed = True
		self.draw.line([x[0], y[0], x[1], y[1]], fill = 1, width = width)

	def addPoint(self, position = [(0,0)]):
		"""
			Add points
				position array of (x,y) position of points
		"""
		self.changed = True
		self.draw.point(position, fill = 1)

	def addPolygon(self, position = [(0,0)], fill = True):
		"""
			Add polygon 
			The polygon outline consists of straight lines between the given coordinates, plus a straight line between the last and the first coordinate.
		"""
		self.changed = True
		self.draw.polygon(position, fill = fill, outline = not outline)

	def addRectangle(self, x = [0, 0], y = [0, 0], fill = True):
		"""
			Add rectangle 
		"""
		self.changed = True
		self.draw.rectangle([x[0], y[0], x[1], y[1]], fill = fill, outline = not fill)

	#finally get some information
	def getMultilineTextSize(self, text, size):
		"""
			get text size
		"""
		font = ImageFont.truetype('fonts/arial.ttf', size)
		return self.draw.multiline_textsize(str(text), font)

	def getTextSize(self, text, size):
		"""
			get text size
		"""
		font = ImageFont.truetype('fonts/arial.ttf', size)
		return self.draw.textsize(str(text), font)
