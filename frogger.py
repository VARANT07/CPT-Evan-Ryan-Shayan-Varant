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
    screen.blit(shop_sign, shop_button_loc)
    screen.blit(exit_button, exit_button_loc)


def game_screen():
    global car_spawn_timer, cars, fps_counter, timer, fly_counter, frames_per_fly_spawn, flies, death_timer, dead, \
        live, current_screen, frog_starting_x, frog_starting_y, death_pos, frame_counter, log_spawn_timer, logs
    screen.fill((0, 0, 255))
    frame_counter += 1

    screen.blit(road_img_trans, (0, (HEIGHT - 375)))

    screen.blit(ground_img_trans, (0, HEIGHT / 2))
    screen.blit(ground_img_trans, (0, HEIGHT - 100))

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

    # LOG SPAWNING
    if log_spawn_timer > 0:
        log_spawn_timer -= 0.5

    if log_spawn_timer <= 0:
        log_spawn = random.randint(1, 50)
        if log_spawn == 1:
            logs.append(generate_log())
            log_spawn_timer = log_spawn_reset

    logs = update_logs(logs)

    draw_log(logs)

    # FLY SPAWNING
    if frame_counter % frames_per_fly_spawn == 0:
        fly_pos = generate_fly_pos(fly_x_loc)
        fly_counter += 1
        flies.append(fly_pos)

    for fly in flies:
        draw_fly(fly)

    flies = fly_existing(flies)

    # SCORE
    score(starting_score)
    fps_counter += 1
    if fps_counter % fps == 0:
        timer -= 1
    if timer == 0:
        current_screen = "game_over"
    countdown(timer)

    car_collision(cars)
    water_collision(logs)

    lives()

    if dead:
        screen.blit(death_animation_img_trans, death_pos)
        death_timer -= 1
        if death_timer < 0:
            dead = False
            frog_starting_x = WIDTH // 2 - (frog_x_size // 2)
            frog_starting_y = HEIGHT - 100
            live -= 1
            death_timer = 120
            if live == 0:
                current_screen = "game_over"
    else:
        draw_frog(frog_starting_x, frog_starting_y)


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
    screen.blit(leader_button,leader_button_loc)
    screen.blit(leaderlabel,leader_board_loc)

def leaderboard():
    screen.fill(BG)
    screen.blit(back_button,back_button_loc)
    screen.blit(leaderlabel_options,leader_board_options_loc)





def shop_screen():
    screen.fill(BG)
    screen.blit(back_button, back_button_loc)
    screen.blit(christmas_skin, christmas_skin_loc)
    screen.blit(OG_skin, OG_skin_loc)
    screen.blit(miles_skin, miles_skin_loc)
    screen.blit(skin_text, skin_loc)


def game_over():
    screen.fill(BG)  # colour of Screen
    screen.blit(game_over_text, game_over_loc)
    screen.blit(play_again_button_image,play_again_rect)
    screen.blit(main_menu_button_image,main_menu_rect)

# ----------------- Movement Functions --------------------


def wasd_movement(movement_event: pygame.event.Event):
    global frog_starting_x, frog_starting_y
    if movement_event.key == ord("w"):
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'up')
    if movement_event.key == ord("s"):
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'down')
    if movement_event.key == ord("a"):
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'left')
    if movement_event.key == ord("d"):
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'right')


def arrow_movement(movement_event: pygame.event.Event):
    global frog_starting_x, frog_starting_y
    if movement_event.key == pygame.K_UP:
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'up')
    if movement_event.key == pygame.K_DOWN:
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'down')
    if movement_event.key == pygame.K_LEFT:
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'left')
    if movement_event.key == pygame.K_RIGHT:
        frog_starting_x, frog_starting_y = frog_movement(frog_starting_x, frog_starting_y, 'right')


# -------------------- Car/Frog/Log Generation and Display ---------


def draw_frog(x: int, y: int):
    if current_frog == "og_skin":
        screen.blit(frog_char_img_trans, (x, y))
    elif current_frog == "miles_skin":
        screen.blit(miles_skin_in_game, (x, y))
    elif current_frog == "christmas_skin":
        screen.blit(christmas_skin_in_game, (x, y))


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
    car_y_pos = random.choice(car_pos)
    car_pos.remove(car_y_pos)
    if car_y_pos == 600 or car_y_pos == 500:
        car_direction = 1  # come in from right
        car_x_pos = 0
    else:
        car_direction = 0  # come in from left
        car_x_pos = WIDTH
    speed = random.randint(15, 17) / 10  # Speed ranges from 1.5-1.7
    car_pos.append(car_y_pos)

    return car_x_pos, car_y_pos, speed, car_direction  # Returns a tuple with all the information needed to draw a car


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
    global frog_starting_x, frog_starting_y, dead, death_pos

    if not dead:
        for i in updated_cars:
            x_pos, y_pos, speed, car_direction = i
            if frog_starting_y == y_pos and x_pos - 50 < frog_starting_x < x_pos + 50:
                death_pos = frog_starting_x, frog_starting_y
                dead = True


def generate_log() -> tuple:
    log_y_pos = random.choice(log_pos)
    log_pos.remove(log_y_pos)  # Removing it and then adding it back at the end of the loop will fix the issue of multiple logs spawning at once in the same pos
    size = random.choice(log_sizes)
    random.shuffle(log_sizes)  # Fixes a weird glitch where it wont spawn on certain locations
    if log_y_pos % 100 == 0:
        direction = "right"
        log_x_pos = 0
    else:
        direction = "left"
        log_x_pos = WIDTH
    log_pos.append(log_y_pos)
    return log_x_pos, log_y_pos, direction, size


def draw_log(logs_list: list):
    for log in logs_list:
        log_x_pos, log_y_pos, direction, size = log
        if size == 2:
            screen.blit(log_1x2_img_trans, (log_x_pos, log_y_pos))
        elif size == 3:
            screen.blit(log_1x3_img_trans, (log_x_pos, log_y_pos))
        elif size == 4:
            screen.blit(log_1x4_img_trans, (log_x_pos, log_y_pos))


def update_logs(logs_list: list):
    updated_logs = []
    for log in logs_list:
        log_x_pos, log_y_pos, direction, size = log
        if direction == "right":
            log_x_pos += 1.5  # Make it a bit faster so the game doesn't look robotic
        elif direction == "left":
            log_x_pos -= 1
        if 0 <= log_x_pos <= WIDTH:
            updated_logs.append((log_x_pos, log_y_pos, direction, size))

    return updated_logs


def water_collision(updated_logs: list):
    global frog_starting_x, frog_starting_y, dead, death_pos
    if not dead and 150 <= frog_starting_y <= 350:
        on_log = False
        for log in updated_logs:
            x_pos, y_pos, direction, size = log
            if frog_starting_y == y_pos and x_pos < frog_starting_x < x_pos + (50*size):
                on_log = True
                if direction == "right":
                    frog_starting_x += 1.5
                elif direction == "left":
                    frog_starting_x -= 1
                break

        if not on_log:
            dead = True
            death_pos = frog_starting_x, frog_starting_y
            

# -------------------- Fly generation and display -------------------- --


def generate_fly_pos(x_pos: list) -> tuple:
    fly_width = random.choice(x_pos)
    fly_height = 100
    lifespan = frames_per_fly_spawn
    permanent = False
    return fly_width, fly_height, lifespan, permanent


def draw_fly(position):
    x, y, lifespan, permanent = position
    # DRAW FLY
    screen.blit(fly_img_trans, (x, y))


def erase_fly(position):
    x, y, lifespan, permanent = position
    pygame.draw.circle(screen, (0, 0, 255), (x + 25, y + 25), 30)


def fly_existing(flies_list: list):
    global starting_score
    update_flies = []

    for fly_char in flies_list:
        fly_width, fly_height, lifespan, permanent = fly_char

        if not permanent and frog_starting_x - 25 <= fly_width <= frog_starting_x + 25 and fly_height == frog_starting_y:
            permanent = True
            fly_x_loc.remove(fly_width)
            if len(fly_x_loc) == 0:
                fly_x_loc.append(1000000)  # Spawns in an area the use cannot see
            lifespan = -1
            starting_score += 10

        if not permanent:
            lifespan -= 1
            if lifespan > 0:
                update_flies.append((fly_width, fly_height, lifespan, permanent))
            else:
                erase_fly(fly_char)
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


def lives():  # LIVE DISPLAY
    global live
    my_font_3 = pygame.font.SysFont("monospace", 40)
    score_text = my_font_3.render("LIVES " + str(live), 1, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 500, 10))


def star_score():  # Adding Score if Star is hit
    global star, starting_score
    if frog_char_img == "hit":
        starting_score += 10  # Need to add proper variable
# --------------------------------------------------
# Game Set up


pygame.init()

WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Frogger")

# --------------------------------
# Initialize global variables

fps = 60
timer = 90
fps_counter = 0

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

log_pos = [350, 350, 300, 250, 200, 150]
logs = []
log_spawn_timer = 0
log_spawn_reset = 10
log_sizes = [2, 3, 3, 3, 4, 4]  # Sizes are dependent on 1xSize, for ex 2 is 1X2, 3 is 1X3, higher chance for bigger logs to make game easier

death_timer = 120
dead = False
death_pos = (0, 0)

fly_spawn_intervals = 5
frames_per_fly_spawn = fps * fly_spawn_intervals
frame_counter = 0
fly_counter = 0
fly_x_loc = [75, 225, 375, 525, 675]
flies = []

starting_score = 0

BG = (20, 30, 50)

movement = "WASD"

# ---------------------------
# Fonts and Writing
my_text_font = pygame.font.Font("Fonts/font.ttf", 50)  # made a font

control_font = pygame.font.Font("Fonts/font.ttf", 30)  # volume label font
control_text = control_font.render("Control settings", True, (255, 255, 255))  # actual text
control_loc = control_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # location of text

label_font = pygame.font.Font("Fonts/font.ttf", 36)  # Define font for the label
label_text = label_font.render("Options", True, (255, 255, 255))  # Render the text surface
label_rect = label_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))  # Position the text

volume_font = pygame.font.Font("Fonts/font.ttf", 30)  # volume label font
volume_text = volume_font.render("Volume", True, (255, 255, 255))  # actual text
volume_loc = volume_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # location of text

menu_text = my_text_font.render("FROGGER", True, (255, 255, 255))
text_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))  # location of main menu

# --------------------------------
# Buttons
button_image = pygame.image.load("Graphics/Home_screen/play_button.png")  # loading play button asset
button_image = pygame.transform.scale(button_image, (500, 150))  # size of play button
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # location of play button

options_button = pygame.image.load("Graphics/Home_screen/Options_button.jpeg")  # loading option button setting
options_button = pygame.transform.scale(options_button, (70, 70))  # size of button
options_button_rect = options_button.get_rect(center=(750, 700))  # Set location of options button

back_button = pygame.image.load("Graphics/Home_screen/back-button2.png")  # back button loading asset
back_button = pygame.transform.scale(back_button, (100, 100))  # size of back button
back_button_loc = back_button.get_rect(center=(100, 700))  # location of back button

on_button = pygame.image.load("Graphics/Home_screen/Sound_On_button.png")  # loading sound on button
on_button = pygame.transform.scale(on_button, (100, 100))  # size of button
on_button_loc = on_button.get_rect(center=(WIDTH // 2 - 75, HEIGHT // 3))  # loc of button

off_button = pygame.image.load("Graphics/Home_screen/Sound_off_button.png")  # loading sound on button
off_button = pygame.transform.scale(off_button, (100, 100))  # size of button
off_button_loc = off_button.get_rect(center=(WIDTH // 2 + 75, HEIGHT // 3))  # loc of button

exit_button = pygame.image.load("Graphics/Home_screen/Exit_game.png")  # loading sound on button
exit_button = pygame.transform.scale(exit_button, (500, 150))  # size of button
exit_button_loc = exit_button.get_rect(center=(WIDTH // 2, 700))  # location of button

arrow_button = pygame.image.load("Graphics/Home_screen/Arrow_keys_options.png")  # loading button asset
arrow_button = pygame.transform.scale(arrow_button, (80, 80))  # size of button
arrow_button_loc = arrow_button.get_rect(center=(WIDTH // 2 + 75, 450))

wasd_button = pygame.image.load("Graphics/Home_screen/wasd.png")  # loading button asset
wasd_button = pygame.transform.scale(wasd_button, (80, 80))
wasd_button_loc = wasd_button.get_rect(center=(WIDTH // 2 - 75, 450))

restart_button = pygame.image.load("Graphics/Home_screen/Restart_button.png")
restart_button = pygame.transform.scale(restart_button, (500, 150))  # size of button
restart_button_loc = restart_button.get_rect(center=(WIDTH // 2, 700))  # loc of button

shop_sign = pygame.image.load("Graphics/Home_screen/shop_button.png")
shop_sign = pygame.transform.scale(shop_sign, (500, 300))  # size of button
shop_button_loc = shop_sign.get_rect(center=(WIDTH // 2, HEIGHT // 2))

game_over_font = pygame.font.Font("Fonts/font.ttf", 36)  # Define font for the label
game_over_text = game_over_font.render("Game_Over", True, (255, 255, 255))  # Render the text surface
game_over_loc = game_over_text.get_rect(center=(400, 100))  # Position the text

# leader board
leader_button = pygame.image.load("Leader_board.png")
leader_button = pygame.transform.scale(leader_button, (500, 400)) # size of button 
leader_button_loc = leader_button.get_rect(center = (WIDTH // 2, 700)) # loc of button

# leader label
leader_font = pygame.font.Font("font.ttf", 50)
leaderlabel= leader_font.render("Leaderboard", True, (255,255,255))
leader_board_loc = leaderlabel.get_rect(center = (WIDTH//2, 700))

# leader label in the leaderboard screen
leader_font_options = pygame.font.Font("font.ttf", 50)
leaderlabel_options = leader_font_options.render("Leaderboard", True, (255,255,255))
leader_board_options_loc = leaderlabel.get_rect(center = (WIDTH//2, HEIGHT // 8))

#Play Again Button 
play_again_button = pygame.image.load("")  # loading play again button asset (Need to add an image)
play_again_button_image = pygame.transform.scale(play_again_button, (250, 75))  # size of play button
play_again_rect = play_again_button_image.get_rect(center =(400,300))  # location of play button
#Main Menu Button 
main_menu_button = pygame.image.load("")  # loading play again button asset (Need to add an image)
main_menu_button_image = pygame.transform.scale(main_menu_button, (250, 75))  # size of play button
main_menu_rect = main_menu_button_image.get_rect(center =(400,400))  # location of play button

skin_font = pygame.font.Font("Fonts/font.ttf", 50)  # volume label font
skin_text = skin_font.render("Skins", True, (255, 255, 255))  # actual text
skin_loc = skin_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))  # location of text

# ---------------------------
# Loading Game Assets
frog_char_img = pygame.image.load('Graphics/Game_assets/Frog_char.png')
frog_char_img_trans = pygame.transform.scale(frog_char_img, (box_size, box_size))

car_1_img = pygame.image.load('Graphics/Cars and Logs/car_1.png')
car_1_img_trans = pygame.transform.scale(car_1_img, (box_size, box_size))

car_2_img = pygame.image.load('Graphics/Cars and Logs/car_2.png')
car_2_img_trans = pygame.transform.scale(car_2_img, (box_size, box_size))

car_3_img = pygame.image.load('Graphics/Cars and Logs/car_3.png')
car_3_img_trans = pygame.transform.scale(car_3_img, (box_size, box_size))

car_4_img = pygame.image.load('Graphics/Cars and Logs/car_4.png')
car_4_img_trans = pygame.transform.scale(car_4_img, (box_size, box_size))

car_5_img = pygame.image.load('Graphics/Cars and Logs/car_5.png')
car_5_img_trans = pygame.transform.scale(car_5_img, (box_size * 2, box_size))

log_1x2_img = pygame.image.load('Graphics/Cars and Logs/1X2 Log.png')
log_1x2_img_trans = pygame.transform.scale(log_1x2_img, (box_size * 2, box_size))

log_1x3_img = pygame.image.load('Graphics/Cars and Logs/1X3 Log.png')
log_1x3_img_trans = pygame.transform.scale(log_1x3_img, (box_size * 3, box_size))

log_1x4_img = pygame.image.load('Graphics/Cars and Logs/1X4 Log.png')
log_1x4_img_trans = pygame.transform.scale(log_1x4_img, (box_size * 4, box_size))

fly_img = pygame.image.load("Graphics/Game_assets/fly.png")
fly_img_trans = pygame.transform.scale(fly_img, (box_size, box_size))

star_char_img = pygame.image.load('Graphics/Game_assets/star.png')
star_char_img_trans = pygame.transform.scale(star_char_img, (box_size, box_size))

death_animation_img = pygame.image.load("Graphics/Game_assets/death_animation.png")
death_animation_img_trans = pygame.transform.scale(death_animation_img, (box_size, box_size))

ground_img = pygame.image.load("Graphics/Game_assets/Ground.png")
ground_img_trans = pygame.transform.scale(ground_img, (WIDTH, box_size))

road_img = pygame.image.load("Graphics/Game_assets/Road.png")
road_img_trans = pygame.transform.scale(road_img, (WIDTH, box_size * 6))

water_img = pygame.image.load("Graphics/Game_assets/Water.png")
water_img_trans = pygame.transform.scale(water_img, (WIDTH, box_size))

christmas_skin = pygame.image.load("Graphics/Game_assets/christmas_frog_skin.png")
christmas_skin = pygame.transform.scale(christmas_skin, (150, 150))
christmas_skin_in_game = pygame.transform.scale(christmas_skin, (box_size, box_size))
christmas_skin_loc = christmas_skin.get_rect(center=(WIDTH // 2, HEIGHT // 2))

OG_skin = pygame.image.load("Graphics/Game_assets/Frog_char.png")
OG_skin = pygame.transform.scale(OG_skin, (150, 150))
OG_skin_loc = OG_skin.get_rect(center=(150, HEIGHT//2))

miles_skin = pygame.image.load("Graphics/Game_assets/miles_morales_frog.png")
miles_skin = pygame.transform.scale(miles_skin, (150, 150))
miles_skin_in_game = pygame.transform.scale(miles_skin, (box_size, box_size))
miles_skin_loc = OG_skin.get_rect(center=(WIDTH-150, HEIGHT//2))
# ---------------------------------------
# load music 
pygame.mixer.init()
sound = pygame.mixer.Sound("Sounds/339124__zagi2__gaming-arcade-loop.wav")
sound.play(-1)
current_frog = "og_skin"  # initial skin

current_screen = "main_menu"

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
            if movement == "WASD":
                wasd_movement(event)
            elif movement == "arrows":
                arrow_movement(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_location = pygame.mouse.get_pos()
            if current_screen == "main_menu":
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "game_screen"
                elif options_button_rect.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "options"
                if shop_button_loc.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "shop_screen"
                elif exit_button_loc.collidepoint(pygame.mouse.get_pos()):
                    running = False
            elif current_screen == "options":
                if back_button_loc.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "main_menu"
                elif arrow_button_loc.collidepoint(pygame.mouse.get_pos()):
                    movement = "arrows"
                elif wasd_button_loc.collidepoint(pygame.mouse.get_pos()):
                    movement = "WASD"
                elif on_button_loc.collidepoint(pygame.mouse.get_pos()):
                    volume_on = True
                    pygame.mixer.unpause()
                elif off_button_loc.collidepoint(pygame.mouse.get_pos()):
                    volume_on = False
                    pygame.mixer.pause()
                elif leader_button_loc.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "leaderboard"
            elif current_screen == "shop_screen":
                if back_button_loc.collidepoint(pygame.mouse.get_pos()):
                    current_screen = "main_menu"
                elif OG_skin_loc.collidepoint(pygame.mouse.get_pos()):
                     current_frog = "Og_skin"
                 elif miles_skin_loc.collidepoint(pygame.mouse.get_pos()):
                     current_frog = "miles_skin"
                 elif christmas_skin_loc.collidepoint(pygame.mouse.get_pos()):
                     current_frog = "christmas_skin"

    screen.fill((0, 0, 0))


    # SCREENS
    if current_screen == "main_menu":
        main_menu()
    elif current_screen == "game_screen":
        game_screen()
    elif current_screen == "options":
        options_menu()
    elif current_screen == "shop_screen":
        shop_screen()
    elif current_screen == "leaderboard":
        leaderboard()
      
    pygame.display.flip()
    clock.tick(fps)
    # ------------------------------------

pygame.quit()
