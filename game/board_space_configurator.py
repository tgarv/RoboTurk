from config import sensor_space_mapping
import led_manager
import board_monitor

import threading
import time
import os
import json
import sys


class BoardSpaceConfigurator:
    def __init__(self):
        self.sensor_space_mapping = sensor_space_mapping.MAPPING
        ranks = range(1, 9)
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        all_squares = []
        for rank in ranks:
            for f in files:
                all_squares.append(f + str(rank))
        self.all_squares = all_squares
        self.led_manager = led_manager.LedManager.getInstance()
        threading.Thread(
            target=lambda: board_monitor.run()
        ).start()

    def configure_board_squares(self, spaces=None):
        new_mapping = self.sensor_space_mapping
        if not spaces:
            new_mapping = {}  # Start from scratch
            spaces = self.all_squares
        for square in spaces:
            self.led_manager.initialize_checkerboard()
            self.led_manager.illuminate_square(square)
            board_monitor.BoardMonitor.reset_pending_actions()
            current_value = self.sensor_space_mapping.get(
                square, "TODO"
            )  # TODO this is wrong, the dict is the other way around
            print(
                "Place a magnet for square %s; current value is %s"
                % (square, current_value)
            )
            square_value = None
            while square_value is None:
                input_value = None
                attempts_remaining = 20
                while input_value is None and attempts_remaining > 0:
                    board_monitor.BoardMonitor.reset_pending_actions()
                    attempts_remaining -= 1
                    # TODO store previous, and if the new one is the same as the previous then skip it (it's likely due to bounce or a misplaced piece)
                    time.sleep(0.25)
                    input_value = board_monitor.BoardMonitor.get_pending_action()
                    if input_value is None:
                        continue
                    (board_id, space_id, event_type) = input_value.split(":")
                    if event_type == "empty":
                        input_value = None
                        continue
                if attempts_remaining == 0:
                    user_input = input(
                        'No mapping found; press Enter to try again, or type "skip" to skip this square'
                    )
                    if user_input == "skip":
                        break
                    else:
                        board_monitor.BoardMonitor.reset_pending_actions()
                        continue
                else:
                    square_value = board_id + ":" + space_id
                    if square_value in new_mapping:
                        print(
                            "\n\n\nERROR:Value %s already exists in mapping for square %s\n\n\n"
                            % (square_value, square)
                        )
                    print("Got value %s for square %s" % (square_value, square))
                    new_mapping[square_value] = square
                    time.sleep(1)
        print("\n\n NEW MAPPING \n\n")
        print(new_mapping)
        write_to_file = input("Write new mapping to file?")
        if write_to_file == "yes":
            with open(
            # TODO this wrote to the wrong file?
                os.path.join(os.path.dirname(__file__), "config/sensor_space_mapping.json"),
                "w",
            ) as file:
                json.dump(new_mapping, file)


if __name__ == "__main__":
    configurator = BoardSpaceConfigurator()
    if len(sys.argv) > 1:
        spaces = sys.argv[1]
        configurator.configure_board_squares(spaces.split(","))
    else:
        configurator.configure_board_squares()
