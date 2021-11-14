class CommandQueue():
	FILEPATH = "game/commands.txt"
	def __init__(self):
		self.queue = []
		
	def reset_queue(self):
		with open(self.FILEPATH, "w") as f:
			f.write("")
	
	def dequeue(self):
		with open(self.FILEPATH, "r") as f:
			lines = f.readlines()
			if lines == []:
				return None
			command = lines.pop(0).strip("\n")
		with open(self.FILEPATH, "w") as f:
			for line in lines:
				f.write(line)
		return command
				
	def enqueue(self, command):
		with open(self.FILEPATH, "a") as f:
			f.write(command + "\n")
