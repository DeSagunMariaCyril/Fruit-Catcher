import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions for landscape
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catcher")

# Load images (ensure these files exist in your directory)
background = pygame.image.load("background_image.jpeg")
fruit_basket = pygame.image.load("fruit_basket.png")
apple_img = pygame.image.load("apple.png")
cherry_img = pygame.image.load("cherry.png")
bomb_img = pygame.image.load("bomb.png")
apple_half_img = pygame.image.load("appleHalf.png")
lemon_half_img = pygame.image.load("lemonHalf.png")
play_button = pygame.image.load("play_button.png")
quit_button = pygame.image.load("quit_button.png")
shield_img = pygame.image.load("shield.png")  # Power-up image for shield
double_points_img = pygame.image.load("double_points.png")  # Power-up image for double points
retry_button = pygame.image.load("retry_button.png")  # Retry button image

# Resize images
apple_img = pygame.transform.scale(apple_img, (80, 80))
cherry_img = pygame.transform.scale(cherry_img, (80, 80))
apple_half_img = pygame.transform.scale(apple_half_img, (80, 80))
lemon_half_img = pygame.transform.scale(lemon_half_img, (80, 80))
bomb_img = pygame.transform.scale(bomb_img, (80, 80))
play_button = pygame.transform.scale(play_button, (400, 150))
quit_button = pygame.transform.scale(quit_button, (400, 150))
shield_img = pygame.transform.scale(shield_img, (80, 80))
double_points_img = pygame.transform.scale(double_points_img, (80, 80))
retry_button = pygame.transform.scale(retry_button, (400, 150))

# Load game-style fonts
title_font = pygame.font.SysFont("pressstart2p", 80)
feedback_font = pygame.font.SysFont("pressstart2p", 50)
font = pygame.font.SysFont("comicsansms", 40)
game_over_font = pygame.font.SysFont("pressstart2p", 80)
shield_font = pygame.font.SysFont("comicsansms", 30)

# Define object sizes and speeds
basket_width = 120
basket_height = 200
basket_speed = 15
fruit_speed = 5

# Game variables
score = 0
level = 1
basket_x = (screen_width - basket_width) // 2
basket_y = screen_height - basket_height - 10
achievement_message = ""
objects = []
bomb_chance = 0.1
next_object_time = 100
shield_active = False
double_points_active = False
lives = 5
missed_fruits = 0
shield_count = 0
shield_timer = 0
shield_lifetime = 5
last_shield_spawn = 0
double_points_timer = 0  # Track double points duration

# Level feedback messages
level_feedback = [
    "Welcome to the game! Start catching fruits!",
    "Things are getting faster!",
    "Watch out for bombs!",
    "You're doing great!",
    "Keep going!"
]

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load fruit categories
healthy_fruit_images = [apple_img, cherry_img]
rotten_fruit_images = [apple_half_img, lemon_half_img]
power_up_images = [shield_img, double_points_img]

# Function to display the main menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill((255, 255, 255))

        # Display title
        title_text = title_font.render("Fruit Catcher", True, (255, 0, 0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

        # Display play and quit buttons
        play_button_rect = screen.blit(play_button, (screen_width // 2 - play_button.get_width() // 2, screen_height // 2))
        quit_button_rect = screen.blit(quit_button, (screen_width // 2 - quit_button.get_width() // 2, screen_height // 2 + 160))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    show_instructions()  # Show instructions before starting the game
                    menu_running = False
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# Function to display the instructions screen
def show_instructions():
    screen.fill((255, 255, 255))
    instructions_text1 = font.render("INSTRUCTIONS:", True, (0, 0, 0))
    instructions_text2 = font.render("Use the LEFT and RIGHT arrow keys", True, (0, 0, 0))
    instructions_text3 = font.render("to move the basket and catch fruits.", True, (0, 0, 0))
    instructions_text4 = font.render("Avoid rotten fruits and bombs!", True, (0, 0, 0))
    instructions_text5 = font.render("Press any key to start the game.", True, (255, 0, 0))

    screen.blit(instructions_text1, (screen_width // 2 - instructions_text1.get_width() // 2, screen_height // 4))
    screen.blit(instructions_text2, (screen_width // 2 - instructions_text2.get_width() // 2, screen_height // 4 + 50))
    screen.blit(instructions_text3, (screen_width // 2 - instructions_text3.get_width() // 2, screen_height // 4 + 100))
    screen.blit(instructions_text4, (screen_width // 2 - instructions_text4.get_width() // 2, screen_height // 4 + 150))
    screen.blit(instructions_text5, (screen_width // 2 - instructions_text5.get_width() // 2, screen_height // 4 + 200))

    pygame.display.update()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()  # Start the game after the instructions
                waiting_for_start = False

# Main game loop
def game_loop():
    global score, basket_x, next_object_time, bomb_chance, level, achievement_message, shield_active, double_points_active, lives, missed_fruits, fruit_speed, objects, shield_count, shield_timer, last_shield_spawn, double_points_timer

    objects = []
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < screen_width - basket_width:
            basket_x += basket_speed

        # Spawn objects (including shield and double points)
        next_object_time -= 1
        if next_object_time <= 0 and len(objects) < 10:
            object_x = random.randint(0, screen_width - basket_width)
            if random.random() < bomb_chance:
                object_img = bomb_img
            elif score >= (last_shield_spawn + 80):  # Only spawn the shield once every 80 points
                object_img = shield_img
                last_shield_spawn = score  # Update the last shield spawn to current score
            elif random.random() < 0.2:  # 20% chance to spawn double points
                object_img = double_points_img
            else:
                object_img = random.choice(healthy_fruit_images + rotten_fruit_images)
            objects.append({"img": object_img, "x": object_x, "y": -100})
            next_object_time = random.randint(60, 120)

        # Move objects and handle collisions
        new_objects = []
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
        for obj in objects:
            obj["y"] += fruit_speed
            obj_rect = pygame.Rect(obj["x"], obj["y"], 80, 80)

            if obj_rect.colliderect(basket_rect):
                if obj["img"] == bomb_img:
                    if not shield_active:
                        lives -= 1
                        achievement_message = f"Boom! Lives left: {lives}"
                        if lives <= 0:
                            running = False
                    else:
                        achievement_message = "Shield protected you!"
                        shield_active = False  # Deactivate shield after use
                        shield_count -= 1  # Decrement shield count
                elif obj["img"] in healthy_fruit_images:
                    score += 20 if double_points_active else 10
                    achievement_message = "Healthy fruit caught!"
                elif obj["img"] in rotten_fruit_images:
                    score -= 5
                    missed_fruits += 1
                    achievement_message = f"Oops! Rotten fruit missed! Total missed: {missed_fruits}"
                elif obj["img"] == shield_img:
                    if not shield_active:  # Only catch a new shield if it's not active
                        shield_active = True
                        shield_count += 1  # Increment shield count
                        shield_timer = time.time()  # Record the time when shield was caught
                        achievement_message = "Shield activated!"
                elif obj["img"] == double_points_img:
                    double_points_active = True
                    double_points_timer = time.time()  # Start the timer for double points
                    achievement_message = "Double points activated!"

            elif obj["y"] < screen_height:
                new_objects.append(obj)

        objects = new_objects

        # Check if the shield timer has expired (5 seconds)
        if shield_active and time.time() - shield_timer > shield_lifetime:
            shield_active = False
            achievement_message = "Shield expired!"

        # Check if double points timer has expired (10 seconds)
        if double_points_active and time.time() - double_points_timer > 10:
            double_points_active = False
            achievement_message = "Double points expired!"

        # Level progression every 100 points
        new_level = score // 100 + 1
        if new_level > level:
            level = new_level
            fruit_speed += 1
            achievement_message = f"Level {level} unlocked!"

        # After Level 5, stop the game and show the message
        if level >= 5:
            achievement_message = "Congratulations! You've completed the game!"
            final_message()

        # Render score and lives
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        achievement_text = feedback_font.render(achievement_message, True, (0, 255, 0))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (screen_width - 200, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(achievement_text, (screen_width // 2 - achievement_text.get_width() // 2, 50))

        # Draw basket and objects
        screen.blit(fruit_basket, (basket_x, basket_y))
        for obj in objects:
            screen.blit(obj["img"], (obj["x"], obj["y"]))

        # Display shield status and countdown if active
        if shield_active:
            remaining_time = max(0, int(shield_lifetime - (time.time() - shield_timer)))
            shield_text = shield_font.render(f"Shield Active: {remaining_time}s", True, (0, 255, 0))
            screen.blit(shield_text, (screen_width // 2 - shield_text.get_width() // 2, screen_height // 2 + 60))

        # Display double points status and countdown if active
        if double_points_active:
            remaining_time = max(0, int(10 - (time.time() - double_points_timer)))
            double_points_text = shield_font.render(f"Double Points: {remaining_time}s", True, (0, 0, 255))
            screen.blit(double_points_text, (screen_width // 2 - double_points_text.get_width() // 2, screen_height // 2 + 100))

        pygame.display.update()
        clock.tick(60)

    # Game over
    game_over()

# Function to display game over screen
def game_over():
    global score
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Your score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))

    retry_button_rect = screen.blit(retry_button, (screen_width // 2 - retry_button.get_width() // 2, screen_height // 2 + 120))
    pygame.display.update()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    score = 0
                    level = 1
                    lives = 3
                    game_loop()
                    waiting_for_retry = False

# Function to display final completion message
def final_message():
    screen.fill((255, 255, 255))
    message = game_over_font.render("Congratulations! You completed the game!", True, (0, 255, 0))
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - 50))
    pygame.display.update()

    time.sleep(5)  # Wait for 5 seconds before returning to the main menu
    main_menu()

# Start the game
main_menu()
