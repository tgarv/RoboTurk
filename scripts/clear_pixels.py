import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 1024 

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = "GRB"

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.02, auto_write=False, pixel_order=ORDER
)

pixels.fill((0,0,0))
pixels.show()
