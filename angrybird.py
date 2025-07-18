import os
import sys
import math
import time
import pygame
current_path = os.getcwd()
import pymunk as pm
from data.angry_bird.characters import Bird
from data.angry_bird.level import Level


pygame.init()
screen = pygame.display.set_mode((1200, 650))
redbird = pygame.image.load(
    "resources/angrybird/red-bird3.png").convert_alpha()
background2 = pygame.image.load(
    "resources/angrybird/background3.png").convert_alpha()
sling_image = pygame.image.load(
    "resources/angrybird/sling-3.png").convert_alpha()
full_sprite = pygame.image.load(
    "resources/angrybird/full-sprite.png").convert_alpha()
rect = pygame.Rect(181, 1050, 50, 50)
cropped = full_sprite.subsurface(rect).copy()
pig_image = pygame.transform.scale(cropped, (30, 30))
buttons = pygame.image.load(
    "resources/angrybird/selected-buttons.png").convert_alpha()
pig_happy = pygame.image.load(
    "resources/angrybird/pig_failed.png").convert_alpha()
stars = pygame.image.load(
    "resources/angrybird/stars-edited.png").convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()
rect = pygame.Rect(164, 10, 60, 60)
pause_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()
running = True
# the base of the physics
space = pm.Space()
space.gravity = (0.0, -700.0)
pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_lenght = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0
game_state = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
wall = False

# Static floor
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_body)
for line in static_lines:
    space.add(line)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def load_music():
    """Load the music"""
    song1 = 'resources/sound/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # Fixing bird to the sling rope
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy))/dx)


def draw_level_cleared():
    """Draw level cleared"""
    global game_state
    global bonus_score_once
    global score
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, WHITE)
    if level.number_of_birds >= 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds-1) * 10000
        bonus_score_once = False
        game_state = 4
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))
        if score >= level.one_star and score <= level.two_star:
            screen.blit(star1, (310, 190))
        if score >= level.two_star and score <= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
        if score >= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
            screen.blit(star3, (700, 200))
        screen.blit(score_level_cleared, (550, 400))
        screen.blit(replay_button, (510, 480))
        screen.blit(next_button, (620, 480))


def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed = bold_font3.render("Level Failed", 1, WHITE)
    if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) > 0:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        screen.blit(pig_happy, (380, 120))
        screen.blit(replay_button, (520, 460))


def restart():
    """Delete all objects of the level"""
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []
    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)


def post_solve_bird_pig(arbiter, space, _):
    """Handle bird and pig collision, damage pig, and remove if dead."""
    global score

    # Unpack shapes from collision
    a, b = arbiter.shapes

    # Identify which is bird and pig
    if a.collision_type == 0 and b.collision_type == 1:
        bird_body = a.body
        pig_body = b.body
    elif a.collision_type == 1 and b.collision_type == 0:
        pig_body = a.body
        bird_body = b.body
    else:
        return  # Wrong types

    # Optional: Only damage if collision is strong enough
    impulse_strength = arbiter.total_impulse.length
    if impulse_strength < 50:  # You can tune this threshold
        return

    # Draw impact visual (optional and safe)
    try:
        if 'screen' in globals():
            p = to_pygame(bird_body.position)
            p2 = to_pygame(pig_body.position)
            r = 30
            pygame.draw.circle(screen, BLACK, p, r, 4)
            pygame.draw.circle(screen, RED, p2, r, 4)
    except Exception as e:
        print(f"Drawing error: {e}")

    # Damage and remove pig if life runs out
    pigs_to_remove = []
    for pig in pigs:
        if pig.body == pig_body:
            pig.life -= 20
            print(f"Pig hit! Life = {pig.life}")
            if pig.life <= 0:
                pigs_to_remove.append(pig)
                score += 10000

    for pig in pigs_to_remove:
        try:
            space.remove(pig.shape, pig.body)
        except Exception as e:
            print(f"Failed to remove pig from space: {e}")
        if pig in pigs:
            pigs.remove(pig)


def post_solve_bird_wood(arbiter, space, _):
    """Collision between bird and wood"""
    global score  # Declare global to update it

    poly_to_remove = []

    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes

        # Safely compare wood collisions from both possible shape orders
        shape_a_type = a.collision_type
        shape_b_type = b.collision_type

        # Ensure correct shape is wood
        wood_shape = b if shape_b_type == 2 else (a if shape_a_type == 2 else None)
        if wood_shape is None:
            return False  # Not a wood collision

        # Check collision against beams and columns
        for column in columns:
            if wood_shape == column.shape:
                poly_to_remove.append(column)

        for beam in beams:
            if wood_shape == beam.shape:
                poly_to_remove.append(beam)

        # Remove identified wood parts
        for poly in poly_to_remove:
            try:
                space.remove(poly.shape, poly.body)
            except Exception:
                pass
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)

        score += 5000
        return True

    return False

def post_solve_pig_wood(arbiter, space, _):
    """Collision between pig and wood"""
    global score  # Needed to update score

    pigs_to_remove = []

    if arbiter.total_impulse.length > 700:
        pig_shape, wood_shape = arbiter.shapes

        # Ensure pig_shape is the actual pig by checking collision_type
        if pig_shape.collision_type != 1:
            pig_shape, wood_shape = wood_shape, pig_shape

        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                score += 10000
                if pig.life <= 0:
                    pigs_to_remove.append(pig)

    for pig in pigs_to_remove:
        try:
            space.remove(pig.shape, pig.body)
        except Exception:
            pass
        if pig in pigs:
            pigs.remove(pig)

    return True

# Bird (0) vs Pig (1)
handler = space.add_collision_handler(0, 1)
if handler:
    handler.post_solve = post_solve_bird_pig

# Bird (0) vs Wood (2)
handler = space.add_collision_handler(0, 2)
if handler:
    handler.post_solve = post_solve_bird_wood

# Pig (1) vs Wood (2)
handler = space.add_collision_handler(1, 2)
if handler:
    handler.post_solve = post_solve_pig_wood


# Load music and initialize level
load_music()

# Create level object (ensure pigs, columns, beams are initialized properly)
level = Level(pigs, columns, beams, space)
level.number = 0
level.load_level()

# Ensure these are initialized before the loop
running = True
wall = True
mouse_pressed = False
t1 = time.time() * 1000
counter = 0
restart_counter = False
score = 0
game_state = 0

while running:
    x_mouse, y_mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_w:
                wall = not wall
                if wall:
                    for line in static_lines1:
                        space.add(line)
                else:
                    for line in static_lines1:
                        space.remove(line)

            elif event.key == pygame.K_s:
                space.gravity = (0.0, -10.0)
                level.bool_space = True

            elif event.key == pygame.K_n:
                space.gravity = (0.0, -700.0)
                level.bool_space = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 100 < x_mouse < 250 and 370 < y_mouse < 550:
                mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_pressed and level.number_of_birds > 0:
                mouse_pressed = False
                level.number_of_birds -= 1
                t1 = time.time() * 1000
                xo, yo = 154, 156

                # Clamp the distance
                md = min(mouse_distance, rope_lenght)
                direction = -md if x_mouse > sling_x + 5 else md
                bird = Bird(direction, angle, xo, yo, space)
                birds.append(bird)

                if level.number_of_birds == 0:
                    t2 = time.time()

            # UI Buttons & States
            if x_mouse < 60 and 90 < y_mouse < 155:
                game_state = 1

            if game_state == 1:
                if x_mouse > 500 and 200 < y_mouse < 300:
                    game_state = 0
                elif x_mouse > 500 and y_mouse > 300:
                    restart()
                    level.load_level()
                    bird_path.clear()
                    game_state = 0

            elif game_state == 3 and 500 < x_mouse < 620 and y_mouse > 450:
                restart()
                level.load_level()
                bird_path.clear()
                score = 0
                game_state = 0

            elif game_state == 4:
                if x_mouse > 610 and y_mouse > 450:
                    level.number += 1
                    restart()
                    level.load_level()
                    bird_path.clear()
                    score = 0
                    bonus_score_once = True
                    game_state = 0
                elif 500 < x_mouse < 610 and y_mouse > 450:
                    restart()
                    level.load_level()
                    bird_path.clear()
                    score = 0
                    game_state = 0

    # --- Drawing ---
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))

    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)

    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)

    if level.number_of_birds > 0:
        for i in range(level.number_of_birds - 1):
            screen.blit(redbird, (100 - i * 35, 508))

    if mouse_pressed and level.number_of_birds > 0:
        sling_action()
    else:
        if time.time() * 1000 - t1 > 300 and level.number_of_birds > 0:
            screen.blit(redbird, (130, 426))
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y - 8),
                             (sling2_x, sling2_y - 7), 5)

    # Birds update
    birds_to_remove = []
    for bird in birds:
        if bird.shape.body.position.y < 0:
            birds_to_remove.append(bird)
        p = to_pygame(bird.shape.body.position)
        screen.blit(redbird, (p[0] - 22, p[1] - 20))
        pygame.draw.circle(screen, BLUE, p, int(bird.shape.radius), 2)
        if counter >= 3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True

    # Pigs update
    pigs_to_remove = []
    for pig in pigs:
        if pig.shape.body.position.y < 0:
            pigs_to_remove.append(pig.shape)

        p = to_pygame(pig.shape.body.position)
        img = pygame.transform.rotate(pig_image, math.degrees(pig.shape.body.angle))
        x, y = p[0] - img.get_width() // 2, p[1] - img.get_height() // 2
        screen.blit(img, (x, y))
        pygame.draw.circle(screen, BLUE, p, int(pig.shape.radius), 2)

    # Static lines
    for line in static_lines:
        body = line.body
        p1 = to_pygame(body.position + line.a.rotated(body.angle))
        p2 = to_pygame(body.position + line.b.rotated(body.angle))
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])

    # Columns and Beams
    for col in columns:
        col.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)

    # Remove birds and pigs from space
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig, pig.body)
        pigs.remove(pig)

    # Physics Step
    for _ in range(2):
        space.step(1.0 / 100)

    # Second part of the sling
    screen.blit(sling_image, (120, 420), pygame.Rect(0, 0, 60, 200))

    # Score
    screen.blit(bold_font.render("SCORE", 1, WHITE), (1060, 90))
    screen.blit(bold_font.render(str(score), 1, WHITE), (1060 if score else 1100, 130))
    screen.blit(pause_button, (10, 90))

    if game_state == 1:
        screen.blit(play_button, (500, 200))
        screen.blit(replay_button, (500, 300))

    draw_level_cleared()
    draw_level_failed()

    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    if restart_counter:
        counter = 0
        restart_counter = False
    counter += 1