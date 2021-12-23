from flask import Flask, request
import logging
import command_queue

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/update_positions", methods=["POST"])
def update_positions():
    print(request.get_json())
    queue = command_queue.CommandQueue()
    updated_positions = request.get_json()["positions"]
    for position in updated_positions:
        queue.enqueue(position)
    return "done"
