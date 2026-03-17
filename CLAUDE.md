# RUN! 3D - Camera Runner Game

## Overview
A 3D endless runner game built as a **single HTML file** (`index.html`, ~760 lines).
The player controls a character using body movements via webcam (MediaPipe Pose) or keyboard/touch.

**GitHub:** https://github.com/itaisabi-collab/camera-runner-3d.git

## Tech Stack
- **Three.js** (v0.149.0) - 3D rendering, loaded from CDN
- **MediaPipe Pose** - Body tracking via webcam
- **Web Audio API** - Procedural music & sound effects
- **Bloom post-processing** (UnrealBloomPass) - Visual effects
- No build tools, no dependencies, no npm - pure browser game

## Architecture
Everything is in `index.html`:
- **Lines 1-53:** HTML + CSS (HUD, overlays, camera preview)
- **Lines 82-101:** Boot loader (loads Three.js, bloom shaders, MediaPipe from CDNs)
- **Lines 104-757:** `initGame()` function containing:
  - `CONFIG (C)` - Speed, spawn timing, jump/duck durations, pose thresholds
  - `STATE (G)` - Game state object (score, speed, obstacles, player, pose data)
  - Object pools (`obsPool`, `coinPool`) for performance
  - Scene setup: renderer, camera, bloom composer, lights, sky, road, environment (posts, trees, buildings)
  - `mkChar()` - Character model (body, head, limbs, shoes)
  - `mkObs(type)` - 3 obstacle types: BLK (block), LOW (jump over), HIGH (duck under)
  - Coins with combo system
  - Particle system (MAX_PARTS=200)
  - Procedural music (`startMusic()`) - melody, harmony, bass, percussion at 145 BPM
  - MediaPipe integration: camera init, pose detection, gesture detection
  - `update(dt)` - Main game loop (movement, collisions, spawning, HUD)
  - Game flow: menu → calibration (3s) → playing → game over
  - Input: keyboard arrows, touch swipe, body pose

## Controls
| Input | Action |
|-------|--------|
| Lean body left/right | Switch lanes |
| Raise both arms | Jump |
| Crouch/lower head | Duck |
| Arrow keys | Lane switch / Jump / Duck |
| Touch swipe | Lane switch / Jump / Duck |

## Key Game Mechanics
- 3 lanes (left/center/right), `LX=[-4, 0, 4]`
- Speed increases over time (`SPD0=0.5` → `SPD_MAX=2.0`)
- Energy system (drains slowly, refills with coins, game over at 0)
- Combo system (consecutive coins multiply score)
- Levels based on score (every 3000 points)
- Camera calibration phase (3 seconds) to set baseline pose

## Commit History
1. Basic camera game
2. Three.js + MediaPipe pose detection
3. Major upgrade: visuals, object pooling, particles, music
4. Bloom post-processing, camera shake, FOV zoom
5. Ground rotation fix
6. Camera request before MediaPipe
7. Better camera/pose status feedback, lighter model
8. Camera switcher for multiple cameras

## What Could Be Improved Next
- More obstacle variety / power-ups
- Mobile performance optimization
- Leaderboard / sharing
- Level themes (different environments)
- Character customization
- Better collision detection (currently lane-based, not precise)
- The game is entirely in one file - could be split if it grows much more
