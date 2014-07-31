import ConfigParser

class Rotor(object):

	def __init__(self, rotor_config, starting_position):

		# If starting_position is not between 0 and 25, a ValueError is raised.
		if starting_position < 0 or starting_position > 25:
			raise ValueError(
				"starting_position in Rotor must be between 0 and 25"
			)

		# Opens the rotor configurations file.
		rotor_configs = ConfigParser.RawConfigParser()
		rotor_configs.read('Config/rotor_configs.cfg')

		# If rotor_config is not in the configuration file, a value error
		# is raised.
		if rotor_configs.has_section(rotor_config) == False:
			print rotor_configs.sections()
			raise ValueError('Rotor config %r not found' % rotor_config)

		# Sets rotor_id, mainly used for debugging.
		self.rotor_id = rotor_configs.getint(rotor_config, 'rotor_id')

		# Imports the rotor map, converts it to a list, and converts
		# each element of the list to an integer.
		self.rotor_map = map(
			lambda x: ord(x) - 65,
			list(rotor_configs.get(rotor_config, 'rotor_map'))
		)

		# Imports the turnover positions, converts them to a list and
		# converts each element of the list to an integer.
		self.turnover_positions = map(
			lambda x: ord(x) - 65,
			rotor_configs.get(rotor_config, 'turnover_positions').split(',')
		)

		# Sets current_position equal to starting_position.
		self.current_position = starting_position

		# Rotates the rotor into the starting position. Rotor_map set above
		# assumes a current position equal to zero.
		for i in range(0, self.current_position):
			self.rotor_map.insert(0, self.rotor_map.pop())
			self.rotor_map = map(lambda x: (x + 1) % 26, self.rotor_map)

	def convertFwd(self, letter):
		# Returns the output location of the electrical current on its initial
		# trip through the rotor.
		return self.rotor_map[letter]

	def convertRev(self, letter):
		# Returns the output location of the electical current on its return
		# trip through the rotor.
		return self.rotor_map.index(letter)

	def rotate(self): # Rotates the rotor one position.
		# Adds one to the current position. This is used later on in the
		# rotate() method to decide if the next rotor should be rotated.
		self.current_position = (self.current_position + 1) % 26
		
		# Removes the last item of rotor_map and moves it to the front of the
		# list. This simulates the circular nature of the rotors.
		self.rotor_map.insert(0, self.rotor_map.pop())
		
		# Adds one to each element in rotor_map. This simulates the physical
		# movement of the rotors.
		self.rotor_map = map(lambda x: (x + 1) % 26, self.rotor_map)

		# If the current position is a turnover position, then True is returned
		# otherwise False is returned. This is used to determine if the next
		# rotor needs to be rotated.
		if self.current_position in self.turnover_positions:
			return True
		else:
			return False

	def currentState(self):
		# Used for debugging. Prints rotor_id, current_position,
		# rotor_map, and turnover_position.
		print 'rotor_id = %r' % self.rotor_id
		print 'current_position = %r' % self.current_position
		print 'turnover_positions = %r' % self.turnover_positions
		print 'rotor_map = %r' % self.rotor_map


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


class Reflector(object):

	def __init__(self, reflect_config):
		# Opens the reflector configurations file.
		reflect_configs = ConfigParser.RawConfigParser()
		reflect_configs.read('Config/reflector_configs.cfg')

		# If reflect_config is not in the configurations file,
		# a ValueError is raised.
		if reflect_configs.has_section(reflect_config) == False:
			print reflect_configs.sections()
			raise ValueError('Reflector config %r not found' % reflect_config)

		# Sets reflector_id, mostly used for debugging.
		self.reflector_id = reflect_configs.getint(
			reflect_config,
			'reflector_id'
		)

		# Imports the reflector map, converts it to a list, and converts
		# each element of the list to an integer.
		self.reflector_map = map(
			lambda x: ord(x) - 65,
			list(reflect_configs.get(reflect_config, 'reflector_map'))
		)

	def convertLetter(self, letter):
		# Converts a letter to another letter.
		return self.reflector_map[letter]

	def currentState(self):
		# Prints the current state of the reflector. Used for debugging.
		print "reflector_id = %r" % self.reflector_id
		print "reflector_map = %r" % self.reflector_map


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
