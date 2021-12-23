import subprocess

PLATFORM_MODE_HARDWARE = 1
PLATFORM_MODE_EMULATED = 2


def get_stockfish_location():
    result = subprocess.run(["which", "stockfish"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip("\n")


def get_platform_mode():
    # Check if we're running on a platform that's capable of running the raspberry pi and neopixel hardware.
    # If we're not, we can run in "emulator" mode without that hardware.
    try:
        import board
        import neopixel

        return PLATFORM_MODE_HARDWARE
    except ModuleNotFoundError:
        pass
    return PLATFORM_MODE_EMULATED
