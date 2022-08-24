from config import sensor_space_mapping
import command_queue
import led_manager
import board_monitor

import threading
import time


class BoardSpaceTester:
    def __init__(self):
        self.sensor_space_mapping = sensor_space_mapping.MAPPING
        self.queue = command_queue.CommandQueue()
        self.led_manager = led_manager.LedManager.getInstance()
        threading.Thread(
            target=lambda: board_monitor.run()
        ).start()

    def test(self):
        self.led_manager.initialize_checkerboard()
        while True:
            input_value = self.queue.dequeue()
            if input_value is None:
                time.sleep(0.1)
                continue
            (board_id, space_id, event_type) = input_value.split(":")
            square = sensor_space_mapping.MAPPING.get(board_id + ":" + space_id)
            if square is None:
                print("No square for this sensor")
            else:
                color = (0, 255, 0) if event_type == "occupied" else (255, 0, 0)
                self.led_manager.illuminate_square(square, color)
                time.sleep(0.25)
                self.queue.reset_queue()


if __name__ == "__main__":
    tester = BoardSpaceTester()
    tester.test()
