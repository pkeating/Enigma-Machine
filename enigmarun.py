import machine
import ConfigParser


def letterToNumber(string):
	# Converts a string to a list of integers. Only letters of the alphabet
	# are converted to integers; all other characters remain a string.
	new_list = []
	for char in string.upper():
		if char.isalpha():
			new_list.append(ord(char) - 65)
		else:
			new_list.append(char)
	return new_list


def numberToLetter(a_list):
	# Converts a list of integers and strings to a string. All integers in
	# the list will be converted to a letter of the alphabet.
	new_string = ''
	for char in a_list:
		if isinstance(char, int):
			new_string += chr(char + 65)
		else:
			new_string += char
	return new_string


def configureRotor(n):
	# Opens the Rotor configurations file.
	config = ConfigParser.RawConfigParser()
	config.read('Config/rotor_configs.cfg')
	
	# Prints instructions to the user along with a list of the valid
	# rotor configurations.
	print "-" * 65
	if n == 1:
		print "Choose the first rotor and its starting position."
	if n == 2:
		print "Choose the second rotor and its starting position."
	if n == 3:
		print "Choose the third rotor and its starting position."
	print "Select the rotor you wish to use. Valid choices are:"
	print config.sections()

	# Gets the rotor configuration from the user and ensures it's valid.
	while True:
		rtr_id = raw_input("Choose Rotor: ")
		if config.has_section(rtr_id):
			break
		else:
			print "Rotor name not recognized."

	# Gets the starting position from the user and ensures it's valid.
	print "Starting position should be a number between 0 and 25."
	while True:
		try:
			rtr_sp = int(raw_input("Choose Starting Position: "))
		# If user doesn't enter an integer, the resulting exception
		# will be handled here.
		except:
			print 'You must enter a number.'
		# If the integer entered by the user is not between 0 and 25,
		# then the user will be informed their input is invalid and
		# will be re-prompted.
		else:
			if rtr_sp < 0 or rtr_sp > 25:
				print 'You must enter a number between 0 and 25.'
			else: # If input is valid, the while loop is broken.
				break

	# Initializes the rotor and returns it to main().
	rotor = machine.Rotor(rtr_id, rtr_sp)
	return rotor


def configureReflector():
	# Opens the Reflector configurations file.
	config = ConfigParser.RawConfigParser()
	config.read('Config/reflector_configs.cfg')

	# Prints the reflectors in the reflector configurations file.
	print "-" * 65
	print "Select the reflector you wish to use. Valid choices are:"
	print config.sections()

	# While loop ensures user's input is valid.
	while True:
		# Gets the reflector name from the user.
		reflector_id = raw_input("Choose reflector: ")
		# If reflector_id is not a section in the config file, the while loop
		# repeats. If reflector_id is valid, the while loop is broken.
		if config.has_section(reflector_id):
			break
		else:
			print "Reflector name not recognized."

	# Initializes the reflector and returns it to main().
	reflector = machine.Reflector(reflector_id)
	return reflector


def configurePlugboard():
	# Explains how to configure the plugboard.
	print "-" * 65
	print "Choose the plugboard settings. The plugboard allows you to swap"
	print "one letter for another before and after it runs through the rotors."
	print "Input should take the form:"
	print "ab, cd, ef, gh"
	print "You can choose as many pairs as you like, but you cannot"
	print "repeat letters."

	# Gets the plugboard settings from the user.
	plugs = raw_input('> ')

	# Configures the plugboard.
	plugboard = machine.Plugboard(plugs)

	# Returns the plugboard to main().
	return plugboard


def main():
	# Configures the machine.
	enigma_machine = machine.EnigmaMachine(
		configurePlugboard(),
		configureRotor(1),
		configureRotor(2),
		configureRotor(3),
		configureReflector()
	)

	# Gets the user's message, converts all letters to integers, and stores
	# the result as a list. Creates an empty list to store the message
	# after it goes through the enigma machine.
	message = letterToNumber(raw_input("Enter Your Message: "))
	new_message = []

	# Runs the message through the enigma machine.
	for i in message:
		# If i is an integer, it is run through the machine.
		if isinstance(i, int):
			enigma_machine.rotateRotors()
			new_message.append(enigma_machine.convertLetter(i))
		else:
			new_message.append(i)

	# Converts new_message to a string.
	new_message = numberToLetter(new_message)

	# Opens an output file and writes new_message to it.
	output_file = open('output.txt', 'w')
	output_file.write(new_message)
	output_file.close()

	# Prints a message to the user letting them know their output is ready
	print '-' * 65
	print "Your encrypted message is available in output.txt"
	print "Remember your plugboard settings, the rotors you chose, their"
	print "starting positions, and the reflector you used. You will need"
	print "these to decrypt the message. To decrypt, rerun the program"
	print "with the same settings and enter the encrypted message.\n"


if __name__ == "__main__":
	main()
