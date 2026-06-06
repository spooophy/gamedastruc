import pygame
import math
from game_logic import WIDTH, HEIGHT, load_scores   # importing from game_logic!


BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GRAY = (80,  80,  80)
YELLOW = (255, 255,  0)
PURPLE = (160,  30, 255)
font_big = None
font_small = None
font_tiny = None

def init_fonts():
    global font_big, font_small, font_tiny
    try:
        font_big = pygame.font.Font("PressStart2P-Regular.ttf", 20)
        font_small = pygame.font.Font("PressStart2P-Regular.ttf", 10)
        font_tiny = pygame.font.Font("PressStart2P-Regular.ttf", 8)
    except FileNotFoundError:
        font_big = pygame.font.SysFont("monospace", 28, bold=True)
        font_small = pygame.font.SysFont("monospace", 14, bold=True)
        font_tiny = pygame.font.SysFont("monospace", 12, bold=True)

def pixel_rect(surface, color, x, y, w, h, ps=4):
    """Rectangle snapped to a pixel grid — gives that chunky retro look."""
    sx = round(x / ps) * ps
    sy = round(y / ps) * ps
    pygame.draw.rect(surface, color, (sx, sy, w, h))

def draw_grid(surface):
    for gx in range(0, WIDTH, 40):
        pygame.draw.line(surface, (20, 20, 20), (gx, 0), (gx, HEIGHT))
    for gy in range(0, HEIGHT, 40):
        pygame.draw.line(surface, (20, 20, 20), (0, gy), (WIDTH, gy))

def draw_scanlines(surface):
    """CRT scanline overlay — always draw this last."""
    line = pygame.Surface((WIDTH, 2), pygame.SRCALPHA)
    line.fill((0, 0, 0, 40))
    for y in range(0, HEIGHT, 4):
        surface.blit(line, (0, y))


# UI ELEMENTS
def draw_button(surface, rect, text, highlighted=False):
    color = YELLOW if highlighted else WHITE
    pixel_rect(surface, color, rect.x, rect.y, rect.width, rect.height)
    pygame.draw.rect(surface, BLACK, rect, 3)
    label = font_small.render(text, True, BLACK)
    surface.blit(label, (rect.centerx - label.get_width() // 2,
                         rect.centery - label.get_height() // 2))


def draw_main_menu(surface, start_hover=False, leaderboard_hover=False):
    surface.fill(BLACK)
    draw_grid(surface)

    title = font_big.render("METEOR MINER", True, WHITE)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))

    start_rect = pygame.Rect(WIDTH // 2 - 90, 190, 180, 50)
    board_rect = pygame.Rect(WIDTH // 2 - 90, 260, 180, 50)

    draw_button(surface, start_rect, "START GAME", start_hover)
    draw_button(surface, board_rect, "LEADERBOARD", leaderboard_hover)

    hint = font_tiny.render("CLICK A BUTTON OR PRESS ENTER", True, GRAY)
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 340))

    draw_scanlines(surface)
    pygame.display.flip()


def draw_title_sequence(surface, message_lines, countdown_text):
    surface.fill(BLACK)
    draw_grid(surface)

    y = HEIGHT // 2 - 80
    for line in message_lines:
        text = font_big.render(line, True, WHITE)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += text.get_height() + 10

    count = font_big.render(countdown_text, True, YELLOW)
    surface.blit(count, (WIDTH // 2 - count.get_width() // 2, y + 20))
    
    hint = font_tiny.render("GET READY...", True, GRAY)
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, y + count.get_height() + 40))

    draw_scanlines(surface)
    pygame.display.flip()

# GAME OBJECT DRAWING
def draw_player(surface, x, y, mouse_x, mouse_y):
    angle  = math.atan2(mouse_y - y, mouse_x - x)
    ship   = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.rect(ship, WHITE, (4,  4, 16, 16))   # body
    pygame.draw.rect(ship, BLACK, (8,  8,  8,  8))   # cockpit
    pygame.draw.rect(ship, WHITE, (18, 10,  8,  4))   # barrel
    rotated = pygame.transform.rotate(ship, -math.degrees(angle))
    rect    = rotated.get_rect(center=(x, y))
    surface.blit(rotated, rect)

def draw_enemy(surface, e, frame):
    x, y = int(e["x"]), int(e["y"])
    radius = e.get("radius", 18)
    t = (frame // 8) % 2

    pixel_rect(surface, WHITE, x-radius, y-radius, radius * 2, radius * 2)
    pixel_rect(surface, BLACK, x-radius//2, y-radius//2, radius, radius)

    if t == 0:
        pixel_rect(surface, WHITE, x-radius-4, y-6,  4, 4)
        pixel_rect(surface, WHITE, x+radius,   y-6,  4, 4)
        pixel_rect(surface, WHITE, x-6,        y+radius, 4, 4)
        pixel_rect(surface, WHITE, x+2,        y+radius, 4, 4)
    else:
        pixel_rect(surface, WHITE, x-radius-4, y+2,  4, 4)
        pixel_rect(surface, WHITE, x+radius,   y+2,  4, 4)
        pixel_rect(surface, WHITE, x-6,        y-radius-4, 4, 4)
        pixel_rect(surface, WHITE, x+2,        y-radius-4, 4, 4)

def draw_bullet(surface, b):
    pixel_rect(surface, WHITE, b["x"]-3, b["y"]-3, 8, 8)
    pixel_rect(surface, BLACK, b["x"]-1, b["y"]-1, 4, 4)


def draw_ray(surface, r):
    x, y = int(r["x"]), int(r["y"])
    angle = math.atan2(r["vy"], r["vx"]) if r["vx"] or r["vy"] else 0
    dx = math.cos(angle) * 18
    dy = math.sin(angle) * 18
    pygame.draw.line(surface, PURPLE, (x - dx, y - dy), (x + dx, y + dy), 4)
    pygame.draw.circle(surface, YELLOW, (x, y), 6)


def draw_explosion(surface, p):
    size = int(p["life"] * 20 / 4) * 4
    if size < 4:
        return
    x, y = int(p["x"]), int(p["y"])
    pixel_rect(surface, WHITE, x - size,    y - size,    size * 2, size * 2)
    pixel_rect(surface, BLACK, x - size//2, y - size//2, size,     size)


# HUD
def draw_hud(surface, score, lives):
    surface.blit(font_small.render(f"SCORE: {str(score).zfill(4)}", True, WHITE), (10, 10))
    surface.blit(font_small.render(f"LIVES: {'I' * lives}",          True, WHITE), (10, 30))


# SCREENS
def draw_game_over_screen(surface):
    surface.fill(BLACK)
    draw_grid(surface)
    over = font_big.render("GAME OVER", True, WHITE)
    cont = font_tiny.render("PRESS ANY KEY", True, GRAY)
    surface.blit(over, (WIDTH//2 - over.get_width()//2, 210))
    surface.blit(cont, (WIDTH//2 - cont.get_width()//2, 290))
    draw_scanlines(surface)
    pygame.display.flip()

def draw_name_entry_screen(surface, player_name):
    surface.fill(BLACK)
    draw_grid(surface)

    board = load_scores()   # calling game_logic from visuals to get the scores for the leaderboard display on the name entry screen

    title = font_big.render("HIGH SCORES", True, WHITE)
    surface.blit(title, (WIDTH //2 - title.get_width()//2, 40))
    pygame.draw.line(surface, WHITE, (60, 80), (WIDTH - 60, 80), 2)

    for i, entry in enumerate(board):
        rank = font_small.render(f"{i+1}.", True, WHITE)
        name = font_small.render(entry["name"], True, WHITE)
        pts = font_small.render(str(entry["score"]).zfill(4), True, WHITE)
        yp = 105 + i * 36
        surface.blit(rank, (100, yp))
        surface.blit(name, (160, yp))
        surface.blit(pts,  (WIDTH - 160, yp))

    if not board:
        empty = font_small.render("NO SCORES YET", True, GRAY)
        surface.blit(empty, (WIDTH//2 - empty.get_width()//2, 120))

    pygame.draw.line(surface, WHITE, (60, 305), (WIDTH - 60, 305), 2)

    prompt = font_small.render("ENTER YOUR NAME:", True, WHITE)
    surface.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 325))

    blink = "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else " "
    typed = font_big.render(player_name + blink, True, YELLOW)
    surface.blit(typed, (WIDTH//2 - typed.get_width()//2, 365))

    hint = font_tiny.render("PRESS ENTER TO SAVE", True, GRAY)
    surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 455))

    draw_scanlines(surface)
    pygame.display.flip()


def draw_leaderboard_screen(surface):
    surface.fill(BLACK)
    draw_grid(surface)

    title = font_big.render("HIGH SCORES", True, WHITE)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 40))
    pygame.draw.line(surface, WHITE, (60, 80), (WIDTH - 60, 80), 2)

    board = load_scores()
    for i, entry in enumerate(board):
        rank = font_small.render(f"{i+1}.", True, WHITE)
        name = font_small.render(entry["name"], True, WHITE)
        pts = font_small.render(str(entry["score"]).zfill(4), True, WHITE)
        yp = 105 + i * 36
        surface.blit(rank, (100, yp))
        surface.blit(name, (160, yp))
        surface.blit(pts,  (WIDTH - 160, yp)) #yp is the y position   

    if not board:
        empty = font_small.render("NO SCORES YET", True, GRAY)
        surface.blit(empty, (WIDTH//2 - empty.get_width()//2, 120))

    prompt = font_small.render("PRESS ANY KEY OR CLICK TO RETURN", True, GRAY)
    surface.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 430))

    draw_scanlines(surface)
    pygame.display.flip()
