class Reflector(object):

	def __init__(self, reflect_config, config_file):
		# If reflect_config is not in the configurations file,
		# a ValueError is raised.
		if config_file.has_section(reflect_config) == False:
			print config_file.sections()
			raise ValueError('Reflector config %r not found' % reflect_config)

		# Sets reflector_id, mostly used for debugging.
		self.reflector_id = config_file.getint(
			reflect_config,
			'reflector_id'
		)

		# Imports the reflector map, converts it to a list, and converts
		# each element of the list to an integer.
		self.reflector_map = map(
			lambda x: ord(x) - 65,
			list(config_file.get(reflect_config, 'reflector_map'))
		)

	def convertLetter(self, letter):
		# Converts a letter to another letter.
		return self.reflector_map[letter]

	def currentState(self):
		# Prints the current state of the reflector. Used for debugging.
		print "reflector_id = %r" % self.reflector_id
		print "reflector_map = %r" % self.reflector_map
