class Plugboard(object):

	def __init__(self, plugs):
		# Removes all characters that are not letters from plugs, converts
		# them to integers, and stores them in self.plugs.
		self.plugs = []
		for char in plugs:
			if char.isalpha():
				self.plugs.append(ord(char.upper()) - 65)

		# Ensures each element of self.plugs is unique.
		if len(self.plugs) != len(set(self.plugs)):
			raise ValueError('Each element of plugs in Plugboard must be unique')

		# Ensures there are an even number of elements in self.plugs.
		if len(self.plugs) % 2 == 1:
			raise ValueError('Plugs must contain an even number of elements')

	def convertLetter(self, letter):
		# Plugboard() converts one letter to another by pairing elements in a
		# list. The values in position 0 and position 1 of the list are
		# connected, so if the value in position 0 is fed into convertLetter(),
		# the value in position 1 will be returned and vice versa.
		# Positions 2 and 3, 4 and 5, etc have the same relationship.
		# If the value fed into the plugboard is not in plugs, then Plugboard()
		# will return the initial value.
		if letter in self.plugs:
			n = self.plugs.index(letter)
			if n % 2 == 0:
				return self.plugs[n + 1]
			else:
				return self.plugs[n - 1]
		else:
			return letter

	def currentState(self):
		# Used for debugging. Prints self.plugs.
		print "self.plugs = %r" % self.plugs
