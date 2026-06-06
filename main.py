import pygame
import game_logic as logic # all the game rules
import visuals  # all the drawing

pygame.init()
screen = pygame.display.set_mode((logic.WIDTH, logic.HEIGHT))
pygame.display.set_caption("meteor shower")
clock  = pygame.time.Clock()
visuals.init_fonts()

# SCREENS  (event handling lives here in main)
def game_over_screen():
    visuals.draw_game_over_screen(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True

def name_entry_screen(final_score):
    player_name = ""
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    logic.save_score(player_name, final_score)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 3 and event.unicode.isalpha():
                    player_name += event.unicode.upper()
        visuals.draw_name_entry_screen(screen, player_name)

def leaderboard_screen():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True
        visuals.draw_leaderboard_screen(screen)

def title_sequence():
    message = [
        "YOU'RE STUCK IN SPACE",
        "WITH A BUNCH OF METEORS,",
        "DESTROY THEM!"
    ]
    start_time = pygame.time.get_ticks()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        elapsed = pygame.time.get_ticks() - start_time
        countdown = 3 - elapsed // 1000
        if countdown <= 0:
            break

        visuals.draw_title_sequence(screen, message, f"{countdown}..")

    return True


def menu_screen():
    start_rect = pygame.Rect(logic.WIDTH // 2 - 90, 190, 180, 50)
    board_rect = pygame.Rect(logic.WIDTH // 2 - 90, 260, 180, 50)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        start_hover = start_rect.collidepoint(mx, my)
        board_hover = board_rect.collidepoint(mx, my)
        visuals.draw_main_menu(screen, start_hover, board_hover)

        if click:
            if start_hover:
                return "start"
            if board_hover:
                return "leaderboard"

# MAIN GAME LOOP
def run_game():
    # initialize player and game state
    player_x = logic.WIDTH  // 2
    player_y = logic.HEIGHT - 80
    speed = 3

    # lists to hold all the game objects
    bullets = []
    enemies = []
    rays = []
    particles = []
    score = 0
    lives = 3
    frame = 0
    spawn_timer = 0
    spawn_rate = 90
    ray_timer = 0
    ray_rate = 70

    while True:
        clock.tick(60)
        frame += 1
        mx, my = pygame.mouse.get_pos()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                b = logic.make_bullet(player_x, player_y, mx, my)
                if b:
                    bullets.append(b)

        # update (all logic, no drawing)
        keys = pygame.key.get_pressed()
        player_x, player_y = logic.move_player(player_x, player_y, keys, speed)
        bullets = logic.move_bullets(bullets)

        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            enemies.append(logic.spawn_enemy(score, frame))
            spawn_timer = 0
            spawn_rate = max(25, spawn_rate - 0.4)

        if frame >= 60 * 60:
            ray_timer += 1
            if ray_timer >= ray_rate:
                rays.append(logic.spawn_gamma_ray())
                ray_timer = 0
                ray_rate = max(25, ray_rate - 0.3)

        enemies = logic.move_enemies(enemies, player_x, player_y)
        rays = logic.move_rays(rays)

        bullets, enemies, particles, score = logic.check_bullet_enemy(
            bullets, enemies, particles, score
        )
        enemies, particles, lives = logic.check_player_enemy(
            enemies, particles, player_x, player_y, lives
        )
        rays, particles, lives = logic.check_player_rays(
            rays, particles, player_x, player_y, lives
        )
        particles = logic.update_particles(particles)

        if lives <= 0:
            return score

        # draw (calling all the visuals, no logic)
        screen.fill(visuals.BLACK)
        visuals.draw_grid(screen)

        for p in particles: visuals.draw_explosion(screen, p)
        for r in rays: visuals.draw_ray(screen, r)
        for b in bullets: visuals.draw_bullet(screen, b)
        for e in enemies: visuals.draw_enemy(screen, e, frame)
        visuals.draw_player(screen, player_x, player_y, mx, my)

        visuals.draw_scanlines(screen)
        visuals.draw_hud(screen, score, lives)

        pygame.display.flip()

# ENTRY POINT
running = True
while running:
    action = menu_screen()
    if action is None:
        break
    if action == "leaderboard":
        if not leaderboard_screen():
            break
        continue

    if not title_sequence():
        break

    final_score = run_game()
    if final_score is None:
        break

    if not game_over_screen():
        break

    name_entry_screen(final_score)

pygame.quit()
