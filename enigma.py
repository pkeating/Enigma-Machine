from EnigmaMachine import Plugboard
from EnigmaMachine import Rotor
from EnigmaMachine import Reflector
from EnigmaMachine import Machine
import ConfigParser

def configureRotor(n):
	# Opens the Rotor configurations file.
	config_file = ConfigParser.RawConfigParser()
	config_file.read('Config/rotor_config.cfg')
	
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
	print config_file.sections()

	# Gets the rotor configuration from the user and ensures it's valid.
	while True:
		rotor_id = raw_input("Choose Rotor: ")
		if config_file.has_section(rotor_id):
			break
		else:
			print "No such rotor exists."

	# Gets the starting position from the user and ensures it's valid.
	print "Starting position should be a number between 0 and 25."
	while True:
		try:
			rotor_starting_position = int(raw_input("Choose Starting Position: "))
		# If user doesn't enter an integer, the resulting exception
		# will be handled here.
		except:
			print 'You must enter a number.'
		# If the integer entered by the user is not between 0 and 25,
		# then the user will be informed their input is invalid and
		# will be re-prompted.
		else:
			if rotor_starting_position < 0 or rotor_starting_position > 25:
				print 'You must enter a number between 0 and 25.'
			else: # If input is valid, the while loop is broken.
				break

	# Initializes the rotor and returns it to main().
	rotor = Rotor.Rotor(rotor_id, rotor_starting_position, config_file)
	return rotor


def configureReflector():
	# Opens the Reflector configurations file.
	config_file = ConfigParser.RawConfigParser()
	config_file.read('Config/reflector_config.cfg')

	# Prints the reflectors in the reflector configurations file.
	print "-" * 65
	print "Select the reflector you wish to use. Valid choices are:"
	print config_file.sections()

	# While loop ensures user's input is valid.
	while True:
		# Gets the reflector name from the user.
		reflector_id = raw_input("Choose reflector: ")
		# If reflector_id is not a section in the config file, the while loop
		# repeats. If reflector_id is valid, the while loop is broken.
		if config_file.has_section(reflector_id):
			break
		else:
			print "No such reflector exists."

	# Initializes the reflector and returns it to main().
	reflector = Reflector.Reflector(reflector_id, config_file)
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
	pairs = raw_input('> ')

	# Configures the plugboard.
	plugboard = Plugboard.Plugboard(pairs)

	# Returns the plugboard to main().
	return plugboard


def main():
	# Configures the machine.
	enigma_machine = Machine.EnigmaMachine(
		configurePlugboard(),
		configureRotor(1),
		configureRotor(2),
		configureRotor(3),
		configureReflector()
	)

	# Gets the user's message.
	message = raw_input('Input Message: ')

	# Put's the message in the Enigma Machine.
	enigma_machine.inputMessage(message)

	# Encrypts the message
	converted_message = enigma_machine.convertMessage()

	# Opens an output file and writes new_message to it.
	output_file = open('output.txt', 'w')
	output_file.write(converted_message)
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
