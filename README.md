# 🏎️ Car Racing Game

> A lightweight car racing game built with **Python + Pygame**, with a browser-based version powered by **HTML5 Canvas and JavaScript**.

[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-00A86B?logo=python&logoColor=white)](https://www.pygame.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-HTML5%20Canvas-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

Dodge incoming vehicles, survive as long as possible, and beat your high score! Choose between the desktop Pygame experience and the web version for browser and mobile-friendly play.

## ✨ Features

### 🐍 Python / Pygame version

- Arrow-key vehicle controls
- Randomly generated obstacles
- Score and persistent high-score tracking
- Menu, playing, and game-over states
- Animated road markings

### 🌐 Web version

- HTML5 Canvas gameplay
- Responsive layout
- Touch controls for mobile devices
- Gameplay mechanics inspired by the Pygame version

## 🚀 Getting Started

### Prerequisites

- Python **3.7 or newer**
- Pygame **2.6.1**
- A modern web browser for the web version

### Run the Python version

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/Sandipan2011/pygame.git
   cd pygame
   ```

2. Install the Python dependencies:

   ```bash
   python -m pip install -r game/python/requirements.txt
   ```

3. Start the game:

   ```bash
   python game/python/main.py
   ```

### Run the web version

Open `game/web/index.html` in a modern browser. For the most reliable local experience, serve the project with a small local web server:

```bash
python -m http.server 8000 --directory game/web
```

Then visit <http://localhost:8000> in your browser.

## 🎮 Controls

| Action | Keyboard |
| --- | --- |
| Move left | <kbd>←</kbd> Left Arrow |
| Move right | <kbd>→</kbd> Right Arrow |
| Start the game | <kbd>Space</kbd> |
| Restart after game over | <kbd>R</kbd> |

> The web version also supports touch controls on compatible devices.

## 🕹️ How to Play

1. Start the game from the menu.
2. Move your car between lanes to avoid incoming obstacles.
3. Earn points as obstacles pass off-screen.
4. Keep driving to beat your high score.
5. A collision ends the run—press <kbd>R</kbd> to try again.

## 📁 Project Structure

```text
game/
├── python/
│   ├── main.py          # Main game loop and gameplay logic
│   ├── config.py        # Game constants and configuration
│   ├── game_utils.py    # Shared helper functions
│   └── requirements.txt # Python dependencies
├── web/
│   └── index.html       # Browser version
└── assets/              # Images and sounds
```

The repository also contains an expanded legacy implementation in [`original_2d_version/`](original_2d_version/), including power-ups and multiple difficulty levels.

## 🛠️ Development

When adding features, keep platform-specific code in its corresponding directory:

- `game/python/` for the Pygame version
- `game/web/` for the browser version
- `game/assets/` for shared game resources

Please test gameplay after changes and keep controls and documentation up to date.

## 🗺️ Roadmap

- [ ] Add polished graphics and sound assets
- [ ] Add power-ups and special abilities
- [ ] Add selectable difficulty levels
- [ ] Improve mobile support
- [ ] Explore multiplayer gameplay
- [ ] Package the game as a mobile application

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make and test your changes.
4. Commit your work: `git commit -m "Add my feature"`
5. Push the branch and open a pull request.

## 📄 License

No license has been specified for this repository yet. Please contact the repository owner before redistributing or reusing the code.
