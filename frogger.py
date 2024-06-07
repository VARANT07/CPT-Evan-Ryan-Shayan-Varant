# Frogger
import pygame
import random


# ------------------ Screen Functions -----------------
def main_menu():
    pygame.display.set_caption("Menu")
    screen.fill(BG)  # colour of screen
    screen.blit(button_image, button_rect)
    screen.blit(menu_text, text_rect)
    screen.blit(options_button, options_button_rect)
    screen.blit(shop_sign,shop_button_loc)
    screen.blit(exit_button, exit_button_loc)




def game_screen():
    global car_spawn_timer, cars, fps_counter, timer, fly_counter, frames_per_fly_spawn, flies
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

    if frame_counter % frames_per_fly_spawn == 0:
        fly_position = generate_fly_pos(fly_x_loc)
        fly_counter += 1
        flies.append(fly_position)


    for fly in flies:
        draw_fly(fly)
    
    flies = fly_existing(flies)

    # SCORE
    score(starting_score)
    fps_counter += 1
    if fps_counter % fps == 0:
        timer -= 1
    if timer < 0:
        screen.fill((0, 0, 0))
    countdown(timer)



def options_menu():
    screen.fill(BG)  # colour of screen
    screen.blit(volume_text, volume_loc)
    screen.blit(back_button, back_button_loc)
    screen.blit(label_text, label_rect)
    screen.blit(on_button, on_button_loc)
    screen.blit(off_button, off_button_loc)
    screen.blit(control_text, control_loc)
    screen.blit(arrow_button, arrow_button_loc)
    screen.blit(wasd_button, wasd_button_loc)
    screen.blit(restart_button,restart_button_loc)


def shop_screen():
    screen.fill(BG)
    screen.blit(back_button, back_button_loc)



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


def car_collision(updated_cars: list):
    global frog_starting_x, frog_starting_y
    for i in updated_cars:
        x_pos, y_pos, speed, car_direction = i
        if frog_starting_y == y_pos and x_pos - 50 < frog_starting_x < x_pos + 50:
            death_pos = frog_starting_x, frog_starting_y
            # screen.blit(death_animation_img_trans, (death_pos))
            # RESPAWN
            frog_starting_x = WIDTH // 2 - (frog_x_size // 2)  # pygame starts from top left so to center it I did this
            frog_starting_y = HEIGHT - 100
            return True


# -------------------- Fly generation and display -------------------- --


def generate_fly_pos(x_pos: list) -> tuple:
    fly_width = random.choice(x_pos)
    fly_height = 100
    lifespan = frames_per_fly_spawn
    permanent = False
    return fly_width, fly_height, lifespan, permanent

def draw_fly (position):
    x, y, lifespan, permanent = position
    # DRAW FLY
    screen.blit(fly_img_trans, (x, y))

def erase_fly(position):
    x, y, lifespan, permanent = position
    pygame.draw.circle(screen, (0, 0, 255), (x + 25, y + 25), 30)

def fly_existing(flies_list: list):
    update_flies = []

    for fly_char in flies_list:
        fly_width, fly_height, lifespan, permanent = fly_char

        if not permanent and fly_width == frog_starting_x and fly_height == frog_starting_y:
            permanent = True
            lifespan = -1

        if not permanent:
            lifespan -= 1
            if lifespan > 0:
                update_flies.append((fly_width, fly_height, lifespan, permanent))
            else:
                erase_fly(fly)
        else:
            update_flies.append((fly_width, fly_height, lifespan, permanent))

    return update_flies


# -------------------- Display of the score and the Timer ------------


def score(scr: int):  # score board Display
    my_font = pygame.font.SysFont("monospace", 40)
    score_text = my_font.render("Score : " + str(scr), 1, (0, 0, 0))
    screen.blit(score_text, (5, 10))


def countdown(timer_countdown):  # Timer Display
    my_font_2 = pygame.font.SysFont("monospace", 40)
    score_text = my_font_2.render("Timer : " + str(timer_countdown), 1, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 250, 10))

def lives(): #LIVE DISPLAY
    global live
    my_font_3 = pygame.font.SysFont("monospace", 40)
    scoretext = my_font_3.render("LIVES "+str(live), 1, (0,0,0))
    screen.blit(scoretext, (WIDTH - 400, 10))

def hit_counter(): #LIVE HIT COUNTER
    global live, current_screen
    if frog_char_img == "hit": 
        live -= 1
    if live == 0:
        current_screen = "game_over_screen"

def star_score():#Adding Score if Star is hit 
    global star
    if frog_char_img == "hit":
        starting_score += 10 #Need to add proper variable 

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
# font 
my_text_font = pygame.font.Font("Fonts/font.ttf", 50) #made a font 


#--------------------------------

# Play Button assets
button_image = pygame.image.load("Graphics/Home_screen/play_button.png")  # loading play button asset
button_rect = button_image.get_rect(center=(320, 250))

button_image = pygame.transform.scale(button_image, (300, 100))  # size of play button
button_rect = button_image.get_rect(center=(320, 130))  # location of play button
# ------------------------
# options button assets
options_button = pygame.image.load("Graphics/Home_screen/Options_button_pixleart.jpeg")  # loading options button settings
options_button_rect = options_button.get_rect(center=(100, 100))

options_button = pygame.transform.scale(options_button, (50, 50))  # size of button
options_button_rect = options_button.get_rect(center=(600, 450))  # Set location of options button
# -----------------------------------
# Main menu text
menu_text = my_text_font.render("FROGGER", True, (255, 255, 255))
text_rect = menu_text.get_rect(center=(320, 50))  # location of main menu
# ------------------------------------
#Back button assets
back_button = pygame.image.load("Graphics/Home_screen/back-button2 (1).png") # back button loading asset
back_button_loc= back_button.get_rect(center=(100,100))
back_button = pygame.transform.scale(back_button, (75, 75)) #size of back button
back_button_loc = back_button.get_rect(center=(50,450)) #location of back button 

# -----------------------

#---------------------------
# options label 
label_font = pygame.font.Font("Fonts/font.ttf", 36)  # Define font for the label
label_text = label_font.render("Options", True, (255, 255, 255))  # Render the text surface
label_rect = label_text.get_rect(center=(320,50))  # Position the text
# --------------------------
# Volume label
volume_font = pygame.font.Font("Fonts/font.ttf", 30) # volume label font 
volume_text = volume_font.render("Volume", True, (255,255,255)) # actual text
volume_loc = volume_text.get_rect(center = (320, 100)) # location of text
#---------------------------
# Volume on button
on_button = pygame.image.load("Graphics/Home_screen/Sound_On_button.png") # loading sound on button
on_button = pygame.transform.scale(on_button, (50, 50))  # size of button
on_button_loc = on_button.get_rect(center=(250, 150)) # loc of button
# -------------------------
# Volume off button
off_button = pygame.image.load("Graphics/Home_screen/Sound_off_button.png") # loading sound on button
off_button = pygame.transform.scale(off_button, (50, 50))  # size of button
off_button_loc = off_button.get_rect(center=(400, 150)) # loc of button

#-----------------------
#Control label 
control_font = pygame.font.Font("Fonts/font.ttf", 30) # volume label font 
control_text = control_font.render("Control settings", True, (255,255,255)) # actual text
control_loc = control_text.get_rect(center = (320, 200)) # location of text
# -------------------
# exit button
exit_button = pygame.image.load("Graphics/Home_screen/Exit_game(1).png")  # loading sound on button
exit_button = pygame.transform.scale(exit_button, (300, 100)) # size of button
exit_button_loc = exit_button.get_rect(center = (320, 400)) # location of button
# ----------------------------
# arrow keys image 
arrow_button = pygame.image.load("Graphics/Home_screen/Arrow_keys_options.png") # loading button asset
arrow_button = pygame.transform.scale(arrow_button, (80, 80)) # size of button
arrow_button_loc = arrow_button.get_rect(center = (400, 250))
# ---------------------
#wasd keys image
wasd_button = pygame.image.load("Graphics/Home_screen/wasd.png") # loading button asset
wasd_button = pygame.transform.scale(wasd_button, (80, 80))
wasd_button_loc = wasd_button.get_rect(center = (250, 250))
#----------------------
# restart progress button
restart_button = pygame.image.load("Graphics/Home_screen/Restart_button.png")
restart_button = pygame.transform.scale(restart_button, (300, 100)) # size of button 
restart_button_loc = restart_button.get_rect(center = (320, 400)) # loc of button
#------------------------------
# shop sign 
shop_sign = pygame.image.load("Graphics/Home_screen/shop_button.png")
shop_sign = pygame.transform.scale(shop_sign, (400,200)) #size of button
shop_button_loc = shop_sign.get_rect(center = (320, 255)) # Loc of button 
# Initialize global variables

live = 3
frog_x_size = 50
frog_y_size = 50
box_size = 50

frog_starting_x = WIDTH // 2 - (frog_x_size // 2)  # pygame starts from top left so to center it I did this
frog_starting_y = HEIGHT - 100

car_pos = [650, 600, 550, 500, 450]  # Y coordinates the cars can spawn in
cars = []
car_spawn_timer = 0
car_spawn_delay = 15  # Ensures that cars have a cooldown before spawning

fly_spawn_intervals = 5
frames_per_fly_spawn = fps * fly_spawn_intervals
frame_counter = 0
fly_counter = 0
fly_x_loc = [100, 250, 400, 550, 700]
fly_position = generate_fly_pos(fly_x_loc)
flies = []

starting_score = 0

BG = (20,30,50)

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

fly_img = pygame.image.load("Fly.png")
fly_img_trans = pygame.transform.scale(fly_img, (50, 50))

star_char_img = pygame.image.load('Graphics/Game_assets/star.png') 
star_char_img_trans = pygame.transform.scale(star_char_img, (box_size, box_size)) 

death_animation_img = pygame.image.load("Graphics/Game_assets/death_animation.png")
death_animation_img_trans = pygame.transform.scale(death_animation_img, (box_size, box_size))

current_screen = "main_menu"  # initial screen
# ---------------------------
# Game Loop
running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # HANDLING THE FROG MOVEMENTS
            if event.key == pygame.K_UP or event.key == ord("w"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'up')
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'down')
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'left')
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'right')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_location = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_location):
                current_screen = "game_screen"
            elif options_button_rect.collidepoint(pygame.mouse.get_pos()):
                    Current_screen = "options"
             if shop_button_loc.collidepoint(pygame.mouse.get_pos()):
                    Current_screen = "shop_screen"
            elif exit_button_loc.collidepoint(pygame.mouse.get_pos()):
                    running = False
            elif current_screen == "options":
                if back_button_loc.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "main_menu"
                elif on_button_loc.collidepoint(pygame.mouse.get_pos()):
                    volume_on = True
                    pygame.mixer.unpause()
                elif off_button_loc.collidepoint(pygame.mouse.get_pos()):
                    volume_on = False
                    pygame.mixer.pause()

    # DRAWING


    # SCREENS
    if current_screen == "main_menu":
        main_menu()
    elif current_screen == "game_screen":
        game_screen()

    pygame.display.flip()
    clock.tick(fps)
    # ------------------------------------

pygame.quit()
