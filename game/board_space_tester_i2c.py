import time

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

# from adafruit_mcp230xx.mcp23017 import MCP23017


# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
mcp0 = MCP23017(i2c, address=0x20)
mcp1 = MCP23017(i2c, address=0x21)
mcp2 = MCP23017(i2c, address=0x22)
mcps = [mcp0, mcp1, mcp2]

state = [[0 for i in range(16)] for i in range(4)]

for mcp_number in range(len(mcps)):
    mcp = mcps[mcp_number]
    for pin_number in range(16):
        pin = mcp.get_pin(pin_number)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        state[mcp_number][mcp_number] = pin.value

# Now loop blinking the pin 0 output and reading the state of pin 1 input.
while True:
    time.sleep(0.5)
    for mcp_number in range(len(mcps)):
        mcp = mcps[mcp_number]
        for pin_number in range(16):
            pin = mcp.get_pin(pin_number)
            if pin.value != state[mcp_number][pin_number]:
                print(f"({mcp_number},{pin_number}) changed to {pin.value}")
            state[mcp_number][pin_number] = pin.value