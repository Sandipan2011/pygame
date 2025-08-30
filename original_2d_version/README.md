# Car Racing Game (Original 2D Version)

A simple 2D car racing game built with Python (Pygame).

## Features

- Player-controlled car with arrow keys
- Random obstacle generation
- Score tracking and high score system
- Game states (Menu, Playing, Game Over)
- Road animation with moving lines
- Power-up system with speed boosts, shields, and score multipliers
- Multiple difficulty levels

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Controls

- **Left Arrow**: Move car left
- **Right Arrow**: Move car right
- **Space**: Start game from menu
- **R**: Restart after game over
- **1-3**: Change difficulty level

## Game Mechanics

- Avoid oncoming obstacles (cars)
- Score increases when obstacles pass off-screen
- Collect power-ups for special abilities
- Game ends on collision with obstacle
- High score is tracked between sessions

## Project Structure

```
original_2d_version/
├── main.py          # Main game logic
├── config.py        # Game constants and configuration
├── game_utils.py    # Helper functions
├── requirements.txt # Python dependencies
└── assets/          # Images and sounds
    ├── car.png
    ├── road.png
    └── crash.wav
```

## Requirements

- Python 3.7+
- Pygame 2.6.1
