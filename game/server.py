from flask import Flask, request
import logging
import command_queue
from led_manager import LedManager
from config import sensor_space_mapping

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# TODO replace this whole server with a thread that's just monitoring the board hardware
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/update_positions", methods=["POST"])
def update_positions():
    led_manager = LedManager.getInstance()
    print(request.get_json())
    queue = command_queue.CommandQueue()
    updated_positions = request.get_json()["positions"]
    for position in updated_positions:
        queue.enqueue(position)

        try:
            (board_id, space_id, event_type) = position.split(":")
        except ValueError:
            continue

        square = sensor_space_mapping.MAPPING.get(board_id + ":" + space_id, None)
        if square is not None:
            led_manager.illuminate_square(
                square, (100, 100, 0), type=LedManager.LIGHTING_TYPE_ALL, show_immediately=True, duration=0.25
            )

    return "done"
