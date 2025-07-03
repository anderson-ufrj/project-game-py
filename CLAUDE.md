# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Corrida pela Relíquia (Relic Run) is a 2D adventure game built with Pygame where players quest for the mythical Eldritch Gem. The game features 4 levels, multiple enemy types, collectible items, and an inventory system.

**Academic Project Information:**
- Course: Tópicos Especiais I
- Institution: IFSULDEMINAS Campus Muzambinho  
- Student: Anderson Henrique da Silva
- Advisor: Prof. Ricardo Martins

## Running the Game

```bash
# Install pygame dependency
pip install pygame

# Run the game from the root directory
cd code
python main.py
```

The game entry point is `code/main.py`. The game uses relative paths that assume execution from the `code/` directory.

## Core Architecture

### Game State Management
- Game states are managed via `self.game_state` integer values in `main.py`
- States: 0=homescreen, 1=loading transition, 2=intro cutscene, 3=level1, etc.
- Each level and cutscene is a separate class (Level1, Level2, Intro, etc.)

### Level Structure
- Each level inherits common patterns but implements unique maps and enemy spawns
- Levels use CSV files for collision data imported from Tiled maps
- Map backgrounds are single image files, not tile-based sprites (performance optimization)
- Collision detection uses invisible sprites positioned based on CSV data

### Entity System
- Base `Entity` class handles movement, collision, and animation
- `Player` class extends Entity with inventory, weapons, and input handling  
- `Enemy` class extends Entity with AI, different monster types, and combat

### Camera System
- Custom `YSortCameraGroup` class moves the world instead of the player
- Implements Y-sorting for proper sprite layering
- Camera follows player movement smoothly

### Audio System
- Background music changes per game state/level
- Sound effects use separate mixer channels to avoid conflicts
- Audio files are in `../audio/` relative to code directory

## Key Components

### Player (`player.py`)
- Movement with arrow keys, shift to run
- Weapon switching and attack system
- Inventory tracking (health/attack/speed orbs, keys, gems)
- Animation states: idle, moving, attacking (per direction)

### Enemies (`enemy.py`)
- Three enemy types: bigboi, black, golu (defined in `settings.py`)
- AI with attack/notice radius and pathfinding toward player
- Different health, damage, and speed per type
- Level-based scaling (level 2 enemies are larger)

### Collectables (`collectables.py`)
- Health orbs, attack orbs, speed orbs, keys, eldritch gems
- Collision detection modifies player stats and inventory
- Animated sprites with frame cycling

### Levels (`level.py`, `level2.py`, etc.)
- Each level loads unique map layout from CSV collision files
- Spawn points for enemies and collectables
- Victory conditions (collect keys/gems, reach exit)
- Reset functionality for game over scenarios

## Map Creation Process

Maps are designed in Tiled but exported as:
1. Background image (single PNG file)
2. CSV files for collision data and entity spawn points
3. Map files located in `../map new/` directory

## File Organization

- `code/` - All Python source files
- `graphics/` - Sprites, animations, UI images organized by type
- `audio/` - Music and sound effects
- `map new/` - Tiled map files and CSV exports

## Development Notes

- Game uses pygame.SCALED for automatic resolution scaling
- Performance optimized by using image backgrounds instead of many tile sprites
- Custom collision system doesn't use pytmx library
- All sprite paths use relative paths from code directory (`../graphics/...`)
- Font file: `../graphics/font/joystix.ttf`