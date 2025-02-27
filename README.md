# Metroidvania Game

A 2D platformer with Metroidvania-style progression, ability upgrades, and multiple levels.

## Getting Started

### Requirements
- Python 3.7+
- Pygame

### Installation
1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the game launcher:
   ```
   python game_launcher.py
   ```

## How to Play

### Controls
- **Arrow Keys**: Move left/right
- **Space**: Jump
- **Z or Left Mouse**: Attack
- **X**: Parry/Block
- **C**: Dash (if unlocked)
- **ESC**: Pause game

### Level Transitions
- Look for green portals to travel between levels
- The game contains three areas:
  - Starting Area
  - Underground Cave
  - Boss Chamber

### Abilities
- Collect ability upgrades throughout the game:
  - Double Jump
  - Wall Jump
  - Dash
  - Charged Attack

## Development

The game architecture is modular with the following key components:
- `main.py`: Entry point
- `game.py`: Core game logic
- `player.py`: Player movement, abilities and combat
- `level.py`: Level generation and transitions
- `enemy.py`: Enemy AI and behaviors

## Credits
Created as a learning project for game development with Python and Pygame.

