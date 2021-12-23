# RoboTurk
Ever heard of the "Mechanical Turk"? A box that supposedly played chess by itself, but actually had a human inside of it? Well, this is Robo Turk, a chess board that makes the Mechanical Turk a reality through the power of robotics. (Just kidding, it doesn't have any robotic parts yet, but it does have cool LEDs and sensors)

## Playing the game
```bash
$ source venv/bin/activate
$ sudo sh run.sh # Stupid raspberry pi needs sudo to access GPIO pins
```

## Configuring the board
This only needs to be done if any of the underlying arduino/reed switch hardware has changed. It'll loop through all squares of the board, waiting for a piece to be placed, and storing a mapping of square to reed switch ID. You can also provide an optional list of squares if you only want to configure the mapping for some of them. It's a pretty tedious process, so good luck.  
`$ python3 game/board_space_configurator.py`  
`$ python3 game/board_space_configurator.py a1,c7,d4`

## Testing the board
This enters a mode where any reed switch events (a piece being placed or removed) are highlighted on the board. This requires the board to already have been configured by the prior step. Each "placed" piece will highlight a square in green, and each "removed" piece will highlight a square in red. There's a delay between placing/removing (to account for the reed switch "bounce" that occasionally happens), so you can't move pieces super quickly and it'll only do one at a time.  
`$ python3 game/board_space_tester.py`


## Setup
Install Stockfish:  
`$ brew install stockfish`  
Initialize virtualenv:  
`$ python3 -m venv venv`  
`$ pip install -r requirements.txt`  

python-chess docs: https://python-chess.readthedocs.io/en/latest/engine.html  
