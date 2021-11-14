import board
import neopixel

class LedManager():
	def __init__(self):
		self.num_pixels = 256
		
		self.pixels = neopixel.NeoPixel(
			board.D21, self.num_pixels, brightness=0.02, auto_write=False, pixel_order="GRB"
		)
		
		self.square_size = 4
		self.row_size = 16
		self.number_of_rows = self.row_size // self.square_size
		self.leds_for_square = {}
		self.coordinates_for_square = {
			"a1": (3, 3),
			"a2": (3, 2),
			"a3": (3, 1),
			"a4": (3, 0),
			"b1": (2, 3),
			"b2": (2, 2),
			"b3": (2, 1),
			"b4": (2, 0),
			"c1": (1, 3),
			"c2": (1, 2),
			"c3": (1, 1),
			"c4": (1, 0),
			"d1": (0, 3),
			"d2": (0, 2),
			"d3": (0, 1),
			"d4": (0, 0),
		}
		
		# Initialize a list of led numbers for each position in the grid
		for i in range(self.number_of_rows):
			for j in range(self.number_of_rows):
				self.leds_for_square[(i, j)] = []
		self.initialize_leds()
				
		
		
	def transform_odd_row(self, row_number, led_number):
		return (self.number_of_rows - 1) - row_number

	def initialize_leds(self):
		for num in range(self.num_pixels):
			column_number = num % self.row_size
			row_number = num // self.row_size
			grid_row_number = row_number // self.square_size
			grid_column_number = column_number // self.square_size
			if row_number %2 == 1:
				grid_column_number = self.transform_odd_row(grid_column_number, num)
			self.leds_for_square[(grid_column_number, grid_row_number)].append(num)
		
	def initialize_checkerboard(self):
		for square in self.leds_for_square.keys():
			row = square[0]
			column = square[1]
			
			# This will initialize a checkerboard pattern
			odd = ((row + column) % 2) == 1
			color = (100, 100, 100) if odd else (0, 0, 0)
			leds = self.leds_for_square[square]
			for led in leds:
				self.pixels[led] = color
		self.pixels.show()
		
	def illuminate_square(self, square, color = (0, 100, 0)):
		coordinates = self.coordinates_for_square.get(square)
		if coordinates is None:
			return
		leds = self.leds_for_square[coordinates]
		for led in leds:
			self.pixels[led] = color
		self.pixels.show()
