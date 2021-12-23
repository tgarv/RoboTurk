class MockBoard:
    D21 = None

    def __init__(self):
        pass


class MockNeopixel:
    def __init__(self):
        pass

    class NeoPixel:
        def __init__(self, foo, size, **kwargs):
            self.pixels = [0] * size

        def show(self):
            pass

        def __getitem__(self, index):
            return self.pixels[index]

        def __setitem__(self, index, value):
            self.pixels[index] = value
