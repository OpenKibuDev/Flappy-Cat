import pygame
import random
import tkinter as tk
from tkinter import messagebox

# SETUP
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Flappy Cat")
clock = pygame.time.Clock()

# SCREEN SIZE
screen_x, screen_y = pygame.display.get_window_size()

# VARIABLES
gravitation = 0
can_jump = True
can_change = False
is_up = False
death = False
score = -1

# CAT
cat = pygame.image.load("sprites/cat.png")
the_x = 200
the_y = screen_y/2

# PIPE
pipe = pygame.image.load("sprites/pipe.png")
pipe_x = 1200
pipe_y = random.randint(-500,0) or random.randint(400,700)

# SOUNDS
die = pygame.mixer.Sound("sounds/die.mp3")
hit = pygame.mixer.Sound("sounds/hit.mp3")
point = pygame.mixer.Sound("sounds/point.mp3")
wing = pygame.mixer.Sound("sounds/wing.mp3")

# SCORE
font = pygame.font.SysFont("Comic Sans MS", 180)
color = (0,60,20)

# GAME
running = True
dead = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    screen.fill((208, 246, 255))


    # THE CAT
    if gravitation != -20:
        gravitation -= 1

    if key[pygame.K_SPACE] and can_jump:
        gravitation = 10
        wing.play()
        can_jump = False

    if not key[pygame.K_SPACE] and can_jump != True:
        can_jump = True

    if the_y >= 720 and not key[pygame.K_SPACE]:
        gravitation = 0
    elif key[pygame.K_SPACE] and the_y >= 720:
        the_y = 719
        gravitation = 10
        wing.play


    cat_rotated = pygame.transform.rotate(cat, gravitation)

    the_y -= gravitation

    cat_rect = cat_rotated.get_rect(center = (the_x, the_y))

    screen.blit(cat_rotated,cat_rect)

    cat_hitbox = cat_rect.inflate(-100, -100)




    # THE PIPE

    random_num = random.randint(1,2)

    if pipe_x >= -150:
        pipe_x -= 20
    elif pipe_x <= -150:
        can_change = True
        pipe_x = 1200
        point.play()
        score += 1


    if random_num == 1 and can_change:
        pipe_y = random.randint(-400,0)
        is_up = True
        can_change = False
    elif random_num == 2 and can_change:
        pipe_y = random.randint(400,700)
        is_up = False
        can_change = False

    if is_up:
        pipe_y_copy = pipe_y + 772
    elif is_up != True:
        pipe_y_copy = pipe_y - 772

    pipe_hitbox = pipe.get_rect(topleft =(pipe_x, pipe_y))
    pipe_copy_hitbox = pipe.get_rect(topleft =(pipe_x, pipe_y_copy))
    screen.blit(pipe, (pipe_x, pipe_y))
    screen.blit(pipe, (pipe_x, pipe_y_copy))


    # SCORE
    text_surface = font.render(str(score), True, color)
    text_rect = text_surface.get_rect(center = (screen_x/2, 100))
    screen.blit(text_surface, text_rect)

    if score == 999:
        running = False


    # DEATH
    if cat_hitbox.colliderect(pipe_hitbox) or cat_hitbox.colliderect(pipe_copy_hitbox):
        dead = True
        running = False
    clock.tick(30)
    pygame.display.update()

was_hit = True
fell = False

while dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = False
    
    if was_hit:
        hit.play()
        was_hit = False
        fell = True
    if fell:
        pygame.time.delay(500)
        die.play()
        pygame.time.delay(1000)
        dead = False
        death = True
pygame.quit()

root = tk.Tk()
root.withdraw()

if death:
    messagebox.showerror("You died", "GAME OVER" + chr(10)+"I don't know what to make as a dead screen.")
elif score == 999:
    messagebox.showwarning("Secret","SECRET FOUND" + chr(10) + "Why would you play this so far?")