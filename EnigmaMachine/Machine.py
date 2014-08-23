from Plugboard import Plugboard
from Reflector import Reflector
from Rotor import Rotor

class EnigmaMachine(object):

	def __init__(self, plugboard, first_rotor, second_rotor, third_rotor, reflector):
		# Ensures the inputs are valid.
		if isinstance(plugboard, Plugboard) == False:
			raise TypeError("1st argument must be of class Plugboard")
		elif isinstance(first_rotor, Rotor) == False:
			raise TypeError("2nd argument must be of class Rotor")
		elif isinstance(second_rotor, Rotor) == False:
			raise TypeError("3nd argument must be of class Rotor")
		elif isinstance(third_rotor, Rotor) == False:
			raise TypeError("4nd argument must be of class Rotor")
		elif isinstance(reflector, Reflector) == False:
			raise TypeError("5th argument must be of class Reflector")
		else:
			# Configures the machine.
			self.plugboard = plugboard
			self.first_rotor = first_rotor
			self.second_rotor = second_rotor
			self.third_rotor = third_rotor
			self.reflector = reflector

	def inputMessage(self, message):
		# If message is not a string, a ValueError is raised.
		if isinstance(message, str) == False:
			raise ValueError("message in EnigmaMachine.inputMessage() must be a string")

		# Initializes an empty list to store message.
		self.message = []
		# For each element in message, if the element is a character, it is
		# converted to an integer and stored in self.message. If it is not a
		# character, it is stored in self.message as itself.
		for char in message.upper():
			if char.isalpha():
				self.message.append(ord(char) - 65)
			else:
				self.message.append(char)
		# Initializes self.converted_message to store the message after it
		# is encrypted.
		self.converted_message = ''

	def rotateRotors(self):
		# Rotates the rotors. The output of the Rotor.rotate() method is either
		# True or False. If the first rotor returns True, then the second
		# rotor is rotated. If the second rotor returns True, then the third
		# rotor is rotated.
		rotate_next = self.first_rotor.rotate()
		if rotate_next:
			rotate_next = self.second_rotor.rotate()
		if rotate_next:
			rotate_next = self.third_rotor.rotate()

	def convertLetter(self, letter):
		# Ensures letter is an integer.
		if isinstance(letter, int) == False:
			raise TypeError("letter in convertLetter() must be an integer")

		# Converts the letter to another letter.
		letter = self.plugboard.convertLetter(letter)
		letter = self.first_rotor.convertFwd(letter)
		letter = self.second_rotor.convertFwd(letter)
		letter = self.third_rotor.convertFwd(letter)
		letter = self.reflector.convertLetter(letter)
		letter = self.third_rotor.convertRev(letter)
		letter = self.second_rotor.convertRev(letter)
		letter = self.first_rotor.convertRev(letter)
		letter = self.plugboard.convertLetter(letter)

		# Returns letter.
		return letter

	def convertMessage(self):
		# For each element in self.message, if the element is an integer,
		# then it is run through the enigma machine, converted back to a letter,
		# and then concatenated onto self.converted_message. If it is not an
		# integer, then it is concatenated onto self.converted_message.
		for char in self.message:
			if isinstance(char, int):
				self.rotateRotors()
				self.converted_message += chr(self.convertLetter(char)+65)
			else:
				self.converted_message += char

		# Returns self.converted_message
		return self.converted_message

	def currentState(self):
		# Prints out the current state of the enigma machine.
		print "-" * 65
		print "Plugboard:"
		self.plugboard.currentState()
		print "\nFirst Rotor:"
		self.first_rotor.currentState()
		print "\nSecond Rotor:"
		self.second_rotor.currentState()
		print "\nThird Rotor:"
		self.third_rotor.currentState()
		print "\nReflector:"
		self.reflector.currentState()
		print "\nMessage"
		print self.message
