import math
import random
import json

WIDTH = 600
HEIGHT = 500
SCORES_FILE = "scores.json"

# LEADERBOARD
def load_scores(): #uses json to load the scores from the scores.json file, which is used for the leaderboard.
    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_score(name, score): 
    board = load_scores()
    board.append({"name": name[:3].upper(), "score": score})
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:5]
    with open(SCORES_FILE, "w") as f:
        json.dump(board, f)

# SPAWNING
def spawn_enemy(score, elapsed_frames):
    side = random.randint(0, 3)
    if  side == 0: x, y = random.randint(0, WIDTH), -20
    elif side == 1: x, y = WIDTH + 20, random.randint(0, HEIGHT)
    elif side == 2: x, y = random.randint(0, WIDTH), HEIGHT + 20
    else:          
        x, y = -20, random.randint(0, HEIGHT)

    if elapsed_frames >= 20 * 60 and random.random() < 0.33:
        return {
            "x": x,
            "y": y,
            "speed": 1.0 + score * 0.002,
            "hp": 4,
            "points": 2,
            "radius": 26,
            "type": "meteor"
        }

    return {
        "x": x,
        "y": y,
        "speed": 1.2 + score * 0.003,
        "hp": 2,
        "points": 1,
        "radius": 18,
        "type": "meteor"
    }

def spawn_gamma_ray():
    side = random.randint(0, 3)
    speed = 4.0
    if  side == 0:
        x, y, vx, vy = random.randint(0, WIDTH), -20, 0, speed
    elif side == 1:
        x, y, vx, vy = WIDTH + 20, random.randint(0, HEIGHT), -speed, 0
    elif side == 2:
        x, y, vx, vy = random.randint(0, WIDTH), HEIGHT + 20, 0, -speed
    else:
        x, y, vx, vy = -20, random.randint(0, HEIGHT), speed, 0
    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "radius": 14,
        "damage": 2,
        "type": "gamma"
    }

def make_bullet(px, py, mx, my):
    dx, dy = mx - px, my - py
    dist = math.hypot(dx, dy)
    if dist == 0:
        return None
    spd = 10
    return {"x": px, "y": py, "vx": dx / dist * spd, "vy": dy / dist * spd}


# MOVEMENT
def move_player(player_x, player_y, keys, speed):
    import pygame
    if (keys[pygame.K_w] or keys[pygame.K_UP])    and player_y > 14:
        player_y -= speed
    if (keys[pygame.K_s] or keys[pygame.K_DOWN])  and player_y < HEIGHT - 14:
        player_y += speed
    if (keys[pygame.K_a] or keys[pygame.K_LEFT])  and player_x > 14:
        player_x -= speed
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < WIDTH - 14:
        player_x += speed
    return player_x, player_y

def move_bullets(bullets):
    for b in bullets:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
    return [b for b in bullets
            if -10 < b["x"] < WIDTH + 10 and -10 < b["y"] < HEIGHT + 10]

def move_enemies(enemies, player_x, player_y):
    for e in enemies:
        dx, dy = player_x - e["x"], player_y - e["y"]
        dist = math.hypot(dx, dy)
        if dist > 0:
            e["x"] += dx / dist * e["speed"]
            e["y"] += dy / dist * e["speed"]
    return enemies


def move_rays(rays):
    for r in rays:
        r["x"] += r["vx"]
        r["y"] += r["vy"]
    return [r for r in rays
            if -30 < r["x"] < WIDTH + 30 and -30 < r["y"] < HEIGHT + 30]

# COLLISIONS
def check_bullet_enemy(bullets, enemies, particles, score):
    dead_bullets = set()
    dead_enemies = set()

    for bi, b in enumerate(bullets):
        for ei, e in enumerate(enemies):
            if math.hypot(b["x"] - e["x"], b["y"] - e["y"]) < e["radius"]:
                dead_bullets.add(bi)
                e["hp"] -= 1
                if e["hp"] <= 0:
                    dead_enemies.add(ei)
                    particles.append({"x": e["x"], "y": e["y"], "life": 1.0})
                    score += e.get("points", 1)
                break

    bullets = [b for i, b in enumerate(bullets) if i not in dead_bullets]
    enemies = [e for i, e in enumerate(enemies) if i not in dead_enemies]
    return bullets, enemies, particles, score

def check_player_enemy(enemies, particles, player_x, player_y, lives):
    for e in enemies[:]:
        if math.hypot(player_x - e["x"], player_y - e["y"]) < e["radius"] + 14:
            enemies.remove(e)
            particles.append({"x": player_x, "y": player_y, "life": 1.0})
            lives -= 1
    return enemies, particles, lives


def check_player_rays(rays, particles, player_x, player_y, lives):
    for r in rays[:]:
        if math.hypot(player_x - r["x"], player_y - r["y"]) < r["radius"] + 14:
            rays.remove(r)
            particles.append({"x": player_x, "y": player_y, "life": 1.0})
            lives -= r["damage"]
    return rays, particles, lives

# PARTICLES  (used for explosions)
def update_particles(particles):
    for p in particles:
        p["life"] -= 0.06
    return [p for p in particles if p["life"] > 0]
