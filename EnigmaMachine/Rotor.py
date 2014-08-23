class Rotor(object):

	def __init__(self, rotor_config, starting_position, config_file):

		# If starting_position is not between 0 and 25, a ValueError is raised.
		if starting_position < 0 or starting_position > 25:
			raise ValueError(
				"starting_position in Rotor must be between 0 and 25"
			)

		# If rotor_config is not in the configuration file, a value error
		# is raised.
		if config_file.has_section(rotor_config) == False:
			print config_file.sections()
			raise ValueError('Rotor config %r not found' % rotor_config)

		# Sets rotor_id, mainly used for debugging.
		self.rotor_id = config_file.getint(rotor_config, 'rotor_id')

		# Imports the rotor map, converts it to a list, and converts
		# each element of the list to an integer.
		self.rotor_map = map(
			lambda x: ord(x) - 65,
			list(config_file.get(rotor_config, 'rotor_map'))
		)

		# Imports the turnover positions, converts them to a list and
		# converts each element of the list to an integer.
		self.turnover_positions = map(
			lambda x: ord(x) - 65,
			config_file.get(rotor_config, 'turnover_positions').split(',')
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
