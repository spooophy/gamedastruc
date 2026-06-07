# Data Structures Analysis: Meteor Miner Game
## School Project Documentation

**Student:** spooophy  
**Project:** Meteor Miner (Python Pygame Game)  
**Date:** 2026  
**Language:** Python  

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Structures Used](#data-structures-used)
3. [Detailed Code Analysis](#detailed-code-analysis)
4. [Time Complexity Analysis](#time-complexity-analysis)
5. [Conclusion](#conclusion)

---

## Project Overview

**Meteor Miner** is a retro-style space shooter game built with Python and Pygame. The player controls a ship, destroys incoming meteors and gamma rays, and accumulates points. The game features a main menu, leaderboard system, and particle effects.

### Game Features:
- Player movement and shooting mechanics
- Enemy spawning and AI targeting
- Collision detection system
- Particle effects for explosions
- Score tracking and leaderboard
- Multiple difficulty modes

### Files:
- `main.py` — Game entry point and main loop
- `game_logic.py` — Game logic, spawning, movement, collisions
- `visuals.py` — Rendering and UI

---

## Data Structures Used

This game demonstrates the following data structures:

| Data Structure | Status | Used For |
|---|---|---|
| **Array / Dynamic Array (List)** | ✅ Implemented | Game objects, messages |
| **Hash Table / Hash Map (Dictionary)** | ✅ Implemented | Game entities, game state |
| **Set** | ✅ Implemented | Collision tracking |
| **Sorting Algorithms** | ✅ Implemented | Leaderboard ranking |
| **Linked List** | ❌ Not Implemented | — |
| **Queue** | ❌ Not Implemented | — |
| **Stack** | ❌ Not Implemented | — |
| **Tree** | ❌ Not Implemented | — |
| **Graph** | ❌ Not Implemented | — |

---

## Detailed Code Analysis

### 1. **Arrays / Dynamic Lists**

**Definition:** A dynamic array is a resizable list that can grow or shrink as elements are added or removed.

**Implementation in Game Logic:**

#### 1.1 Game Object Collections (main.py, lines 107-110)
```python
# Dynamic lists to store game objects
bullets = []      # Stores all active bullet objects
enemies = []      # Stores all active enemy objects
rays = []         # Stores all gamma ray obstacles
particles = []    # Stores all particle effect objects
```

**Why Used:** These lists grow and shrink dynamically as bullets are fired, enemies spawn, and objects are destroyed. This provides flexibility without pre-allocating memory.

#### 1.2 Adding Elements (main.py, line 131)
```python
if event.type == pygame.MOUSEBUTTONDOWN:
    b = logic.make_bullet(player_x, player_y, mx, my)
    if b:
        bullets.append(b)  # Add new bullet to array
```

**Time Complexity:** O(1) amortized time for append operation.

#### 1.3 List Comprehension - Filtering (game_logic.py, lines 102-103)
```python
def move_bullets(bullets):
    for b in bullets:
        b["x"] += b["vx"]  # Update position
        b["y"] += b["vy"]
    # Filter bullets that are still on screen
    return [b for b in bullets
            if -10 < b["x"] < WIDTH + 10 and -10 < b["y"] < HEIGHT + 10]
```

**Purpose:** Removes bullets that have left the screen to optimize performance.

**Time Complexity:** O(n) where n = number of bullets

#### 1.4 Array Iteration (game_logic.py, lines 98-103)
```python
def move_bullets(bullets):
    for b in bullets:              # Iterate through each bullet
        b["x"] += b["vx"]          # Update x position
        b["y"] += b["vy"]          # Update y position
```

**Purpose:** Updates position of all bullets each frame.

**Time Complexity:** O(n) where n = number of bullets

#### 1.5 Message Array (main.py, lines 49-53)
```python
message = [
    "YOU'RE STUCK IN SPACE",
    "WITH A BUNCH OF METEORS,",
    "DESTROY THEM!"
]
```

**Purpose:** Stores text messages to display during title sequence.

---

### 2. **Hash Tables / Dictionaries**

**Definition:** A hash table uses a hash function to map keys to values, enabling O(1) average lookup time.

**Implementation in Game:**

#### 2.1 Enemy Objects (game_logic.py, lines 35-43)
```python
# Enemy is stored as a dictionary (hash table)
return {
    "x": x,                        # Key: position x-coordinate
    "y": y,                        # Key: position y-coordinate
    "speed": 1.0 + score * 0.002, # Key: movement speed
    "hp": 4,                       # Key: health points
    "points": 2,                   # Key: score reward
    "radius": 26,                  # Key: collision radius
    "type": "meteor"               # Key: object type
}
```

**Why Hash Table:** 
- Fast O(1) key-value lookup by property name
- No need to remember index positions
- Easy to add new properties

**Hash Function Example:**
```
"hp" → Hash Function → Index 4 → Value: 4
"x"  → Hash Function → Index 1 → Value: 250.5
```

#### 2.2 Bullet Objects (game_logic.py, line 82)
```python
return {
    "x": px,                           # x position
    "y": py,                           # y position
    "vx": dx / dist * spd,             # x velocity
    "vy": dy / dist * spd              # y velocity
}
```

**Usage:** Every bullet in the game is a dictionary with velocity and position properties.

#### 2.3 Dictionary Access (game_logic.py, line 131)
```python
if math.hypot(b["x"] - e["x"], b["y"] - e["y"]) < e["radius"]:
    dead_bullets.add(bi)
    e["hp"] -= 1  # Access hash table with key "hp"
```

**Time Complexity:** O(1) for key access

#### 2.4 Leaderboard Entry (game_logic.py, line 19)
```python
board.append({"name": name[:3].upper(), "score": score})
```

**Purpose:** Each leaderboard entry is a dictionary with "name" and "score" keys.

#### 2.5 Particle Objects (game_logic.py, line 134)
```python
particles.append({"x": e["x"], "y": e["y"], "life": 1.0})
```

**Purpose:** Stores explosion particle effects as dictionaries.

---

### 3. **Sets**

**Definition:** A set is an unordered collection of unique elements, with O(1) average lookup time.

**Implementation in Game:**

#### 3.1 Collision Tracking (game_logic.py, lines 124-125)
```python
def check_bullet_enemy(bullets, enemies, particles, score):
    dead_bullets = set()  # Set to store indices of dead bullets
    dead_enemies = set()  # Set to store indices of dead enemies
```

**Why Used:** Sets provide efficient O(1) membership testing to check if an object should be removed.

#### 3.2 Adding to Set (game_logic.py, lines 130-133)
```python
for bi, b in enumerate(bullets):
    for ei, e in enumerate(enemies):
        if math.hypot(b["x"] - e["x"], b["y"] - e["y"]) < e["radius"]:
            dead_bullets.add(bi)  # Add bullet index to set O(1)
            e["hp"] -= 1
            if e["hp"] <= 0:
                dead_enemies.add(ei)  # Add enemy index to set O(1)
```

**Time Complexity:** O(1) for add operation

#### 3.3 Set Membership Testing (game_logic.py, lines 138-139)
```python
# Filter using set membership testing
bullets = [b for i, b in enumerate(bullets) if i not in dead_bullets]
enemies = [e for i, e in enumerate(enemies) if i not in dead_enemies]
```

**Purpose:** Efficiently remove dead objects from arrays.

**Time Complexity:** O(1) for "not in" operation on sets

**Complexity of entire operation:** O(n) for filtering n objects

---

### 4. **Sorting Algorithms**

**Definition:** Sorting arranges elements in a specific order.

**Implementation in Game:**

#### 4.1 Leaderboard Sorting (game_logic.py, line 20)
```python
def save_score(name, score):
    board = load_scores()
    board.append({"name": name[:3].upper(), "score": score})
    board.sort(key=lambda x: x["score"], reverse=True)  # Sort by score
    board = board[:5]  # Keep top 5
```

**Algorithm Used:** Python's `sort()` uses Timsort (O(n log n))

**Purpose:** Ranks leaderboard scores from highest to lowest.

**Code Breakdown:**
- `key=lambda x: x["score"]` — Extract score for comparison
- `reverse=True` — Sort in descending order (highest first)
- `board[:5]` — Keep only top 5 scores

**Time Complexity:** O(n log n) where n = number of scores

---

## Time Complexity Analysis

### Operation Performance Summary

| Operation | Data Structure | Time Complexity | Used Where |
|---|---|---|---|
| Add object | Array | O(1) amortized | Spawn bullet/enemy |
| Access property | Hash Table | O(1) avg | Get x, y, hp, etc. |
| Iterate all objects | Array | O(n) | Update positions |
| Remove object | Set membership test | O(1) | Collision cleanup |
| Filter array | Array + comprehension | O(n) | Remove off-screen objects |
| Sort leaderboard | Timsort | O(n log n) | Save score |
| Collision detection | Nested loops + distance | O(n²) | Check all bullet-enemy pairs |

### Bottleneck: Collision Detection

The most expensive operation is collision detection (lines 127-136):
```python
for bi, b in enumerate(bullets):        # O(n) - bullets
    for ei, e in enumerate(enemies):    # O(m) - enemies
        # Distance calculation
        if math.hypot(...) < e["radius"]:  # O(1)
            # Process collision
# Total: O(n × m) where n = bullets, m = enemies
```

**Impact:** With 100 bullets and 50 enemies, this is 5,000 comparisons per frame!

**Optimization Tip:** Could use spatial partitioning (grid/quadtree) to reduce to O(n log n).

---

## Code Walkthrough: Frame Update Cycle

Here's how data structures are used in a single game frame:

```
FRAME UPDATE (60 times per second):
│
├─ bullets array → move_bullets() → filter out-of-bounds
│  └─ Time: O(n) where n = bullets
│
├─ enemies array → move_enemies() → update positions
│  └─ Time: O(m) where m = enemies  
│
├─ COLLISION DETECTION
│  ├─ Create dead_bullets set
│  ├─ Create dead_enemies set
│  ├─ Nested loop: O(n × m) comparisons
│  └─ Add indices to sets: O(1) each
│
├─ Filter arrays using sets
│  ├─ bullets = [... if i not in dead_bullets]  O(n)
│  └─ enemies = [... if i not in dead_enemies]  O(m)
│
└─ UPDATE LEADERBOARD (when score saved)
   └─ Sort hash tables in array: O(k log k) where k = scores
```

---

## Example: Complete Game Object Lifecycle

### 1. **Bullet Creation** (Hash Table + Array)
```python
# game_logic.py - Create bullet as hash table
bullet = {
    "x": px,                    # Hash: "x" → px
    "y": py,                    # Hash: "y" → py
    "vx": velocity_x,           # Hash: "vx" → velocity_x
    "vy": velocity_y            # Hash: "vy" → velocity_y
}

# main.py - Add to array
bullets.append(bullet)  # O(1) amortized
```

### 2. **Bullet Movement** (Array Iteration)
```python
# game_logic.py - move_bullets()
for b in bullets:           # O(n) iteration
    b["x"] += b["vx"]      # O(1) hash table access
    b["y"] += b["vy"]      # O(1) hash table access
```

### 3. **Collision Detection** (Nested Loop + Set)
```python
# game_logic.py - check_bullet_enemy()
dead_bullets = set()        # O(1) create
for bi, b in enumerate(bullets):    # O(n) bullets
    for ei, e in enumerate(enemies):    # O(m) enemies
        distance = math.hypot(b["x"] - e["x"], ...)  # O(1) hash access
        if distance < e["radius"]:
            dead_bullets.add(bi)    # O(1) set add
```

### 4. **Cleanup** (Set Membership Testing)
```python
# game_logic.py - filter using set
bullets = [b for i, b in enumerate(bullets) if i not in dead_bullets]
# O(n) iteration with O(1) set membership test per bullet
```

---

## Memory Usage

### Space Complexity

```
Array Storage:
├─ bullets array: O(b) where b = number of bullets
├─ enemies array: O(e) where e = number of enemies
├─ rays array: O(r) where r = number of rays
└─ particles array: O(p) where p = number of particles

Hash Tables:
├─ Each bullet: 4 properties (x, y, vx, vy) = O(1) fixed
├─ Each enemy: 7 properties (x, y, speed, hp, points, radius, type) = O(1) fixed
├─ Each ray: 6 properties = O(1) fixed
└─ Each particle: 3 properties = O(1) fixed

Sets:
├─ dead_bullets set: O(number of collisions per frame)
└─ dead_enemies set: O(number of collisions per frame)

Total: O(b + e + r + p) where b, e, r, p are dynamic counts
```

---

## Performance Optimization Recommendations

### Current Bottlenecks:

1. **O(n²) Collision Detection**
   - Current: 5,000+ comparisons with 100 bullets × 50 enemies
   - Solution: Use spatial partitioning (grid-based collision detection)

2. **Array Filtering**
   - Removes out-of-bounds objects every frame
   - Could use object pooling instead

3. **Full Leaderboard Sort**
   - Unnecessary to sort every time
   - Could use insertion sort or priority queue

### Recommended Improvements:

```python
# Use a spatial grid for collision detection
class SpatialGrid:
    def __init__(self, cell_size=50):
        self.cell_size = cell_size
        self.grid = {}
    
    def add(self, obj_id, x, y):
        cell = (int(x // self.cell_size), int(y // self.cell_size))
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(obj_id)
    
    def get_nearby(self, x, y, radius=100):
        # Only check objects in nearby cells
        pass
```

---

## Summary of Data Structures

### ✅ Implemented:

1. **Dynamic Arrays (Lists)**
   - Used for: bullets, enemies, rays, particles
   - Complexity: O(1) append, O(n) iteration
   - Real-world analogy: Cargo train that can grow or shrink

2. **Hash Tables (Dictionaries)**
   - Used for: Game objects (enemy stats, bullet velocity, etc.)
   - Complexity: O(1) access
   - Real-world analogy: Filing cabinet with labeled drawers

3. **Sets**
   - Used for: Dead object tracking in collision detection
   - Complexity: O(1) add, O(1) membership test
   - Real-world analogy: A guest list (fast membership check)

4. **Sorting Algorithms**
   - Used for: Leaderboard ranking
   - Complexity: O(n log n) using Timsort
   - Real-world analogy: Arranging test scores from highest to lowest

### ❌ Not Implemented:

- Linked Lists (could replace arrays for removal efficiency)
- Queues (could manage enemy spawning)
- Stacks (could manage undo/redo)
- Trees (could optimize collision detection with spatial trees)
- Graphs (could represent game state as nodes)

---

## Conclusion

The Meteor Miner game effectively demonstrates three core data structures:

1. **Arrays** provide dynamic storage for game objects
2. **Hash Tables** store game entity properties efficiently
3. **Sets** enable fast collision cleanup
4. **Sorting** ranks high scores for the leaderboard

These data structures are chosen for their **performance characteristics** — allowing the game to handle real-time updates at 60 frames per second with hundreds of game objects.

The main performance bottleneck is the O(n²) collision detection, which could be optimized using more advanced data structures like spatial partitioning trees.

---

## Appendix: Key Code References

### File: `game_logic.py`
- Lines 10-23: Leaderboard (arrays + sorting)
- Lines 26-53: Enemy spawning (hash tables)
- Lines 76-82: Bullet creation (hash tables)
- Lines 98-112: Movement functions (array iteration)
- Lines 123-140: Collision detection (nested arrays + sets)

### File: `main.py`
- Lines 107-110: Game object arrays initialization
- Lines 131: Array append operation
- Lines 136-152: Array iteration and updates
- Lines 154-162: Collision detection calls

### File: `visuals.py`
- Lines 172-175: Array iteration for drawing (loop through collections)

---

**End of Document**
