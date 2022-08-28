import time

import board
import busio
import digitalio

import command_queue

from adafruit_mcp230xx.mcp23017 import MCP23017


# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
mcp0 = MCP23017(i2c, address=0x20)
mcp1 = MCP23017(i2c, address=0x21)
mcp2 = MCP23017(i2c, address=0x22)
mcp3 = MCP23017(i2c, address=0x23)
mcps = [mcp0, mcp1, mcp2, mcp3]

state = [[0 for i in range(16)] for i in range(4)]

class BoardMonitor():
	board_state = {}
	def __init__(self):
		self.queue = command_queue.CommandQueue()

		for mcp_number in range(len(mcps)):
			mcp = mcps[mcp_number]
			for pin_number in range(16):
				pin = mcp.get_pin(pin_number)
				pin.direction = digitalio.Direction.INPUT
				pin.pull = digitalio.Pull.UP
				state[mcp_number][mcp_number] = pin.value
		for mcp_number in range(len(mcps)):
				mcp = mcps[mcp_number]
				for pin_number in range(16):
					pin = mcp.get_pin(pin_number)
					pin_value = "occupied" if pin.value == False else "empty"
					state[mcp_number][pin_number] = pin_value
					BoardMonitor.board_state[f"{mcp_number}:{pin_number}"] = pin_value

	def run(self):
		while True:
			time.sleep(0.1)
			for mcp_number in range(len(mcps)):
				mcp = mcps[mcp_number]
				for pin_number in range(16):
					pin = mcp.get_pin(pin_number)
					pin_value = "occupied" if pin.value == False else "empty"
					if pin_value != state[mcp_number][pin_number]:
						print(f"Enqueuing {mcp_number}:{pin_number}:{pin_value}")
						self.queue.enqueue(f"{mcp_number}:{pin_number}:{pin_value}")
					state[mcp_number][pin_number] = pin_value
					BoardMonitor.board_state[f"{mcp_number}:{pin_number}"] = pin_value

def run():
	monitor = BoardMonitor()
	monitor.run()

if __name__ == "__main__":
	run()
