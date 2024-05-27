# Frogger
import pygame
import random

# Functions


def draw_frog(x: int, y: int):
    screen.blit(frog_char_img_trans, (x, y))


def frog_movement(frog_x: int, frog_y: int, direction: str) -> tuple:
    if direction == 'up' and frog_y > 50:  # Prevents frog from going out of the map
        frog_y -= box_size
    if direction == 'down' and frog_y < HEIGHT - 100:
        frog_y += box_size
    if direction == 'left' and frog_x > 50:
        frog_x -= box_size
    if direction == 'right' and frog_x < WIDTH - 100:
        frog_x += box_size
    return frog_x, frog_y


def generate_car() -> tuple:  # Generates a random car
    y_pos = random.choice(car_pos)

    if y_pos == 600 or y_pos == 500:
        car_direction = 1  # come in from right
        x_pos = 0
    else:
        car_direction = 0  # come in from left
        x_pos = WIDTH
    speed = random.randint(15, 17) / 10  # Speed ranges from 1.5-1.7

    return x_pos, y_pos, speed, car_direction  # Returns a tuple with all the information needed to draw a car


def draw_car(car: list):  # Draws the cars on screen
    for i in car:
        x_pos, y_pos, speed, car_direction = i
        # ASSIGNING EACH Y POSITION ITS OWN CAR TYPE
        if y_pos == 650:
            screen.blit(car_1_img_trans, (x_pos, y_pos))
        elif y_pos == 600:
            screen.blit(car_2_img_trans, (x_pos, y_pos))
        elif y_pos == 550:
            screen.blit(car_3_img_trans, (x_pos, y_pos))
        elif y_pos == 500:
            screen.blit(car_4_img_trans, (x_pos, y_pos))
        elif y_pos == 450:
            screen.blit(car_5_img_trans, (x_pos, y_pos))


def update_car(car: list) -> list:  # Moves the cars and gets rid of them if they get off-screen
    updated_cars = []

    for i in car:
        x_pos, y_pos, speed, car_direction = i
        if car_direction == 0:  # If car is coming in from the left, move it to the right
            x_pos -= speed
        if car_direction == 1:  # If car is coming in from the right, move it to the left
            x_pos += speed
        if 0 <= x_pos <= WIDTH:  # Makes sure cars only get added to the list if their on the screen
            updated_cars.append((x_pos, y_pos, speed, car_direction))

    return updated_cars

def score(score): #score board 
    myfont = pygame.font.SysFont("monospace", 40)
    scoretext = myfont.render("Score : "+str(score), 1, (0,0,0))
    screen.blit(scoretext, (5, 10))
    
pygame.init()

WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Frogger")
# ----------------------------
# Play Button variables 
button_image = pygame.image.load("play_button.png") #loading play button asset
button_rect = button_image.get_rect(center=(320, 250))
button_image = pygame.transform.scale(button_image, (300, 100)) #size of play button
button_rect = button_image.get_rect(center=(320, 130)) #location of play button 
# ---------------------------
# Initialize global variables

frog_x_size = 50
frog_y_size = 50
box_size = 50

frog_starting_x = WIDTH//2 - (frog_x_size//2)  # pygame starts from top left so to center it I did this
frog_starting_y = HEIGHT - 100

car_pos = [650, 600, 550, 500, 450]  # Y coordinates the cars can spawn in
cars = []
car_spawn_timer = 0
car_spawn_delay = 15  # Ensures that cars have a cooldown before spawning

# ---------------------------
# Loading graphics
frog_char_img = pygame.image.load('Graphics/Frog_char.png')
frog_char_img_trans = pygame.transform.scale(frog_char_img, (frog_x_size, frog_y_size))

car_1_img = pygame.image.load('Graphics/car_1.png')
car_1_img_trans = pygame.transform.scale(car_1_img, (frog_x_size, frog_y_size))

car_2_img = pygame.image.load('Graphics/car_2.png')
car_2_img_trans = pygame.transform.scale(car_2_img, (frog_x_size, frog_y_size))

car_3_img = pygame.image.load('Graphics/car_3.png')
car_3_img_trans = pygame.transform.scale(car_3_img, (frog_x_size, frog_y_size))

car_4_img = pygame.image.load('Graphics/car_4.png')
car_4_img_trans = pygame.transform.scale(car_4_img, (frog_x_size, frog_y_size))

car_5_img = pygame.image.load('Graphics/car_5.png')
car_5_img_trans = pygame.transform.scale(car_5_img, (frog_x_size * 2, frog_y_size))

# ---------------------------
# Game Loop
running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # HANDLING THE FROG MOVEMENTS
            if event.key == pygame.K_UP or event.key == ord("w"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'up')
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'down')
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'left')
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'right')
                
    # DRAWING
    screen.fill((255, 255, 255))
    draw_frog(frog_starting_x, frog_starting_y)
    
    # CAR SPAWNING
    if car_spawn_timer > 0:
        car_spawn_timer -= 0.5

    if car_spawn_timer <= 0:
        car_spawn = random.randint(1, 40)
        if car_spawn == 1:
            cars.append(generate_car())
            car_spawn_timer = car_spawn_delay

    cars = update_car(cars)

    draw_car(cars)

    pygame.display.flip()
    clock.tick(60)
    # ------------------------------------
    

pygame.quit()
