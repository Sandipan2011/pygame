# Car Racing Game

A simple car racing game built with Python (Pygame) and a web version (HTML/CSS/JavaScript).

## Features

- **Python Version**: Built with Pygame
  - Player-controlled car with arrow keys
  - Random obstacle generation
  - Score tracking and high score system
  - Game states (Menu, Playing, Game Over)
  - Road animation with moving lines

- **Web Version**: Built with HTML5 Canvas and JavaScript
  - Responsive design
  - Touch controls for mobile devices
  - Similar gameplay mechanics

## Python Version Setup

1. Install dependencies:
```bash
pip install -r game/python/requirements.txt
```

2. Run the game:
```bash
python game/python/main.py
```

## Controls

- **Left Arrow**: Move car left
- **Right Arrow**: Move car right
- **Space**: Start game from menu
- **R**: Restart after game over

## Game Mechanics

- Avoid oncoming obstacles (cars)
- Score increases when obstacles pass off-screen
- Game ends on collision with obstacle
- High score is tracked between sessions

## Project Structure

```
game/
├── python/
│   ├── main.py          # Main game logic
│   ├── config.py        # Game constants and configuration
│   ├── game_utils.py    # Helper functions
│   └── requirements.txt # Python dependencies
├── web/
│   └── index.html       # Web version
└── assets/              # Images and sounds (to be added)
```

## Requirements

- Python 3.7+
- Pygame 2.6.1
- Modern web browser (for web version)

## Future Enhancements

- Add proper graphics and sound assets
- Implement power-ups and special features
- Add difficulty levels
- Multiplayer support
- Mobile app version
