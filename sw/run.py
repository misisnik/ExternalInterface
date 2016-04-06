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

	def Reset(self):
		"""
			Reset display - it means that reset array in window (gui) and those write via SPI
		"""
		self.control.Reset()

	def main(self):
		while 1:
			"""
				just main part of this class - usually add text and so on.... for testing
			"""
			self.window.addMultilineText('test jak svina \nahoj jak se mas jak jak se mas ja se mas mdlsam ldmal dmskla ah',9, 0, 0, 'center')
			self.window.addEllipse([0, 20], [50, 30], False)

			self.window.addLine([0,10],[100,10],2)

			#self.window.addArc(0,90,[0,10],[150,40])
			self.window.addChord(0,90,[0,10],[150,40])
			try:
				while 1:
					time.sleep(1)
					self.controll.Reverse(not self.controll.reverse)
					self.controll.RewriteDisplay()
				#self.window.addPolygon([(5,30),(100,30),(50,50)], False)
				#self.window.addRectangle([0,50], [40,60], False)
			except Exception as e:
				while 1:
					try:
						self.controll = Controll(self.window)
						#write on display first screen 
						self.controll.RewriteDisplay()
						break
					except:
						continue

new = Display()
new.main()
