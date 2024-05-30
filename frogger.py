# Frogger
import pygame
import random

# -------------------- Car and Frog Generation and Display ---------


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
    for car_info in car:
        x_pos, y_pos, _, _ = car_info
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

    for car_info in car:
        x_pos, y_pos, speed, car_direction = car_info
        if car_direction == 0:  # If car is coming in from the left, move it to the right
            x_pos -= speed
        if car_direction == 1:  # If car is coming in from the right, move it to the left
            x_pos += speed
        if 0 <= x_pos <= WIDTH:  # Makes sure cars only get added to the list if their on the screen
            updated_cars.append((x_pos, y_pos, speed, car_direction))

    return updated_cars


# -------------------- Fly generation and display -------------------- --


def generate_fly_pos():
    fly_width = random.randint(0, WIDTH - 1)
    fly_height = random.randint(0, HEIGHT - 1)
    return fly_width, fly_height


def draw_fly (position):
    x, y = position
    # DRAW FLY
    # pygame.draw.circle(screen, (240, 240, 240), (x, y), 30)


# -------------------- Display of the score and the Timer ------------ 


def score(scr: int): #score board Display
    my_font = pygame.font.SysFont("monospace", 40)
    score_text = my_font.render("Score : "+str(scr), 1, (0,0,0))
    screen.blit(score_text, (5, 10))


def countdown(timer): #Timer Display
    my_font_2 = pygame.font.SysFont("monospace", 40)
    score_text = my_font_2.render("Timer : "+str(timer), 1, (0,0,0))
    screen.blit(score_text, (WIDTH - 250, 10))


pygame.init()

WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Frogger")
fps = 60
timer = 90
fps_counter = 0

# ---------------------------
# Play Button assets
button_image = pygame.image.load("Graphics/Home_screen/play_button.png") #loading play button asset
button_rect = button_image.get_rect(center=(320, 250))

button_image = pygame.transform.scale(button_image, (300, 100)) #size of play button
button_rect = button_image.get_rect(center=(320, 130)) #location of play button 
# ------------------------
# options button assets 
options_button = pygame.image.load("Graphics/Home_screen/Options_button_pixleart.jpeg")# loading options button settings
options_button_rect = options_button.get_rect(center=(100,100))

options_button = pygame.transform.scale(options_button, (50, 50))# size of button
options_button_rect = options_button.get_rect(center=(600, 450))  # Set location of options button
#-----------------------------------
# Main menu text
menu_text = mytextfont.render("FROGGER", True, (255,255,255))
text_rect = menu_text.get_rect(center=(320,50))#location of main menu

# ----------------------------
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

fly_spawn_intervals = 5
frames_per_fly_spawn = fps * fly_spawn_intervals

starting_score = 0

# ---------------------------
# Loading Game Asset
frog_char_img = pygame.image.load('Graphics/Game_assets/Frog_char.png')
frog_char_img_trans = pygame.transform.scale(frog_char_img, (frog_x_size, frog_y_size))

car_1_img = pygame.image.load('Graphics/Cars/car_1.png')
car_1_img_trans = pygame.transform.scale(car_1_img, (frog_x_size, frog_y_size))

car_2_img = pygame.image.load('Graphics/Cars/car_2.png')
car_2_img_trans = pygame.transform.scale(car_2_img, (frog_x_size, frog_y_size))

car_3_img = pygame.image.load('Graphics/Cars/car_3.png')
car_3_img_trans = pygame.transform.scale(car_3_img, (frog_x_size, frog_y_size))

car_4_img = pygame.image.load('Graphics/Cars/car_4.png')
car_4_img_trans = pygame.transform.scale(car_4_img, (frog_x_size, frog_y_size))

car_5_img = pygame.image.load('Graphics/Cars/car_5.png')
car_5_img_trans = pygame.transform.scale(car_5_img, (frog_x_size * 2, frog_y_size))

Current_screen = "main menu" # initial screen 
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
        # Screen Functions
        def main_menu(): 
         pygame.display.set_caption("Menu")
         screen.fill(BG) # colour of screen
         screen.blit(button_image, button_rect)
         screen.blit(menu_text, text_rect)
         screen.blit(options_button, options_button_rect)

        def game_screen(): 
         screen.fill((0, 100, 0)) # colour of screen

        def options_menu():
         screen.fill((BG)) # colour of screen
         screen.blit(volume_text, volume_loc)
         screen.blit(back_button, back_button_loc)
         screen.blit(label_text, label_rect)
         screen.blit(on_button, on_button_loc)
         screen.blit(off_button, off_button_loc)
          

     
                    
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
    
    # SCORE
    score(starting_score)
    fps_counter += 1
    if fps_counter % fps == 0:
        timer -= 1
    countdown(timer)

    pygame.display.flip()
    clock.tick(fps)
    # ------------------------------------
    

pygame.quit()
