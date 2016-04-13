"""
terminal.matrix_orbital.matrix_orbital
======================================
.. moduleauthor:: Pavol Vargovcik <pallly.vargovcik@gmail.com>
.. autoclass:: MatrixOrbital
	:members:

"""
from serial import Serial
from threading import RLock
import time

# from .window  import Window
# from .buttons import ButtonListener
# from .leds    import Led
# from .fonts   import load_all_fonts, fonts

class SerialSafe(Serial):
	def __init__(self):
		self.mutex = RLock()
		self.bytecounter = 0
		Serial.__init__(self)

	def write(self, bs):
		self.mutex.acquire()
		if self.bytecounter >= 64:
			time.sleep(0.05)
			self.bytecounter = 0
		Serial.write(self, bs)
		self.bytecounter += len(bs)
		self.mutex.release()

	def write_unsafe(self, bs):
		Serial.write(self, bs)

class MatrixOrbital():
	"""
	Abstractiion of the serial commands from Matrix Orbital documentation into
	more human-friendly methods.

	:param port: path to the graphical terminal's serial interface character
	device file
	:type  port: :class:`str`

	"""
	def __init__(self, gui, port):
		try:
			self._ser = SerialSafe()
		except Exception as e:
			raise Exception('Failed to open USB chanel')
		self._ser.port         = port
		self._ser.baudrate     = 19200
		self._ser.timeout      = 1
		self._ser.writeTimeout = 1

		self._ser.open()
		#self.leds = tuple([Led(self._ser, n) for n in range(3)])
		self._handle_startup()
		self.gui = gui
		#self._fonts = fonts()

	def _handle_startup(self):
		"""
			initialization of the graphical terminal (set scrolling, font metrics, clear
			screen, initialize :class:`.ButtonListener`) after startup and reset
		"""
		#self._scroll = True
		#self.buttons = ButtonListener(self._ser)
		self._clear()
		#self.set_font_metrics()

	def RewriteDisplay(self):
		"""
			Rewrite display from buffer
			There are rewrite just not equals segments

			The display has 8 pages each is one write from buffer
		"""
		self.gui.getBitmap()
		self.write_bitmap(self.gui.data)

	def read_user_data(self):
		self._ser.write(b'\xFE\x35')
		return bytearray(self._ser.read(16))

	def write_user_data(self, data):
		assert len(data) == 16
		self._ser.write(b'\xFE\x34' + bytes(data))

	def write_bitmap(self, data):
		"""
			just write bitmap
		"""
		try:
			self._ser.write(b'\xFE\x64\x00\x00\xC0\x40' + bytes(data))
		except ValueError as e:
			#failed to open hid try to connect
			self.exceptionConnect()
			return write_bitmap(data)

	def Reset(self):
		"""
			send the reset command and wait while the grephical terminal resets
		"""
		self.buttons.stop()
		self.buttons.join()

		self._ser.flushInput()
		self._ser.write(b'\xFE\xFD\x4D\x4F\x75\x6E')
		assert self._ser.read(2) == b'\xFE\xD4'

		self._handle_startup()

	def Reverse(self):
		"""
			just reverse display
		"""
		return False

	def Joystick(self):
		"""
			Get status of joystick position
		"""
		#reset gpio -> load new values
		while 1:
			try:
				but = self._ser.read(1)
				print(but)
				if but == b'\x88':
					#central button
					return 'center'
				if but == b'C':
					#right
					return 'right'
				if but == b't':
					#left
					return 'left'
				if but == b'W':
					#up
					return 'up'
				if but == b'\xaa':
					#down
					return 'down'
				return False
			except ValueError as e:
				#failed to open hid try to connect
				self.exceptionConnect()
				#and try to again call this function
				return self.Joystick()

	def setErrorLed(self):
		"""
			set error leds
		"""
		return False

	def _clear(self):
		"""
			clear whole terminal (use :meth:`Terminal.main_win.clear` instead)
		"""
		self._ser.write(b'\xFE\x58')

	def close(self):
		"""
			stop :class:`.ButtonListener` and close the serial port
		"""
		self.buttons.stop()
		self.buttons.join()
		self._ser.close()

	def without_buttons(self, fn):
		self.buttons.stop()
		self.buttons.join()

		fn()
		self.buttons = ButtonListener(self._ser)

	def exceptionConnect(self):
		while 1:
			try:
				self.__init__(self.gui)
				#and rewrite display
				self.RewriteDisplay()
				break
			except Exception as e:
				print(e)
				time.sleep(1)
		return True
