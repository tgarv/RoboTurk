from config import sensor_space_mapping
import led_manager
import board_monitor

import threading
import time


class BoardSpaceTester:
    def __init__(self):
        self.sensor_space_mapping = sensor_space_mapping.MAPPING
        self.led_manager = led_manager.LedManager.getInstance()
        threading.Thread(
            target=lambda: board_monitor.run()
        ).start()

    def test(self):
        time.sleep(1)
        self.led_manager.initialize_checkerboard()
        while True:
            for key, value in board_monitor.BoardMonitor.board_state.items():
                square = self.sensor_space_mapping.get(key, None)
                if square is not None:
                    color = (0, 255, 0) if value == "occupied" else (255, 0, 0)
                    self.led_manager.illuminate_square(square, color, show_immediately=False)
            self.led_manager.show()
            time.sleep(0.05)

if __name__ == "__main__":
    tester = BoardSpaceTester()
    tester.test()
