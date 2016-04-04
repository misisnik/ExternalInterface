"""Top part of whole display software. There are mostly GUI commands"""

from controll import Controll
from window import GUI

class Display(object):
	"""There are main library of display"""
	def __init__(self):
		"""
			initialization for hw controll and gui part
		"""
		self.window = GUI()
		self.controll = Controll(self.window)
		#write on display first screen 
		self.controll.RewriteDisplay()

	def Reset(self):
		"""
			Reset display - it means that reset array in window (gui) and those write via SPI
		"""
		self.control.Reset()

	def main(self):
		"""
			just main part of this class - usually add text and so on.... for testing
		"""
		self.window.addText('Ahoj jak se mas', 15)
		#and rewrite screen
		self.controll.RewriteDisplay()

new = Display()
new.main()
