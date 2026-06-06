# Meteor Miner

A small retro Python shooter game built with Pygame. In this game, you control a ship in space, destroy meteors, and survive as long as possible.

## How to run

1. Install Pygame if you don't have it:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Controls

- Move: `W`, `A`, `S`, `D` or arrow keys
- Shoot: left mouse click

## Features

- Main menu with Start and Leaderboard buttons
- Title countdown before gameplay begins
- Large meteors appear after 20 seconds and award double points
- Gamma ray obstacles appear after 1 minute and deal double damage
- High score saving in `scores.json`

## Files

- `main.py` — game entry point and loop
- `game_logic.py` — enemy spawning, movement, collisions, and particle logic
- `visuals.py` — rendering and UI drawing
- `scores.json` — saved leaderboard data
- `PressStart2P-Regular.ttf` — fallback game font
