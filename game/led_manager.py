import math
import time
import chess

from config import led_config, config

if config.get_platform_mode() == config.PLATFORM_MODE_HARDWARE:
    import board  # Raspberry Pi board - only available on raspberry pi hardware
    import neopixel  # Adafruit neopixel library - only available on raspberry pi hardware
else:
    from mock_hardware import MockBoard as board
    from mock_hardware import MockNeopixel as neopixel


class LedManager:
    LIGHTING_TYPE_ALL = 1
    LIGHTING_TYPE_INNER = 2
    LIGHTING_TYPE_OUTER = 3
    SQUARE_COLOR_LIGHT = (50, 50, 50)
    SQUARE_COLOR_DARK = (0, 0, 0)

    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if LedManager.__instance == None:
            LedManager()
        return LedManager.__instance

    def __init__(self):
        if LedManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LedManager.__instance = self
        self.number_of_leds_per_quadrant = led_config.number_of_leds_per_quadrant

        self.pixels = neopixel.NeoPixel(
            board.D21,
            self.number_of_leds_per_quadrant * 4,
            brightness=led_config.brightness,  # TODO would be cool to be able to change brightness in the middle of a game. Could just set this to max and adjust brightness through multipliers on the color tuples, though.
            auto_write=False,
            pixel_order=led_config.pixel_color_order,
        )

        # This one was hard to name - it's the number of LEDs on one side of a square
        self.width_of_square_in_leds = 4

        # the matrices are square, so the number of rows is sqrt of the number of leds
        self.led_rows_per_quadrant = int(math.sqrt(self.number_of_leds_per_quadrant))
        self.number_of_rows_of_squares_in_quadrant = (
            self.led_rows_per_quadrant // self.width_of_square_in_leds
        )
        self.leds_for_square = {}

        # TODO make these configurable
        self.piece_color_1 = (255, 0, 255)
        self.piece_color_2 = (0, 255, 255)

        self.light_colored_squares = led_config.light_colored_squares
        self.coordinates_for_square = led_config.coordinates_for_square

        self.initialize_leds()

    def transform_odd_row(self, row_number, led_number):
        return (self.number_of_rows_of_squares_in_quadrant - 1) - row_number

    def initialize_leds(self):
        for quadrant in [1, 2, 3, 4]:  # lol
            temp_leds_for_square = {}
            quadrant_mapping = self.coordinates_for_square[quadrant]
            for column in range(self.number_of_rows_of_squares_in_quadrant):
                for row in range(self.number_of_rows_of_squares_in_quadrant):
                    temp_leds_for_square[(row, column)] = []
            for pixel_number in range(self.number_of_leds_per_quadrant):
                quadrant_offset = (quadrant - 1) * self.number_of_leds_per_quadrant
                column_number = pixel_number % self.led_rows_per_quadrant
                row_number = pixel_number // self.led_rows_per_quadrant
                grid_row_number = row_number // self.width_of_square_in_leds
                grid_column_number = column_number // self.width_of_square_in_leds
                if row_number % 2 == 1:
                    grid_column_number = self.transform_odd_row(
                        grid_column_number, pixel_number
                    )
                temp_leds_for_square[(grid_column_number, grid_row_number)].append(
                    quadrant_offset + pixel_number
                )

            # Transform from coordinate basis (which only makes sense inside that quadrant) to global square name0
            for coordinates, leds in temp_leds_for_square.items():
                square_name = quadrant_mapping[coordinates]
                self.leds_for_square[square_name] = leds

    def initialize_checkerboard(self, piece_map=None):
        for square in self.leds_for_square.keys():
            light = square in self.light_colored_squares
            # This will initialize a checkerboard pattern
            color = (50, 50, 50) if light else (0, 0, 0)
            leds = self.leds_for_square[square]
            for led in leds:
                self.pixels[led] = color
        if piece_map is not None:
            for square_number, piece in piece_map.items():
                square_name = chess.SQUARE_NAMES[square_number]
                is_color_1 = piece.color == chess.WHITE
                self.illuminate_square(
                    square_name,
                    self.piece_color_1 if is_color_1 else self.piece_color_2,
                    self.LIGHTING_TYPE_INNER,
                    False,
                )
        self.pixels.show()

    def flash_piece_colors(self, board: chess.Board, duration: float=0.1):
        for square_number, piece in board.piece_map().items():
            square_name = chess.SQUARE_NAMES[square_number]
            is_color_1 = piece.color == board.turn
            self.illuminate_square(
                square_name,
                self.SQUARE_COLOR_DARK,
                self.LIGHTING_TYPE_INNER,
                False,
            )
            time.sleep(duration)
            self.illuminate_square(
                square_name,
                self.piece_color_1 if is_color_1 else self.piece_color_2,
                self.LIGHTING_TYPE_INNER,
                False,
            )

    def illuminate_square(
        self, square, color=(0, 255, 0), type=2, show_immediately=True, duration=None
    ):
        leds = self.leds_for_square[square]
        if leds is None:
            return
        indices_to_illuminate = []
        if type == self.LIGHTING_TYPE_ALL:
            indices_to_illuminate = range(16)
        elif type == self.LIGHTING_TYPE_INNER:
            indices_to_illuminate = led_config.indices_for_inner_leds
        elif type == self.LIGHTING_TYPE_OUTER:
            indices_to_illuminate = led_config.indices_for_outer_leds
        previous_value = {}
        for i in indices_to_illuminate:
            led = leds[i]
            previous_value[led] = self.pixels[led]
            self.pixels[led] = color
        if show_immediately:
            self.pixels.show()
            if duration is not None:
                time.sleep(duration)
                for index, value in previous_value.items():
                    self.pixels[index] = value
                self.pixels.show()
                # TODO consider a lock on the LedManager. When we highlight a placed piece, but that piece completes a move, the move animation and the highlight animation interact weirdly
