"""
# Raspbot RCA Nav Script Reader
# Please merge with main.py
# Made by Taian Chen
"""

# TODO merge with main.py for host
# TODO add self param and docstring note as multiprocess
def nav_script_read(filename):
	"""
	Reads
	:param filename:
	:return:
	"""
	open(filename, "r") as instructions:
		# TODO fix undefined, remember to integrated everything properly with main.py
		for line in instructions:
			instruction_line += 1
		pass
		while instruction_line > 0:
			raw_instructions = instructions.readline()
			instructions_split = raw_instructions.split()
			client.nav_execute(self, instructions_split[0], instructions_split[1])
			sleep(instructions_split[2])
			instruction_line -= 1
		pass
	instructions.close()
	pass
pass
	
	