import board
import neopixel

class LedManager():
	quadrant_rotations = [
		{"rotation": 180},
		{"rotation": 90},
		{"rotation": 0},
		{"rotation": 270},
	]
	indices_for_inner_leds = [5,6,9,10]
	indices_for_outer_leds = [0,1,2,3,4,7,8,11,12,13,14,15]
	def __init__(self):
		self.num_pixels = 256
		
		self.pixels = neopixel.NeoPixel(
			board.D21, self.num_pixels * 4, brightness=0.2, auto_write=False, pixel_order="GRB"
		)
		
		#TODO rename these to be quadrant-based
		self.square_size = 4
		self.row_size = 16
		self.number_of_rows = self.row_size // self.square_size
		self.leds_for_square = {}
		self.light_squares = set(["a1","a3","a5","a7","b2","b4","b6","b8","c1","c3","c5","c7","d2","d4","d6","d8","e1","e3","e5","e7","f2","f4","f6","f8","g1","g3","g5","g7","h2","h4","h6","h8"])
		self.coordinates_for_square = {
			1: {	
				# (0, 0): "a1",
				# (0, 1): "a2",
				# (0, 2): "a3",
				# (0, 3): "a4",
				# (1, 0): "b1",
				# (1, 1): "b2",
				# (1, 2): "b3",
				# (1, 3): "b4",
				# (2, 0): "c1",
				# (2, 1): "c2",
				# (2, 2): "c3",
				# (2, 3): "c4",
				# (3, 0): "d1",
				# (3, 1): "d2",
				# (3, 2): "d3",
				# (3, 3): "d4",
				(0,0): "a1",
				(0,1): "a2",
				(0,2): "a3",
				(0,3): "a4",
				(1,0): "b1",
				(1,1): "b2",
				(1,2): "b3",
				(1,3): "b4",
				(2,0): "c1",
				(2,1): "c2",
				(2,2): "c3",
				(2,3): "c4",
				(3,0): "d1",
				(3,1): "d2",
				(3,2): "d3",
				(3,3): "d4",
			},

			4: {
				(0,3): "e1",
				(1,3): "e2",
				(2,3): "e3",
				(3,3): "e4",
				(0,2): "f1",
				(1,2): "f2",
				(2,2): "f3",
				(3,2): "f4",
				(0,1): "g1",
				(1,1): "g2",
				(2,1): "g3",
				(3,1): "g4",
				(0,0): "h1",
				(1,0): "h2",
				(2,0): "h3",
				(3,0): "h4",
			},

			3: {
				(3, 3): "e5",
				(3, 2): "e6",
				(3, 1): "e7",
				(3, 0): "e8",
				(2, 3): "f5",
				(2, 2): "f6",
				(2, 1): "f7",
				(2, 0): "f8",
				(1, 3): "g5",
				(1, 2): "g6",
				(1, 1): "g7",
				(1, 0): "g8",
				(0, 3): "h5",
				(0, 2): "h6",
				(0, 1): "h7",
				(0, 0): "h8",
			},

			2: {
				(3,0): "a5",
				(2,0): "a6",
				(1,0): "a7",
				(0,0): "a8",
				(3,1): "b5",
				(2,1): "b6",
				(1,1): "b7",
				(0,1): "b8",
				(3,2): "c5",
				(2,2): "c6",
				(1,2): "c7",
				(0,2): "c8",
				(3,3): "d5",
				(2,3): "d6",
				(1,3): "d7",
				(0,3): "d8",
			},
		}

		# Initialize a list of led numbers for each position in the grid
		
		self.initialize_leds()
				
		
		
	def transform_odd_row(self, row_number, led_number):
		return (self.number_of_rows - 1) - row_number

	def initialize_leds(self):
		for quadrant in [1,2,3,4]:
			temp_leds_for_square = {}
			quadrant_mapping = self.coordinates_for_square[quadrant]
			for j in range(self.number_of_rows):
				for i in range(self.number_of_rows):
					temp_leds_for_square[(i, j)] = []
			for num in range(self.num_pixels):
				quadrant_offset = (quadrant - 1) * self.num_pixels
				column_number = num % self.row_size
				row_number = num // self.row_size
				grid_row_number = row_number // self.square_size
				grid_column_number = column_number // self.square_size
				if row_number %2 == 1:
					grid_column_number = self.transform_odd_row(grid_column_number, num)
				temp_leds_for_square[(grid_column_number, grid_row_number)].append(quadrant_offset + num)

			# Transform from coordinate basis (which only makes sense inside that quadrant) to global square name0
			for coordinates, leds in temp_leds_for_square.items():
				square_name = quadrant_mapping[coordinates]
				self.leds_for_square[square_name] = leds
		
	def initialize_checkerboard(self):
		for square in self.leds_for_square.keys():
			light = square in self.light_squares
			# This will initialize a checkerboard pattern
			color = (50,50,50) if light else (0, 0, 0)
			leds = self.leds_for_square[square]
			for led in leds:
				self.pixels[led] = color
		self.pixels.show()
		
	def illuminate_square(self, square, color = (0, 255, 0)):
		leds = self.leds_for_square[square]
		if leds is None:
			return
		for i in self.indices_for_inner_leds:
			led = leds[i];
			self.pixels[led] = color
		self.pixels.show()
