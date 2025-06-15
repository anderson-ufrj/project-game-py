# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running the Game
```bash
# Recommended: Use the automatic script
./run.sh

# Manual execution
source venv/bin/activate
python jogo.py
```

### Development Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing
No test framework is currently set up. To test changes, run the game manually and verify functionality.

## High-Level Architecture

### Core Game Structure
The game follows a state machine pattern with the following states:
- MENU → CHARACTER_SELECT → PLAYING → GAME_OVER
- PAUSED state can be entered from PLAYING state

### Class Hierarchy
```
GameObject (base for all entities)
    └── MagicCaster (entities that can cast spells)
        ├── Wand (player character)
        └── Pixie (enemy entities)
```

### Key Systems

**Sprite Management**: Uses pygame sprite groups for efficient collision detection:
- `all_sprites`: All game entities
- `player_spells`: Player projectiles
- `pixie_spells`: Enemy projectiles
- `pixies`: Enemy entities

**Collision System**: Handled in `check_collisions()` method:
- Player spells vs enemies (scoring)
- Enemy spells vs player (damage)
- Direct player-enemy collisions (damage)

**Difficulty Progression**: 
- Level increases every 30 seconds
- Enemy spawn rate increases and health scales with level
- Points awarded scale with difficulty

**Input Handling**:
- Event-based for menus and single actions (ESC, ENTER, SPACE)
- Continuous polling for movement (arrow keys/WASD)

### Important Implementation Details

1. **All graphics are procedurally generated** - no external image files are used
2. **Sounds are generated programmatically** using byte arrays
3. **The game runs at 60 FPS** with frame limiting in the main loop
4. **Entity behaviors are enum-based** (PixieBehavior: STRAIGHT, ZIGZAG, CIRCULAR)
5. **Visual effects include**:
   - Animated starfield background
   - Glow effects on wand
   - Explosion animations
   - Invulnerability flashing

### File Structure
```
jogo.py              # Single file containing entire game implementation
requirements.txt     # Only dependency: pygame>=2.1.0
run.sh              # Convenience script for setup and execution
```

The entire game is implemented in a single `jogo.py` file (~1300 lines) using pygame. All assets (sprites, sounds) are generated programmatically at runtime.