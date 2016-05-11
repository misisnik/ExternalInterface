"""
display controll
====================
.. moduleauthor:: Michal Sladecek <misisnik@gmail.com>
.. autoclass:: Controll
.. autofunction:: lib

"""
from mcp2210.commands import ChipSettings, SPISettings, USBSettings
from mcp2210.device import MCP2210, CommandException
import numbers
import time
############################################
#main class
############################################
class Controll(object):
	def __init__(self, gui, register = ['0'] * 8):
		"""
			Authenticate and inicialization display for fast useing
		"""
		#display buffer
		self.display_buffer = [''] * 1536
		#spi buffer
		self.spi_buffer = ''
		#register buffer
		self.shift_register = register
		#reverse display variable
		self.reverse = False
		#last dc (latch) for display
		self.last_display_dc = False
		#first ve have to inicialization mcp2210
		self.init_mcp2210()
		#set shift register
		self.SetShiftRegister()
		#next is display ist3020 inicialization
		self.init_display()
		#gui
		self.gui = gui

	def init_mcp2210(self):
		"""inicialization of MCP2210 main chip which allow communication from system to display"""
		#self.communication = MCP2210(0x04D8, 0x00DE)
		try:
			self.communication = MCP2210(0x04D8, 0x00DE)
		except Exception as e:
			raise Exception('Failed to open USB chanel')

		#gpio local variables
		self._gpio = self.communication.gpio
		self._gpio_direction = self.communication.gpio_direction
		#other inicialization
		self.gpio_init()
		self.spi_init()



	def gpio_init(self):
		"""
			GPIO designations 	- 0x00 is GPIO, 0x01 is Chip selects, 0x02 is Dedicated function pin
			GPIO direction 		- 0x00 is Output, 0x01 is Input
		"""
		#designation
		gpio_settings = self.communication.chip_settings
		gpio_settings.pin_designations[0] = 0x00
		gpio_settings.pin_designations[1] = 0x00
		gpio_settings.pin_designations[2] = 0x00
		gpio_settings.pin_designations[3] = 0x01
		gpio_settings.pin_designations[4] = 0x00
		gpio_settings.pin_designations[5] = 0x00
		gpio_settings.pin_designations[6] = 0x00
		gpio_settings.pin_designations[7] = 0x00
		gpio_settings.pin_designations[8] = 0x00
		self.communication.chip_settings = gpio_settings
		#and also direction
		for i in range(0,9):
			if i == 0 or i == 1 or i == 4 or i == 5 or i == 6:
				self._gpio_direction[i] = 0x01
			else:
				self._gpio_direction[i] = 0x00
				self._gpio[i] = False

	def spi_init(self):
		"""
			SPI inicialization
		"""
		spi_settings = self.communication.transfer_settings
		spi_settings.bit_rate = 10000000
		spi_settings.idle_cs = 0b000001000		#idle of CE pins 0-8
		spi_settings.active_cs = 0b000000000	#active of CE pins 0-8
		spi_settings.spi_mode = 0x00 			#SPI mode could be 0x00, 0x01, 0x02
		spi_settings.interbyte_delay = 0
		spi_settings.cs_data_delay = 0
		spi_settings.lb_cs_delay = 0
		self.communication.transfer_settings = spi_settings

	def init_display(self):
		"""
			Inicialization of ist3020 display
		"""
		self.WriteCommand(0xE2, True)	#Sw reset
		time.sleep(0.01)
		self.WriteCommand(0xab)			#Built-in Oscillator ON
		self.WriteCommand(0xa0)			#s1-s132    
		self.WriteCommand(0xc8)			#c64-c1
		self.WriteCommand(0xa2)			#1/9bias
		self.WriteCommand(0x2c)			#VC ON
		self.WriteFromBuffer()		#Finally write whole packet from SPI buffer
		time.sleep(0.01)
		self.WriteCommand(0x2e, True)	#VR ON - fast write command
		time.sleep(0.01)
		self.WriteCommand(0x2f, True)	#VF ON - fast write command
		time.sleep(0.01)
		self.WriteCommand(0x20)			#Regulor_Resistor_Select
		self.WriteCommand(0x81)			#Set Reference Voltage Select Mode
		self.WriteCommand(45)			#Set Reference Voltage Register
		self.WriteCommand(0x70)			#External capacitor
		self.WriteCommand(0x40)			#Set start line
		self.WriteCommand(0xaf)			#Display on
		self.WriteCommand(0x90)
		self.WriteCommand(0x00)
		self.WriteCommand(0xa6)
		self.WriteCommand(0xa4)
		self.WriteFromBuffer()			#Finally write whole packet from SPI buffer


	def WriteCommand(self, data, fast = False):
		"""
			Write commands data to ist3020 display
			if variable fast is True then the data going to send without buffering
		"""
		#Set DC low for command
		if self.last_display_dc != False:
			self._gpio[2] = False
			self.last_display_dc = False
		#Convert scalar argument to list so either can be passed as parameter.
		if isinstance(data, numbers.Number):
			data = [data & 0xFF]
		#sending data
		self.WriteByte([chr(x) for x in data], fast)

	def WriteData(self, data, fast = False):
		"""
			Write data to ist3020 display
			if variable fast is True then the data going to send without buffering
		"""
		# Set DC low for command, high for data.
		if self.last_display_dc != True:
			self._gpio[2] = True
			self.last_display_dc = True
		# Convert scalar argument to list so either can be passed as parameter.
		if isinstance(data, numbers.Number):
			data = [data & 0xFF]
		#sending data
		self.WriteByte([chr(x) for x in data], fast)

	def WriteByte(self, data, fast = False):
		"""
			If variable fast is True then send now (without buffering) else buffering data until called funtion WriteFromBuffer
		"""
		if fast:
			try:
				self.communication.transfer("".join(data))
			except ValueError as e:
				self.exceptionConnect()
				time.sleep(0.5)
				#and try again
				self.WriteByte(data, fast)

		else:
			self.spi_buffer += "".join(data)

	def WriteFromBuffer(self):
		"""
			Write data from buffer
		"""
		try:
			self.communication.transfer(self.spi_buffer)
		except ValueError as e:
			self.exceptionConnect()
			time.sleep(0.5)
			#and try again
			self.WriteFromBuffer()

		self.spi_buffer = ''

	def SetPageAddress(self, data):
		"""
			Set page address of 192x64px display -> in ist3020
		"""
		address=0xb0|data
		self.WriteCommand(address)

	def SetColumnAddress(self, data):
		"""
			Set column address of 192x64px display -> in ist3020
		"""
		self.WriteCommand((0x10|(data>>4)))
		self.WriteCommand((0x0f&data))

	def RewriteDisplay(self):
		"""
			Rewrite display from buffer
			There are rewrite just not equals segments

			The display has 8 pages each is one write from buffer
		"""
		if self.gui.changed:
			self.gui.getBitmap()	#get new bitmap of gui
			self.gui.changed = False

		picture = self.gui.data[::-1]
		#dooo
		for i in range(0, 0x08):
			#compare page with buffer
			if self.display_buffer[i*192:i*192+192] == picture[i*192:i*192+192]:
				continue
			#compare columns with buffer
			start = 0
			end = 192
			for c in range(192):
				if picture[i*192+c] != self.display_buffer[i*192+c] and start == 0:
					start = c
				if picture[i*192+c:i*192+192] == self.display_buffer[i*192+c:i*192+192]:
					end = c
				break
			#and finally we can describe page and column
			self.SetPageAddress(i)
			self.SetColumnAddress(start)
			self.WriteFromBuffer()		#write packet from buffer
			self.WriteData(picture[i*192+start:i*192+end])
			self.WriteFromBuffer()		#write packet from buffer
		#and rewrite buffer
		self.picture_buffer = picture

	def Reset(self):
		"""
			reset picture on display + reset picture on gui buffer
		"""
		self.gui.reset()
		self.controll.RewriteDisplay()

	def Reverse(self, reverse = False):
		"""
			reverse display
		"""
		if reverse != self.reverse:
			if reverse:
				self.WriteCommand(0b0010100111, True)
			else:
				self.WriteCommand(0b0010100110, True)
			self.reverse = reverse
		return True

	def Joystick(self):
		"""
			Get status of joystick position
		"""
		#reset gpio -> load new values
		try:
			self._gpio._value = None
			gpio = self._gpio

			gpio_bin = "{0}{1}{2}".format(gpio[6], gpio[5], gpio[4])

			if gpio_bin == "101":
				#central button
				return 'center'
			if gpio_bin == "001":
				#right
				return 'right'
			if gpio_bin == "010":
				#left
				return 'left'
			if gpio_bin == "011":
				#up
				return 'up'
			if gpio_bin == "100":
				#down
				return 'down'
			return False
		except ValueError as e:
			#failed to open hid try to connect
			self.exceptionConnect()
			#and try to again call this function
			return self.Joystick()

	def Buttons(self):
		"""
			return which button is pressed
		"""
		#reset gpio -> load new values
		try:
			self._gpio._value = None
			gpio = self._gpio

			if gpio[0] == 1 and gpio[1] == 1:
				#both
				return 'BOTH'
			if gpio[0] == 1:
				#OK button
				return 'OK'
			if gpio[1] == 1:
				#NG
				return 'NG'
			return False

		except ValueError as e:
			#failed to open hid try to connect
			self.exceptionConnect()
			#and try to again call this function
			return self.Buttons()

	def SetShiftRegister(self):
		"""
			set shift register from self.shift_register buffer
		"""
		data = int("".join(self.shift_register[::-1]),2)
		self._gpio[2] = True
		self.WriteByte([chr(data)], True)
		#register latch
		self._gpio[7] = False
		time.sleep(0.1)
		self._gpio[7] = True
		self._gpio[2] = self.last_display_dc


	def setErrorLed(self, status):
		"""
			set error set 	
				True - led is ON
				False - led is OFF
		"""
		self._gpio_direction[8] = 0x00
		if status:
			self._gpio[8] = True
		else:
			self._gpio[8] = False

	def exceptionConnect(self):
		while 1:
			try:
				self.__init__(self.gui, self.shift_register)
				#and rewrite display
				self.RewriteDisplay()
				break
			except Exception as e:
				print(e)
				time.sleep(1)
		return True
